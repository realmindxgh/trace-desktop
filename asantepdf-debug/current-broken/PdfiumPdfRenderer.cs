using System.IO;
using System.Runtime.InteropServices;
using System.Windows;
using System.Windows.Media;
using System.Text;
using System.Windows.Media.Imaging;
using PDFiumCore;

namespace PdfRescue.App;

public sealed record PdfTextCharacter(int Index, string Text, Rect PdfBounds);
public sealed record PdfTextPage(double Width, double Height, IReadOnlyList<PdfTextCharacter> Characters)
{
    public string FullText => string.Concat(Characters.Select(x => x.Text));
}

/// <summary>
/// Production PDF renderer backed by PDFium. Rendering is serialized per document
/// because PDFium document/page handles are not treated as concurrently mutable state.
/// </summary>
public sealed class PdfiumPdfRenderer : IPdfRenderer
{
    private const int RenderAnnotations = 0x01;
    private const int RenderLcdText = 0x02;
    private const uint MaxRenderWidth = 8192;
    private const int MaxRenderHeight = 16384;

    private readonly SemaphoreSlim _gate = new(1, 1);
    private FpdfDocumentT? _document;
    private bool _disposed;

    public uint PageCount { get; private set; }

    public PdfiumPdfRenderer()
    {
        PdfiumRuntime.EnsureInitialized();
    }

    public async Task OpenAsync(string path, CancellationToken cancellationToken = default)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(path);
        var fullPath = Path.GetFullPath(path);
        if (!File.Exists(fullPath))
            throw new FileNotFoundException("PDF file was not found.", fullPath);

