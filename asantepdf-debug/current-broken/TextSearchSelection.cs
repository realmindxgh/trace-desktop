using System.Collections.ObjectModel;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;
using PdfRescue.App.Services;

namespace PdfRescue.App;

public partial class MainWindow
{
    private PdfTextPage? _currentTextPage;
    private int? _textSelectionStart;
    private int? _textSelectionEnd;
    private int _textLayerSourcePage;
    private int _textLayerRotation;
    private readonly ObservableCollection<DocumentSearchHit> _searchHits = new();

    private async Task LoadTextLayerAsync(int sourcePageNumber, BitmapSource bitmap, int rotation, CancellationToken token)
    {
        _currentTextPage = null;
        _textSelectionStart = null;
        _textSelectionEnd = null;
        _textLayerSourcePage = sourcePageNumber;
        _textLayerRotation = rotation % 360;
        TextSelectionCanvas.Children.Clear();
        TextSelectionCanvas.Width = bitmap.PixelWidth;
        TextSelectionCanvas.Height = bitmap.PixelHeight;
        TextSelectionCanvas.Visibility = _markupMode == MarkupMode.None ? Visibility.Visible : Visibility.Collapsed;
        if (_textLayerRotation != 0 || _renderer is not PdfiumPdfRenderer pdfium) return;
        try
        {
            _currentTextPage = await pdfium.ExtractTextPageAsync(sourcePageNumber, token);
        }
        catch (OperationCanceledException) { }
        catch (Exception ex)
        {
            App.Log("Text layer extraction failed: " + ex.Message);
        }
    }

    private void TextSelection_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
    {
        if (_busy || _markupMode != MarkupMode.None || _currentTextPage is null || _textLayerRotation != 0) return;
        var point = e.GetPosition(TextSelectionCanvas);
        var index = HitTextCharacter(point);
        if (index is null) return;
        _textSelectionStart = index;
        _textSelectionEnd = index;
        TextSelectionCanvas.CaptureMouse();
        DrawTextSelection();
        e.Handled = true;
    }

    private void TextSelection_MouseMove(object sender, MouseEventArgs e)
    {
        if (e.LeftButton != MouseButtonState.Pressed || _textSelectionStart is null || _currentTextPage is null) return;
        var index = HitTextCharacter(e.GetPosition(TextSelectionCanvas), nearest: true);
        if (index is null) return;
        _textSelectionEnd = index;
        DrawTextSelection();
        e.Handled = true;
    }

    private void TextSelection_MouseLeftButtonUp(object sender, MouseButtonEventArgs e)
    {
        if (_textSelectionStart is null) return;
        TextSelectionCanvas.ReleaseMouseCapture();
        var index = HitTextCharacter(e.GetPosition(TextSelectionCanvas), nearest: true);
        if (index is not null) _textSelectionEnd = index;
        DrawTextSelection();
        e.Handled = true;
    }

    private int? HitTextCharacter(Point point, bool nearest = false)
    {
        if (_currentTextPage is null || PreviewImage.Source is not BitmapSource bitmap) return null;
        int? best = null;
        var bestDistance = double.MaxValue;
        foreach (var character in _currentTextPage.Characters)
        {
            var rect = PdfRectToPixelRect(character.PdfBounds, _currentTextPage, bitmap);
            var expanded = rect;
            expanded.Inflate(3, 3);
            if (expanded.Contains(point)) return character.Index;
            if (!nearest) continue;
            var cx = Math.Clamp(point.X, rect.Left, rect.Right);
            var cy = Math.Clamp(point.Y, rect.Top, rect.Bottom);
            var d = (point.X - cx) * (point.X - cx) + (point.Y - cy) * (point.Y - cy);
            if (d < bestDistance) { bestDistance = d; best = character.Index; }
        }
        return nearest && bestDistance < 1600 ? best : null;
    }

    private void DrawTextSelection()
    {
        TextSelectionCanvas.Children.Clear();
        if (_currentTextPage is null || PreviewImage.Source is not BitmapSource bitmap || _textSelectionStart is null || _textSelectionEnd is null) return;
        var min = Math.Min(_textSelectionStart.Value, _textSelectionEnd.Value);
        var max = Math.Max(_textSelectionStart.Value, _textSelectionEnd.Value);
        var selected = _currentTextPage.Characters.Where(x => x.Index >= min && x.Index <= max).ToArray();
        foreach (var lineRect in GroupSelectionRects(selected, _currentTextPage, bitmap))
        {
            var rectangle = new Rectangle
            {
                Width = Math.Max(1, lineRect.Width),
                Height = Math.Max(1, lineRect.Height),
                Fill = new SolidColorBrush(Color.FromArgb(82, 46, 144, 250)),
                Stroke = new SolidColorBrush(Color.FromArgb(130, 46, 144, 250)),
                StrokeThickness = 0.7,
                IsHitTestVisible = false
            };
            Canvas.SetLeft(rectangle, lineRect.Left);
            Canvas.SetTop(rectangle, lineRect.Top);
            TextSelectionCanvas.Children.Add(rectangle);
        }
    }

