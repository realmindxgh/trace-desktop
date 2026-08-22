using System.Text.Json;

namespace PdfRescue.App.Services;

public enum AppThemePreference
{
    System,
    Light,
    Dark
}

public enum RecentViewMode
{
    Grid,
    List,
    Compact
}

public sealed class RecentDocumentEntry
{
    public string Path { get; set; } = string.Empty;
    public DateTimeOffset LastOpenedUtc { get; set; } = DateTimeOffset.UtcNow;
    public int LastPage { get; set; } = 1;
    public int PageCount { get; set; }
    public uint PreviewWidth { get; set; } = 1100;
    public bool Pinned { get; set; }
    public string? ThumbnailPath { get; set; }
}

public sealed class WorkspacePageState
{
    public int SourcePageNumber { get; set; }
    public int Rotation { get; set; }
}

public sealed class WorkspaceSessionEntry
{
    public string Path { get; set; } = string.Empty;
    public int LastPage { get; set; } = 1;
    public uint PreviewWidth { get; set; } = 1100;
    public bool Modified { get; set; }
    public List<WorkspacePageState> Layout { get; set; } = [];
}

public sealed class AsantePdfAppState
{
    public AppThemePreference Theme { get; set; } = AppThemePreference.System;
    public RecentViewMode RecentView { get; set; } = RecentViewMode.Grid;
    public bool ReopenLastSession { get; set; } = true;
    public bool TrackRecentDocuments { get; set; } = true;
    public List<RecentDocumentEntry> RecentDocuments { get; set; } = [];
    public List<WorkspaceSessionEntry> LastSession { get; set; } = [];
}

public sealed class AppStateStore
{
    private readonly object _gate = new();
    private readonly JsonSerializerOptions _json = new() { WriteIndented = true };

    public static string RootDirectory => Path.Combine(
        Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "AsantePDF");

    public static string StatePath => Path.Combine(RootDirectory, "state.json");
    public static string ThumbnailDirectory => Path.Combine(RootDirectory, "Thumbnails");
    public static string RecoveryDirectory => Path.Combine(RootDirectory, "Recovery");

    public AsantePdfAppState Load()
    {
        lock (_gate)
        {
            try
            {
                Directory.CreateDirectory(RootDirectory);
                Directory.CreateDirectory(ThumbnailDirectory);
                Directory.CreateDirectory(RecoveryDirectory);
                if (!File.Exists(StatePath)) return new AsantePdfAppState();
                var state = JsonSerializer.Deserialize<AsantePdfAppState>(File.ReadAllText(StatePath), _json)
                            ?? new AsantePdfAppState();
                state.RecentDocuments ??= [];
                state.LastSession ??= [];
                return state;
            }
            catch (Exception ex)
            {
                App.Log("Could not load app state: " + ex);
                return new AsantePdfAppState();
            }
        }
    }

    public void Save(AsantePdfAppState state)
    {
        lock (_gate)
        {
            try
            {
                Directory.CreateDirectory(RootDirectory);
                var temp = StatePath + ".tmp";
                File.WriteAllText(temp, JsonSerializer.Serialize(state, _json));
                File.Move(temp, StatePath, true);
            }
            catch (Exception ex)
            {
                App.Log("Could not save app state: " + ex);
            }
        }
    }

    public static string ThumbnailPathFor(string pdfPath)
    {
        var bytes = System.Security.Cryptography.SHA256.HashData(System.Text.Encoding.UTF8.GetBytes(Path.GetFullPath(pdfPath).ToUpperInvariant()));
        return Path.Combine(ThumbnailDirectory, Convert.ToHexString(bytes)[..24] + ".png");
    }
}