        ThrowIfDisposed();
        await _gate.WaitAsync(cancellationToken).ConfigureAwait(false);
        try
        {
            cancellationToken.ThrowIfCancellationRequested();
            CloseDocumentCore();

            var loaded = await Task.Run(
                () => fpdfview.FPDF_LoadDocument(fullPath, string.Empty),
                cancellationToken).ConfigureAwait(false);

            if (loaded is null)
            {
                var error = fpdfview.FPDF_GetLastError();
                throw new InvalidDataException($"PDFium could not open the PDF. Error code: {error}.");
            }

            _document = loaded;
            var count = fpdfview.FPDF_GetPageCount(loaded);
            if (count < 0)
            {
                CloseDocumentCore();
                throw new InvalidDataException("PDFium returned an invalid page count.");
            }

            PageCount = checked((uint)count);
        }
        catch
        {
            if (_document is not null && PageCount == 0)
                CloseDocumentCore();
            throw;
        }
        finally
        {
            _gate.Release();
        }
    }

    public async Task<PdfTextPage> ExtractTextPageAsync(int oneBasedPageNumber, CancellationToken cancellationToken = default)
    {
        ThrowIfDisposed();
        await _gate.WaitAsync(cancellationToken).ConfigureAwait(false);
        try
        {
            cancellationToken.ThrowIfCancellationRequested();
            var document = _document ?? throw new InvalidOperationException("No PDF is open.");
            if (oneBasedPageNumber < 1 || oneBasedPageNumber > PageCount)
                throw new ArgumentOutOfRangeException(nameof(oneBasedPageNumber));
            return await Task.Run(() => ExtractTextCore(document, oneBasedPageNumber - 1, cancellationToken), cancellationToken).ConfigureAwait(false);
        }
        finally { _gate.Release(); }
    }

    private static PdfTextPage ExtractTextCore(FpdfDocumentT document, int zeroBasedPageNumber, CancellationToken token)
    {
        var page = fpdfview.FPDF_LoadPage(document, zeroBasedPageNumber);
        if (page is null) throw new InvalidDataException($"PDFium could not load page {zeroBasedPageNumber + 1}.");
        try
        {
            var width = fpdfview.FPDF_GetPageWidthF(page);
            var height = fpdfview.FPDF_GetPageHeightF(page);
            var textPage = fpdf_text.FPDFTextLoadPage(page);
            if (textPage is null) return new PdfTextPage(width, height, []);
            try
            {
                var count = Math.Max(0, fpdf_text.FPDFTextCountChars(textPage));
                var chars = new List<PdfTextCharacter>(count);
                for (var i = 0; i < count; i++)
                {
                    token.ThrowIfCancellationRequested();
                    var codePoint = checked((int)fpdf_text.FPDFTextGetUnicode(textPage, i));
                    string text;
                    try { text = codePoint <= 0 ? string.Empty : char.ConvertFromUtf32(codePoint); }
                    catch { text = string.Empty; }
                    double left = 0, right = 0, bottom = 0, top = 0;
                    if (!fpdf_text.FPDFTextGetCharBox(textPage, i, ref left, ref right, ref bottom, ref top)) continue;
                    chars.Add(new PdfTextCharacter(i, text, new Rect(left, bottom, Math.Max(0, right - left), Math.Max(0, top - bottom))));
                }
                return new PdfTextPage(width, height, chars);
            }
            finally { fpdf_text.FPDFTextClosePage(textPage); }
        }
        finally { fpdfview.FPDF_ClosePage(page); }
    }

    public async Task<BitmapSource> RenderAsync(
        int oneBasedPageNumber,
        uint width,
        CancellationToken cancellationToken = default)
    {
        ThrowIfDisposed();
        if (width == 0)
            throw new ArgumentOutOfRangeException(nameof(width), "Render width must be greater than zero.");

        await _gate.WaitAsync(cancellationToken).ConfigureAwait(false);
        try
        {
            cancellationToken.ThrowIfCancellationRequested();
            var document = _document ?? throw new InvalidOperationException("No PDF is open.");
            if (oneBasedPageNumber < 1 || oneBasedPageNumber > PageCount)
                throw new ArgumentOutOfRangeException(nameof(oneBasedPageNumber));

            var requestedWidth = Math.Min(width, MaxRenderWidth);
            return await Task.Run(
                () => RenderCore(document, oneBasedPageNumber - 1, requestedWidth, cancellationToken),
                cancellationToken).ConfigureAwait(false);
        }
        finally
        {
            _gate.Release();
        }
    }

    private static BitmapSource RenderCore(
        FpdfDocumentT document,
        int zeroBasedPageNumber,
        uint requestedWidth,
        CancellationToken cancellationToken)
    {
        cancellationToken.ThrowIfCancellationRequested();

        var page = fpdfview.FPDF_LoadPage(document, zeroBasedPageNumber);
        if (page is null)
            throw new InvalidDataException($"PDFium could not load page {zeroBasedPageNumber + 1}.");

        try
        {
            var pageWidth = fpdfview.FPDF_GetPageWidthF(page);
            var pageHeight = fpdfview.FPDF_GetPageHeightF(page);
            if (pageWidth <= 0 || pageHeight <= 0)
                throw new InvalidDataException($"Page {zeroBasedPageNumber + 1} has invalid dimensions.");

            var pixelWidth = checked((int)requestedWidth);
            var proportionalHeight = Math.Max(1, (int)Math.Ceiling(pixelWidth * (pageHeight / pageWidth)));
            var pixelHeight = Math.Min(proportionalHeight, MaxRenderHeight);

            var bitmap = fpdfview.FPDFBitmapCreate(pixelWidth, pixelHeight, 1);
            if (bitmap is null)
                throw new OutOfMemoryException("PDFium could not allocate the page bitmap.");

            try
            {
                cancellationToken.ThrowIfCancellationRequested();
                _ = fpdfview.FPDFBitmapFillRect(bitmap, 0, 0, pixelWidth, pixelHeight, 0xFFFFFFFFUL);
                fpdfview.FPDF_RenderPageBitmap(
                    bitmap,
                    page,
                    0,
                    0,
                    pixelWidth,
                    pixelHeight,
                    0,
                    RenderAnnotations | RenderLcdText);

                cancellationToken.ThrowIfCancellationRequested();
                var stride = fpdfview.FPDFBitmapGetStride(bitmap);
                var buffer = fpdfview.FPDFBitmapGetBuffer(bitmap);
                if (stride <= 0 || buffer == IntPtr.Zero)
                    throw new InvalidDataException("PDFium returned an invalid bitmap buffer.");

                var byteCount = checked(stride * pixelHeight);
                var pixels = new byte[byteCount];
                Marshal.Copy(buffer, pixels, 0, byteCount);

                var source = BitmapSource.Create(
                    pixelWidth,
                    pixelHeight,
                    96,
                    96,
                    PixelFormats.Bgra32,
                    null,
                    pixels,
                    stride);
                source.Freeze();
                return source;
            }
            finally
            {
                fpdfview.FPDFBitmapDestroy(bitmap);
            }
        }
        finally
        {
            fpdfview.FPDF_ClosePage(page);
        }
    }

    public void Dispose()
    {
        if (_disposed) return;
        _gate.Wait();
        try
        {
            if (_disposed) return;
            _disposed = true;
            CloseDocumentCore();
        }
        finally
        {
            _gate.Release();
            _gate.Dispose();
        }
    }

    private void CloseDocumentCore()
    {
        if (_document is not null)
        {
            fpdfview.FPDF_CloseDocument(_document);
            _document = null;
        }
        PageCount = 0;
    }

    private void ThrowIfDisposed() => ObjectDisposedException.ThrowIf(_disposed, this);

    private static class PdfiumRuntime
    {
        private static readonly object Sync = new();
        private static bool _initialized;

        public static void EnsureInitialized()
        {
            if (_initialized) return;
            lock (Sync)
            {
                if (_initialized) return;
                fpdfview.FPDF_InitLibrary();
                _initialized = true;
            }
        }
    }
}