    private static IReadOnlyList<Rect> GroupSelectionRects(IEnumerable<PdfTextCharacter> chars, PdfTextPage page, BitmapSource bitmap)
    {
        var rects = chars.Select(c => PdfRectToPixelRect(c.PdfBounds, page, bitmap)).Where(r => r.Width > 0 && r.Height > 0).OrderBy(r => r.Top).ThenBy(r => r.Left).ToList();
        var lines = new List<Rect>();
        foreach (var rect in rects)
        {
            var lineIndex = lines.FindIndex(line => Math.Abs((line.Top + line.Height / 2) - (rect.Top + rect.Height / 2)) <= Math.Max(4, Math.Min(line.Height, rect.Height) * 0.55));
            if (lineIndex < 0) lines.Add(rect);
            else lines[lineIndex] = Rect.Union(lines[lineIndex], rect);
        }
        return lines.OrderBy(r => r.Top).ThenBy(r => r.Left).ToArray();
    }

    private static Rect PdfRectToPixelRect(Rect pdfRect, PdfTextPage page, BitmapSource bitmap)
    {
        if (page.Width <= 0 || page.Height <= 0) return Rect.Empty;
        var x = pdfRect.Left / page.Width * bitmap.PixelWidth;
        var y = (page.Height - pdfRect.Top) / page.Height * bitmap.PixelHeight;
        var width = pdfRect.Width / page.Width * bitmap.PixelWidth;
        var height = pdfRect.Height / page.Height * bitmap.PixelHeight;
        return new Rect(x, y, width, height);
    }

    private string GetSelectedText()
    {
        if (_currentTextPage is null || _textSelectionStart is null || _textSelectionEnd is null) return string.Empty;
        var min = Math.Min(_textSelectionStart.Value, _textSelectionEnd.Value);
        var max = Math.Max(_textSelectionStart.Value, _textSelectionEnd.Value);
        var sb = new StringBuilder();
        foreach (var c in _currentTextPage.Characters.Where(x => x.Index >= min && x.Index <= max).OrderBy(x => x.Index)) sb.Append(c.Text);
        return sb.ToString().Replace("\u0000", string.Empty).Trim();
    }

    private void CopySelectedText_Click(object sender, RoutedEventArgs e)
    {
        var text = GetSelectedText();
        if (string.IsNullOrEmpty(text)) return;
        Clipboard.SetText(text);
        StatusText.Text = "Selected text copied.";
    }

    private async void HighlightSelectedText_Click(object sender, RoutedEventArgs e)
    {
        if (_currentPdf is null || _currentTextPage is null || PreviewImage.Source is not BitmapSource bitmap || _textSelectionStart is null || _textSelectionEnd is null) return;
        var min = Math.Min(_textSelectionStart.Value, _textSelectionEnd.Value);
        var max = Math.Max(_textSelectionStart.Value, _textSelectionEnd.Value);
        var selected = _currentTextPage.Characters.Where(x => x.Index >= min && x.Index <= max).ToArray();
        var rects = GroupSelectionRects(selected, _currentTextPage, bitmap);
        if (rects.Count == 0) return;
        var output = AskSavePath("Save highlighted PDF", SuggestName(_currentPdf, "highlighted"));
        if (output is null) return;
        var areas = rects.Select(r => new NormalizedPdfRect(r.X / bitmap.PixelWidth, r.Y / bitmap.PixelHeight, r.Width / bitmap.PixelWidth, r.Height / bitmap.PixelHeight)).ToArray();
        var page = PagesList.SelectedItem as PdfPageItem;
        if (page is null) return;
        var ok = await RunPdfOperationAsync("Highlighting selected text...", "Highlighted text.", token => AddMultipleHighlightsAsync(_currentPdf, output, page.SourcePageNumber, areas, token));
        if (ok) await ShowCompletionAsync("Highlight complete", output, true);
    }

    private async Task AddMultipleHighlightsAsync(string input, string output, int pageNumber, IReadOnlyList<NormalizedPdfRect> areas, CancellationToken token)
    {
        if (areas.Count == 0) throw new ArgumentException("No text selection was available to highlight.", nameof(areas));
        var tempDir = Path.Combine(Path.GetTempPath(), "AsantePDF", "text-highlight", Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(tempDir);
        try
        {
            var current = input;
            for (var i = 0; i < areas.Count; i++)
            {
                token.ThrowIfCancellationRequested();
                var next = i == areas.Count - 1 ? output : Path.Combine(tempDir, $"step-{i:000}.pdf");
                await _markup.AddHighlightAsync(current, next, pageNumber, areas[i], token);
                current = next;
                SetDeterminateProgress(i + 1, areas.Count, $"Highlighting line {i + 1:N0} of {areas.Count:N0}...");
            }
        }
        finally { try { Directory.Delete(tempDir, true); } catch { } }
    }

    private void SearchSelectedText_Click(object sender, RoutedEventArgs e)
    {
        var text = GetSelectedText();
        if (string.IsNullOrWhiteSpace(text)) return;
        DocumentSearchBox.Text = text.Length > 80 ? text[..80] : text;
        _ = RunDocumentSearchAsync(DocumentSearchBox.Text);
    }

    private void TextSelection_ContextMenuOpening(object sender, ContextMenuEventArgs e)
    {
        if (string.IsNullOrWhiteSpace(GetSelectedText())) e.Handled = true;
    }

    private async void DocumentSearchBox_KeyDown(object sender, KeyEventArgs e)
    {
        if (e.Key == Key.Enter) { await RunDocumentSearchAsync(DocumentSearchBox.Text); e.Handled = true; }
        else if (e.Key == Key.Escape) { DocumentSearchBox.Clear(); _searchHits.Clear(); SearchResultsList.ItemsSource = null; TextSelectionCanvas.Children.Clear(); e.Handled = true; }
    }

    private async void FindNext_Click(object sender, RoutedEventArgs e)
    {
        if (_searchHits.Count == 0) { await RunDocumentSearchAsync(DocumentSearchBox.Text); return; }
        var next = SearchResultsList.SelectedIndex < 0 ? 0 : (SearchResultsList.SelectedIndex + 1) % _searchHits.Count;
        SearchResultsList.SelectedIndex = next;
        await NavigateToSearchHitAsync(_searchHits[next]);
    }

    private async Task RunDocumentSearchAsync(string query)
    {
        query = query?.Trim() ?? string.Empty;
        if (_currentPdf is null || query.Length == 0 || _renderer is not PdfiumPdfRenderer pdfium) return;
        _searchHits.Clear();
        ShowSidebar("search");
        SearchResultsList.ItemsSource = _searchHits;
        var current = PagesList.SelectedIndex;
        await RunBusyAsync("Searching document...", async token =>
        {
            for (var pageNumber = 1; pageNumber <= (int)_renderer.PageCount; pageNumber++)
            {
                token.ThrowIfCancellationRequested();
                SetDeterminateProgress(pageNumber - 1, (int)_renderer.PageCount, $"Searching page {pageNumber:N0} of {_renderer.PageCount:N0}...");
                var page = await pdfium.ExtractTextPageAsync(pageNumber, token);
                var text = page.FullText;
                var index = 0;
                while ((index = text.IndexOf(query, index, StringComparison.CurrentCultureIgnoreCase)) >= 0)
                {
                    var from = Math.Max(0, index - 42);
                    var length = Math.Min(text.Length - from, query.Length + 84);
                    var snippet = text.Substring(from, length).Replace('\r', ' ').Replace('\n', ' ').Trim();
                    _searchHits.Add(new DocumentSearchHit(pageNumber, snippet));
                    index += Math.Max(1, query.Length);
                }
            }
            SetDeterminateProgress((int)_renderer.PageCount, (int)_renderer.PageCount, $"Found {_searchHits.Count:N0} result(s)." );
        });
        if (current >= 0 && current < Pages.Count) PagesList.SelectedIndex = current;
        StatusText.Text = _searchHits.Count == 0 ? "No matches found." : $"Found {_searchHits.Count:N0} match(es).";
    }

    private async void SearchResultsList_MouseDoubleClick(object sender, MouseButtonEventArgs e)
    {
        if (SearchResultsList.SelectedItem is DocumentSearchHit hit) await NavigateToSearchHitAsync(hit);
    }

    private async Task NavigateToSearchHitAsync(DocumentSearchHit hit)
    {
        var target = Pages.FirstOrDefault(x => x.SourcePageNumber == hit.SourcePageNumber) ?? Pages.ElementAtOrDefault(hit.SourcePageNumber - 1);
        if (target is null) return;
        PagesList.SelectedItem = target;
        PagesList.ScrollIntoView(target);
        await RenderPreviewAsync(target);
    }

    private sealed record DocumentSearchHit(int SourcePageNumber, string Snippet)
    {
        public override string ToString() => $"Page {SourcePageNumber}: {Snippet}";
    }
}
