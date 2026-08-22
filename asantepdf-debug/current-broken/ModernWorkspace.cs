using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Diagnostics;
using System.IO;
using System.Runtime.CompilerServices;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Threading;
using Microsoft.Win32;
using PdfRescue.App.Services;

namespace PdfRescue.App;

public partial class MainWindow
{
    private readonly AppStateStore _stateStore = new();
    private AsantePdfAppState _appState = new();
    private readonly ObservableCollection<RecentDocumentCardViewModel> _recentCards = new();
    private readonly ObservableCollection<DocumentTabViewModel> _documentTabViews = new();
    private readonly List<DocumentSession> _documentSessions = new();
    private DocumentSession? _activeSession;
    private bool _openingFromTabSwitch;
    private bool _closingAccepted;
    private RecentViewMode _recentViewMode = RecentViewMode.Grid;
    private DispatcherTimer? _taskTimer;
    private readonly Stopwatch _taskStopwatch = new();
    private bool _taskMinimized;
    private IPdfRenderer? _secondaryRenderer;
    private DocumentSession? _secondarySession;
    private bool _syncingScroll;

    private void InitializeModernWorkspace()
    {
        _appState = _stateStore.Load();
        _recentViewMode = _appState.RecentView;
        ThemeManager.Apply(_appState.Theme);
        UpdateThemeGlyph();

        RecentDocumentsItems.ItemsSource = _recentCards;
        DocumentTabsItems.ItemsSource = _documentTabViews;
        ApplyRecentViewTemplate();
        UpdateResumeSessionButton();
        RefreshRecentCards();
        ApplyWorkspaceVisibility();

        _taskTimer = new DispatcherTimer { Interval = TimeSpan.FromSeconds(1) };
        _taskTimer.Tick += (_, _) =>
        {
            if (!_taskStopwatch.IsRunning) return;
            TaskElapsedText.Text = _taskStopwatch.Elapsed.TotalMinutes >= 1
                ? $"{(int)_taskStopwatch.Elapsed.TotalMinutes}:{_taskStopwatch.Elapsed.Seconds:00} elapsed"
                : $"{_taskStopwatch.Elapsed.Seconds}s elapsed";
        };
        _taskTimer.Start();
    }

    private void ApplyWorkspaceVisibility()
    {
        var hasDocument = _currentPdf is not null && Pages.Count > 0;
        HomeView.Visibility = hasDocument ? Visibility.Collapsed : Visibility.Visible;
        WorkspaceView.Visibility = hasDocument ? Visibility.Visible : Visibility.Collapsed;
        ZoomStatusItem.Visibility = hasDocument ? Visibility.Visible : Visibility.Collapsed;
        PageStatusText.Text = hasDocument ? PageStatusText.Text : "Home";
        if (!hasDocument)
        {
            PreviewImage.Source = null;
            TextSelectionCanvas.Children.Clear();
        }
    }

    private void UpdateThemeGlyph()
    {
        ThemeToggleGlyph.Text = ThemeManager.IsDark ? "\uE706" : "\uE708"; // sun / moon
        ThemeToggleButton.ToolTip = ThemeManager.IsDark ? "Switch to light mode" : "Switch to dark mode";
    }

    private void ThemeToggle_Click(object sender, RoutedEventArgs e)
    {
        _appState.Theme = ThemeManager.IsDark ? AppThemePreference.Light : AppThemePreference.Dark;
        ThemeManager.Apply(_appState.Theme);
        UpdateThemeGlyph();
        _stateStore.Save(_appState);
        RefreshDocumentTabsVisuals();
    }

    private void Settings_Click(object sender, RoutedEventArgs e)
    {
        var theme = new ComboBox { MinWidth = 220, Margin = new Thickness(0, 6, 0, 12) };
        theme.Items.Add("Follow Windows");
        theme.Items.Add("Light");
        theme.Items.Add("Dark");
        theme.SelectedIndex = _appState.Theme switch { AppThemePreference.Light => 1, AppThemePreference.Dark => 2, _ => 0 };

        var reopen = new CheckBox { Content = "Offer to resume my last workspace", IsChecked = _appState.ReopenLastSession, Margin = new Thickness(0, 4, 0, 8) };
        var recent = new CheckBox { Content = "Keep a recent documents list", IsChecked = _appState.TrackRecentDocuments, Margin = new Thickness(0, 4, 0, 8) };
        var clear = new Button { Content = "Clear recent documents", HorizontalAlignment = HorizontalAlignment.Left, Margin = new Thickness(0, 6, 0, 12) };
        clear.Click += (_, _) =>
        {
            _appState.RecentDocuments.Clear();
            _stateStore.Save(_appState);
            RefreshRecentCards();
        };

        var content = new StackPanel();
        content.Children.Add(new TextBlock { Text = "Appearance", FontWeight = FontWeights.SemiBold });
        content.Children.Add(theme);
        content.Children.Add(new TextBlock { Text = "Startup & privacy", FontWeight = FontWeights.SemiBold });
        content.Children.Add(reopen);
        content.Children.Add(recent);
        content.Children.Add(clear);
        content.Children.Add(new TextBlock
        {
            Text = "AsantePDF is completely free. There are no premium features, subscriptions or usage limits.",
            TextWrapping = TextWrapping.Wrap,
            Foreground = (Brush)Application.Current.Resources["MutedTextBrush"],
            Margin = new Thickness(0, 8, 0, 4)
        });

        var window = BuildPromptWindow("AsantePDF Settings", "Choose how AsantePDF should behave.", content, out var ok);
        window.Background = (Brush)Application.Current.Resources["PanelBackground"];
        ok.Content = "Save";
        ok.Click += (_, _) => window.DialogResult = true;
        if (window.ShowDialog() != true) return;

        _appState.Theme = theme.SelectedIndex switch { 1 => AppThemePreference.Light, 2 => AppThemePreference.Dark, _ => AppThemePreference.System };
        _appState.ReopenLastSession = reopen.IsChecked == true;
        _appState.TrackRecentDocuments = recent.IsChecked == true;
        if (!_appState.TrackRecentDocuments) _appState.RecentDocuments.Clear();
        ThemeManager.Apply(_appState.Theme);
        UpdateThemeGlyph();
        _stateStore.Save(_appState);
        RefreshRecentCards();
        UpdateResumeSessionButton();
    }

    private void Home_Click(object sender, RoutedEventArgs e) => ShowHomeWithoutClosingDocuments();
    private void RecentNav_Click(object sender, RoutedEventArgs e) => ShowHomeWithoutClosingDocuments();
    private void ToolsNav_Click(object sender, RoutedEventArgs e) => ShowHomeWithoutClosingDocuments();

    private void ShowHomeWithoutClosingDocuments()
    {
        CaptureActiveSessionState();
        _currentPdf = null;
        Pages.Clear();
        ApplyWorkspaceVisibility();
        RefreshRecentCards();
        UpdateResumeSessionButton();
        UpdateCommandStates();
    }

    private async void ResumeSession_Click(object sender, RoutedEventArgs e)
    {
        var entries = _appState.LastSession.Where(x => File.Exists(x.Path)).ToArray();
        if (entries.Length == 0)
        {
            UpdateResumeSessionButton();
            return;
        }

        foreach (var entry in entries)
        {
            await OpenPdfAsync(entry.Path);
            if (_activeSession is null) continue;
            _activeSession.LastPage = Math.Max(1, entry.LastPage);
            _activeSession.PreviewWidth = entry.PreviewWidth;
            _activeSession.Modified = entry.Modified;
            _activeSession.Layout = entry.Layout.Select(x => new SessionPageState(x.SourcePageNumber, x.Rotation)).ToList();
        }
        if (_activeSession is not null) await ActivateDocumentSessionAsync(_activeSession);
    }

    private void UpdateResumeSessionButton()
    {
        var count = _appState.ReopenLastSession
            ? _appState.LastSession.Count(x => File.Exists(x.Path))
            : 0;
        ResumeSessionButton.Visibility = count > 0 ? Visibility.Visible : Visibility.Collapsed;
        ResumeSessionText.Text = count switch
        {
            1 => "Resume last document",
            > 1 => $"Resume {count} documents",
            _ => "Resume session"
        };
    }

    private void RefreshRecentCards()
    {
        var valid = _appState.RecentDocuments
            .Where(x => File.Exists(x.Path))
            .GroupBy(x => Path.GetFullPath(x.Path), StringComparer.OrdinalIgnoreCase)
            .Select(g => g.First())
            .ToList();
        _appState.RecentDocuments = valid;

        IEnumerable<RecentDocumentEntry> sorted = valid;
        var sort = RecentSortCombo.SelectedIndex;
        if (sort == 1) sorted = sorted.OrderBy(x => Path.GetFileName(x.Path), StringComparer.OrdinalIgnoreCase);
        else if (sort == 2) sorted = sorted.OrderByDescending(x => SafeModifiedUtc(x.Path));
        else sorted = sorted.OrderByDescending(x => x.Pinned).ThenByDescending(x => x.LastOpenedUtc);

        _recentCards.Clear();
        foreach (var entry in sorted.Take(40))
        {
            var vm = new RecentDocumentCardViewModel(entry);
            _recentCards.Add(vm);
            _ = LoadRecentThumbnailAsync(vm, entry);
        }

        var any = _recentCards.Count > 0;
        RecentsHeader.Visibility = any ? Visibility.Visible : Visibility.Collapsed;
        RecentDocumentsItems.Visibility = any ? Visibility.Visible : Visibility.Collapsed;
        NoRecentsPanel.Visibility = any ? Visibility.Collapsed : Visibility.Visible;
    }

    private static DateTime SafeModifiedUtc(string path)
    {
        try { return File.GetLastWriteTimeUtc(path); } catch { return DateTime.MinValue; }
    }

    private async Task LoadRecentThumbnailAsync(RecentDocumentCardViewModel vm, RecentDocumentEntry entry)
    {
        try
        {
            var cached = entry.ThumbnailPath;
            if (string.IsNullOrWhiteSpace(cached)) cached = AppStateStore.ThumbnailPathFor(entry.Path);
            if (File.Exists(cached))
            {
                vm.Thumbnail = LoadBitmap(cached);
                return;
            }

            using var renderer = PdfRendererFactory.CreateProduction();
            await renderer.OpenAsync(entry.Path, _lifetime.Token);
            if (renderer.PageCount == 0) return;
            var bitmap = await renderer.RenderAsync(1, 360, _lifetime.Token);
            Directory.CreateDirectory(AppStateStore.ThumbnailDirectory);
            SaveBitmapPng(bitmap, cached);
            entry.ThumbnailPath = cached;
            entry.PageCount = checked((int)renderer.PageCount);
            vm.Meta = BuildRecentMeta(entry);
            vm.Thumbnail = bitmap;
            _stateStore.Save(_appState);
        }
        catch (OperationCanceledException) { }
        catch (Exception ex) { App.Log("Recent thumbnail failed: " + ex.Message); }
    }

    private static BitmapSource LoadBitmap(string path)
    {
        using var stream = File.OpenRead(path);
        var decoder = new PngBitmapDecoder(stream, BitmapCreateOptions.PreservePixelFormat, BitmapCacheOption.OnLoad);
        var frame = decoder.Frames[0];
        frame.Freeze();
        return frame;
    }

    private static void SaveBitmapPng(BitmapSource bitmap, string path)
    {
        var encoder = new PngBitmapEncoder();
        encoder.Frames.Add(BitmapFrame.Create(bitmap));
        using var stream = File.Create(path);
        encoder.Save(stream);
    }

    private static string BuildRecentMeta(RecentDocumentEntry entry)
    {
        var age = DateTimeOffset.UtcNow - entry.LastOpenedUtc;
        var when = age.TotalMinutes < 2 ? "just now" : age.TotalHours < 1 ? $"{(int)age.TotalMinutes}m ago" : age.TotalDays < 1 ? $"{(int)age.TotalHours}h ago" : age.TotalDays < 7 ? $"{(int)age.TotalDays}d ago" : entry.LastOpenedUtc.LocalDateTime.ToString("d MMM");
        return entry.PageCount > 0 ? $"{entry.PageCount:N0} pages • opened {when}" : $"Opened {when}";
    }

    private async void RecentCard_Click(object sender, RoutedEventArgs e)
    {
        if (sender is Button { Tag: string path } && File.Exists(path)) await OpenPdfAsync(path);
    }

    private void RecentGridView_Click(object sender, RoutedEventArgs e) => SetRecentView(RecentViewMode.Grid);
    private void RecentListView_Click(object sender, RoutedEventArgs e) => SetRecentView(RecentViewMode.List);
    private void RecentCompactView_Click(object sender, RoutedEventArgs e) => SetRecentView(RecentViewMode.Compact);
    private void RecentSortCombo_SelectionChanged(object sender, SelectionChangedEventArgs e) { if (IsLoaded) RefreshRecentCards(); }

    private void SetRecentView(RecentViewMode mode)
    {
        _recentViewMode = mode;
        _appState.RecentView = mode;
        _stateStore.Save(_appState);
        ApplyRecentViewTemplate();
    }

    private void ApplyRecentViewTemplate()
    {
        if (RecentDocumentsItems is null) return;
        var key = _recentViewMode switch
        {
            RecentViewMode.List => "RecentListTemplate",
            RecentViewMode.Compact => "RecentCompactTemplate",
            _ => "RecentGridTemplate"
        };
        RecentDocumentsItems.ItemTemplate = (DataTemplate)FindResource(key);
    }

    private void RegisterRecentDocument(string path, int pageCount)
    {
        if (!_appState.TrackRecentDocuments) return;
        path = Path.GetFullPath(path);
        var existing = _appState.RecentDocuments.FirstOrDefault(x => string.Equals(Path.GetFullPath(x.Path), path, StringComparison.OrdinalIgnoreCase));
        if (existing is null)
        {
            existing = new RecentDocumentEntry { Path = path };
            _appState.RecentDocuments.Add(existing);
        }
        existing.LastOpenedUtc = DateTimeOffset.UtcNow;
        existing.PageCount = pageCount;
        existing.LastPage = PagesList.SelectedIndex >= 0 ? PagesList.SelectedIndex + 1 : 1;
        existing.PreviewWidth = _previewWidth;
        existing.ThumbnailPath ??= AppStateStore.ThumbnailPathFor(path);
        _appState.RecentDocuments = _appState.RecentDocuments
            .OrderByDescending(x => x.Pinned).ThenByDescending(x => x.LastOpenedUtc).Take(60).ToList();
        _stateStore.Save(_appState);
        RefreshRecentCards();
    }

    private void RegisterDocumentTabAfterOpen(string path)
    {
        var full = Path.GetFullPath(path);
        var session = _documentSessions.FirstOrDefault(x => string.Equals(x.Path, full, StringComparison.OrdinalIgnoreCase));
        if (session is null)
        {
            session = new DocumentSession { Path = full, LastPage = 1, PreviewWidth = _previewWidth };
            _documentSessions.Add(session);
        }
        _activeSession = session;
        session.LastOpenedUtc = DateTimeOffset.UtcNow;
        if (_documentTabViews.All(x => x.Id != session.Id))
            _documentTabViews.Add(new DocumentTabViewModel(session));
        RefreshDocumentTabsVisuals();
        PersistWorkspaceSession();
    }

    private void RefreshDocumentTabsVisuals()
    {
        foreach (var tab in _documentTabViews)
        {
            tab.IsActive = _activeSession?.Id == tab.Id;
            tab.Modified = _documentSessions.FirstOrDefault(x => x.Id == tab.Id)?.Modified == true;
        }
    }

    private void CaptureActiveSessionState()
    {
        if (_activeSession is null || string.IsNullOrWhiteSpace(_activeSession.Path)) return;
        _activeSession.LastPage = Math.Max(1, PagesList.SelectedIndex + 1);
        _activeSession.PreviewWidth = _previewWidth;
        _activeSession.Layout = Pages.Select(x => new SessionPageState(x.SourcePageNumber, x.Rotation)).ToList();
        PersistWorkspaceSession();
        var recent = _appState.RecentDocuments.FirstOrDefault(x => string.Equals(x.Path, _activeSession.Path, StringComparison.OrdinalIgnoreCase));
        if (recent is not null)
        {
            recent.LastPage = _activeSession.LastPage;
            recent.PreviewWidth = _previewWidth;
        }
    }

    private async Task ActivateDocumentSessionAsync(DocumentSession session)
    {
        if (_activeSession?.Id == session.Id && _currentPdf is not null) return;
        CaptureActiveSessionState();
        _activeSession = session;
        _openingFromTabSwitch = true;
        try
        {
            await OpenPdfAsync(session.Path);
            _previewWidth = session.PreviewWidth;
            if (session.Layout.Count > 0)
            {
                Pages.Clear();
                foreach (var state in session.Layout)
                    Pages.Add(new PdfPageItem(state.SourcePageNumber, Pages.Count + 1) { Rotation = state.Rotation, Thumbnail = GetCachedThumbnail(state.SourcePageNumber) });
                Renumber();
            }
            if (Pages.Count > 0)
            {
                var index = Math.Clamp(session.LastPage - 1, 0, Pages.Count - 1);
                PagesList.SelectedIndex = index;
                await RenderPreviewAsync(Pages[index]);
            }
            RefreshDocumentTabsVisuals();
        }
        finally { _openingFromTabSwitch = false; }
    }

    private async void DocumentTab_Click(object sender, RoutedEventArgs e)
    {
        if (sender is not Button { Tag: Guid id }) return;
        var session = _documentSessions.FirstOrDefault(x => x.Id == id);
        if (session is not null) await ActivateDocumentSessionAsync(session);
    }

    private async void CloseDocumentTab_Click(object sender, RoutedEventArgs e)
    {
        e.Handled = true;
        if (sender is not Button { Tag: Guid id }) return;
        var session = _documentSessions.FirstOrDefault(x => x.Id == id);
        if (session is null) return;
        if (!ConfirmCloseSession(session)) return;

        var wasActive = _activeSession?.Id == id;
        _documentSessions.Remove(session);
        var vm = _documentTabViews.FirstOrDefault(x => x.Id == id);
        if (vm is not null) _documentTabViews.Remove(vm);
        if (_secondarySession?.Id == id) CloseSplitView();

        if (wasActive)
        {
            var next = _documentSessions.LastOrDefault();
            if (next is not null) await ActivateDocumentSessionAsync(next);
            else
            {
                _activeSession = null;
                _currentPdf = null;
                Pages.Clear();
                ApplyWorkspaceVisibility();
                RefreshRecentCards();
                UpdateCommandStates();
            }
        }
        PersistWorkspaceSession();
    }

    private bool ConfirmCloseSession(DocumentSession session)
    {
        if (!session.Modified) return true;
        var answer = MessageBox.Show(this,
            $"{Path.GetFileName(session.Path)} has unsaved page changes.\n\nSave a new PDF before closing this tab?",
            "Unsaved changes", MessageBoxButton.YesNoCancel, MessageBoxImage.Warning);
        if (answer == MessageBoxResult.Cancel) return false;
        if (answer == MessageBoxResult.Yes && _activeSession?.Id == session.Id)
        {
            SaveAs_Click(this, new RoutedEventArgs());
            // SaveAs is currently synchronous from the user's perspective until its async handler yields.
            // Keep the tab open if the in-memory layout remains marked modified.
            return !session.Modified;
        }
        return true;
    }

    private void PersistWorkspaceSession()
    {
        _appState.LastSession = _documentSessions
            .Where(x => File.Exists(x.Path))
            .Select(x => new WorkspaceSessionEntry
            {
                Path = x.Path,
                LastPage = x.LastPage,
                PreviewWidth = x.PreviewWidth,
                Modified = x.Modified,
                Layout = x.Layout.Select(p => new WorkspacePageState { SourcePageNumber = p.SourcePageNumber, Rotation = p.Rotation }).ToList()
            }).ToList();
        _stateStore.Save(_appState);
        UpdateResumeSessionButton();
    }

    private void MarkActiveSessionModified()
    {
        if (_activeSession is null) return;
        _activeSession.Modified = true;
        CaptureActiveSessionState();
        RefreshDocumentTabsVisuals();
    }

    private async void PreviousPage_Click(object sender, RoutedEventArgs e)
    {
        if (Pages.Count == 0) return;
        PagesList.SelectedIndex = Math.Max(0, PagesList.SelectedIndex - 1);
        PagesList.ScrollIntoView(PagesList.SelectedItem);
        await Task.CompletedTask;
    }

    private async void NextPage_Click(object sender, RoutedEventArgs e)
    {
        if (Pages.Count == 0) return;
        PagesList.SelectedIndex = Math.Min(Pages.Count - 1, Math.Max(0, PagesList.SelectedIndex) + 1);
        PagesList.ScrollIntoView(PagesList.SelectedItem);
        await Task.CompletedTask;
    }

    private void PageNumberBox_KeyDown(object sender, KeyEventArgs e)
    {
        if (e.Key != Key.Enter || Pages.Count == 0) return;
        if (int.TryParse(PageNumberBox.Text, out var page))
        {
            page = Math.Clamp(page, 1, Pages.Count);
            PagesList.SelectedIndex = page - 1;
            PagesList.ScrollIntoView(PagesList.SelectedItem);
        }
        e.Handled = true;
    }

    private void FitPage_Click(object sender, RoutedEventArgs e)
    {
        if (_currentPdf is null) return;
        var width = PreviewScroll.ViewportWidth > 100 ? PreviewScroll.ViewportWidth - 90 : 900;
        var height = PreviewScroll.ViewportHeight > 100 ? PreviewScroll.ViewportHeight - 90 : 700;
        if (PreviewImage.Source is BitmapSource bitmap && bitmap.PixelHeight > 0)
        {
            var widthByHeight = height * bitmap.PixelWidth / bitmap.PixelHeight;
            _previewWidth = (uint)Math.Clamp((int)Math.Min(width, widthByHeight), 320, 2000);
        }
        else _previewWidth = (uint)Math.Clamp((int)width, 320, 2000);
        _ = RerenderSelectedPageAsync();
    }

    private void ZoomMenu_Click(object sender, RoutedEventArgs e)
    {
        var combo = new ComboBox { ItemsSource = new[] { "50%", "75%", "100%", "125%", "150%", "200%" }, SelectedIndex = 2, MinWidth = 160, Margin = new Thickness(0, 8, 0, 10) };
        var window = BuildPromptWindow("Zoom", "Choose a zoom level.", combo, out var ok);
        ok.Click += (_, _) => window.DialogResult = true;
        if (window.ShowDialog() != true) return;
        var text = combo.SelectedItem?.ToString()?.TrimEnd('%');
        if (int.TryParse(text, out var percent))
        {
            _previewWidth = (uint)Math.Clamp((int)Math.Round(1100 * percent / 100d), 320, 2400);
            _ = RerenderSelectedPageAsync();
        }
    }

    private void PagesRibbon_Click(object sender, RoutedEventArgs e) => OpenButtonContextMenu(sender);
    private void EditRibbon_Click(object sender, RoutedEventArgs e) => OpenButtonContextMenu(sender);
    private void AnnotateRibbon_Click(object sender, RoutedEventArgs e) => OpenButtonContextMenu(sender);
    private void ConvertRibbon_Click(object sender, RoutedEventArgs e) => OpenButtonContextMenu(sender);
    private void ProtectRibbon_Click(object sender, RoutedEventArgs e) => OpenButtonContextMenu(sender);
    private void OptimizeRibbon_Click(object sender, RoutedEventArgs e) => OpenButtonContextMenu(sender);
    private static void OpenButtonContextMenu(object sender)
    {
        if (sender is Button { ContextMenu: { } menu } button)
        {
            menu.PlacementTarget = button;
            menu.IsOpen = true;
        }
    }

    private void PagesSidebar_Click(object sender, RoutedEventArgs e) => ShowSidebar("pages");
    private void BookmarksSidebar_Click(object sender, RoutedEventArgs e) => ShowSidebar("bookmarks");
    private void SearchSidebar_Click(object sender, RoutedEventArgs e) => ShowSidebar("search");
    private void ShowSidebar(string mode)
    {
        PagesList.Visibility = mode == "pages" ? Visibility.Visible : Visibility.Collapsed;
        BookmarksPanel.Visibility = mode == "bookmarks" ? Visibility.Visible : Visibility.Collapsed;
        SearchResultsList.Visibility = mode == "search" ? Visibility.Visible : Visibility.Collapsed;
    }

    private void CommandSearchBox_KeyDown(object sender, KeyEventArgs e)
    {
        if (e.Key != Key.Enter) return;
        var q = CommandSearchBox.Text.Trim();
        if (_currentPdf is not null)
        {
            DocumentSearchBox.Text = q;
            _ = RunDocumentSearchAsync(q);
        }
        else if (q.Contains("ocr", StringComparison.OrdinalIgnoreCase)) OcrPdf_Click(sender, new RoutedEventArgs());
        else if (q.Contains("compress", StringComparison.OrdinalIgnoreCase)) Compress_Click(sender, new RoutedEventArgs());
        else if (q.Contains("merge", StringComparison.OrdinalIgnoreCase)) Merge_Click(sender, new RoutedEventArgs());
        else if (q.Contains("doctor", StringComparison.OrdinalIgnoreCase)) StandaloneDoctor_Click(sender, new RoutedEventArgs());
        else OpenPdf_Click(sender, new RoutedEventArgs());
        e.Handled = true;
    }

    private OcrUiOptions? PromptOcrOptions()
    {
        var range = new ComboBox { MinWidth = 260, Margin = new Thickness(0, 5, 0, 10), ItemsSource = new[] { "All pages", "Current page", "Custom range" }, SelectedIndex = 0 };
        var custom = new TextBox { MinWidth = 260, Margin = new Thickness(0, 0, 0, 10), Text = "1-" + Math.Max(1, Pages.Count), IsEnabled = false };
        range.SelectionChanged += (_, _) => custom.IsEnabled = range.SelectedIndex == 2;
        var quality = new ComboBox { MinWidth = 260, Margin = new Thickness(0, 5, 0, 10), ItemsSource = new[] { "Balanced (recommended)", "High quality", "Maximum quality" }, SelectedIndex = 0 };
        var engineItems = new List<string> { "Automatic local OCR" };
        if (_ocr.IsBundledTesseractAvailable) engineItems.Add("Bundled Tesseract • English");
        var engine = new ComboBox { MinWidth = 260, Margin = new Thickness(0, 5, 0, 10), ItemsSource = engineItems, SelectedIndex = 0 };
        var openResult = new CheckBox { Content = "Offer to open the result in a new tab", IsChecked = true, Margin = new Thickness(0, 5, 0, 12) };
        var panel = new StackPanel();
        panel.Children.Add(new TextBlock { Text = "Pages", FontWeight = FontWeights.SemiBold }); panel.Children.Add(range);
        panel.Children.Add(custom);
        panel.Children.Add(new TextBlock { Text = "OCR engine", FontWeight = FontWeights.SemiBold }); panel.Children.Add(engine);
        panel.Children.Add(new TextBlock { Text = "Output quality", FontWeight = FontWeights.SemiBold }); panel.Children.Add(quality);
        panel.Children.Add(openResult);
        panel.Children.Add(new TextBlock { Text = "The source PDF will never be overwritten. OCR runs locally on this computer.", Foreground = (Brush)Application.Current.Resources["MutedTextBrush"], TextWrapping = TextWrapping.Wrap, FontSize = 11 });
        var window = BuildPromptWindow("OCR PDF", "Choose how AsantePDF should make this document searchable.", panel, out var ok);
        ok.Content = "Run OCR";
        ok.Click += (_, _) =>
        {
            try
            {
                if (range.SelectedIndex == 2) _ = ParsePageRange(custom.Text, Pages.Count);
                window.DialogResult = true;
            }
            catch (Exception ex) { MessageBox.Show(window, ex.Message, "OCR page range", MessageBoxButton.OK, MessageBoxImage.Information); }
        };
        if (window.ShowDialog() != true) return null;
        var pages = range.SelectedIndex switch
        {
            1 => new[] { Math.Max(1, PagesList.SelectedIndex + 1) },
            2 => ParsePageRange(custom.Text, Pages.Count),
            _ => Enumerable.Range(1, Pages.Count).ToArray()
        };
        var width = quality.SelectedIndex switch { 1 => 2100u, 2 => 2600u, _ => 1800u };
        var jpeg = quality.SelectedIndex switch { 1 => 91, 2 => 94, _ => 88 };
        return new OcrUiOptions(pages.ToHashSet(), width, jpeg, engine.SelectedIndex == 1, openResult.IsChecked == true);
    }

    private static int[] ParsePageRange(string text, int pageCount)
    {
        if (pageCount < 1) return [];
        var pages = new SortedSet<int>();
        foreach (var raw in (text ?? string.Empty).Split(',', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries))
        {
            var token = raw.Trim();
            var dash = token.IndexOf('-');
            if (dash < 0)
            {
                if (!int.TryParse(token, out var page) || page < 1 || page > pageCount) throw new ArgumentException($"'{token}' is not a valid page number.");
                pages.Add(page);
                continue;
            }
            var leftText = token[..dash].Trim();
            var rightText = token[(dash + 1)..].Trim();
            var start = string.IsNullOrEmpty(leftText) ? 1 : int.Parse(leftText);
            var end = string.IsNullOrEmpty(rightText) ? pageCount : int.Parse(rightText);
            if (start < 1 || end > pageCount || start > end) throw new ArgumentException($"'{token}' is not a valid page range.");
            for (var page = start; page <= end; page++) pages.Add(page);
        }
        if (pages.Count == 0) throw new ArgumentException("Choose at least one page.");
        return pages.ToArray();
    }

    private sealed record OcrUiOptions(HashSet<int> PagesToOcr, uint RenderWidth, int JpegQuality, bool ForceBundledEnglish, bool OfferOpenResult);

    private async void ConvertLauncher_Click(object sender, RoutedEventArgs e)
    {
        var combo = new ComboBox { MinWidth = 280, Margin = new Thickness(0, 8, 0, 10) };
        combo.ItemsSource = new[] { "Office document to PDF", "PDF to Word", "PDF to Excel", "PDF to PowerPoint", "Images to PDF" };
        combo.SelectedIndex = 0;
        var window = BuildPromptWindow("Convert", "What would you like to convert?", combo, out var ok);
        ok.Click += (_, _) => window.DialogResult = true;
        if (window.ShowDialog() != true) return;
        switch (combo.SelectedIndex)
        {
            case 0: OfficeToPdf_Click(sender, new RoutedEventArgs()); break;
            case 1: await EnsureDocumentForStandaloneToolAsync(); if (_currentPdf is not null) PdfToWord_Click(sender, new RoutedEventArgs()); break;
            case 2: await EnsureDocumentForStandaloneToolAsync(); if (_currentPdf is not null) PdfToExcel_Click(sender, new RoutedEventArgs()); break;
            case 3: await EnsureDocumentForStandaloneToolAsync(); if (_currentPdf is not null) PdfToPowerPoint_Click(sender, new RoutedEventArgs()); break;
            case 4: ImagesToPdf_Click(sender, new RoutedEventArgs()); break;
        }
    }

    private async void StandaloneSplit_Click(object sender, RoutedEventArgs e)
    {
        if (await EnsureDocumentForStandaloneToolAsync()) Split_Click(sender, new RoutedEventArgs());
    }

    private async void StandaloneDoctor_Click(object sender, RoutedEventArgs e)
    {
        if (await EnsureDocumentForStandaloneToolAsync()) Doctor_Click(sender, new RoutedEventArgs());
    }

    private async Task<bool> EnsureDocumentForStandaloneToolAsync()
    {
        if (_currentPdf is not null) return true;
        var dialog = new OpenFileDialog { Title = "Choose a PDF", Filter = "PDF files (*.pdf)|*.pdf", CheckFileExists = true };
        if (dialog.ShowDialog(this) != true) return false;
        await OpenPdfAsync(dialog.FileName);
        return _currentPdf is not null;
    }

    private async Task ShowCompletionAsync(string title, string outputPath, bool openAsPdf)
    {
        if (string.IsNullOrWhiteSpace(outputPath) || !File.Exists(outputPath)) return;
        var window = new Window
        {
            Title = title, Owner = this, Width = 520, SizeToContent = SizeToContent.Height,
            WindowStartupLocation = WindowStartupLocation.CenterOwner, ResizeMode = ResizeMode.NoResize,
            Background = (Brush)Application.Current.Resources["PanelBackground"], ShowInTaskbar = false
        };
        var root = new StackPanel { Margin = new Thickness(22) };
        root.Children.Add(new TextBlock { Text = "✓", FontSize = 30, Foreground = (Brush)Application.Current.Resources["SuccessBrush"], FontWeight = FontWeights.Bold });
        root.Children.Add(new TextBlock { Text = title, FontSize = 20, FontWeight = FontWeights.SemiBold, Margin = new Thickness(0, 8, 0, 0) });
        root.Children.Add(new TextBlock { Text = Path.GetFileName(outputPath), Foreground = (Brush)Application.Current.Resources["MutedTextBrush"], Margin = new Thickness(0, 5, 0, 4), TextWrapping = TextWrapping.Wrap });
        root.Children.Add(new TextBlock { Text = outputPath, Foreground = (Brush)Application.Current.Resources["SubtleTextBrush"], FontSize = 10, TextWrapping = TextWrapping.Wrap, Margin = new Thickness(0, 0, 0, 18) });
        var actions = new WrapPanel { HorizontalAlignment = HorizontalAlignment.Right };
        if (openAsPdf && string.Equals(Path.GetExtension(outputPath), ".pdf", StringComparison.OrdinalIgnoreCase))
        {
            var open = new Button { Content = "Open in new tab", MinWidth = 130, Margin = new Thickness(4, 0, 0, 0) };
            open.Click += (_, _) => window.DialogResult = true;
            actions.Children.Add(open);
        }
        var folder = new Button { Content = "Open containing folder", MinWidth = 145, Margin = new Thickness(4, 0, 0, 0) };
        folder.Click += (_, _) =>
        {
            try { Process.Start(new ProcessStartInfo("explorer.exe", $"/select,\"{outputPath}\"") { UseShellExecute = true }); } catch { }
        };
        actions.Children.Add(folder);
        var done = new Button { Content = "Done", IsDefault = true, MinWidth = 85, Margin = new Thickness(4, 0, 0, 0) };
        done.Click += (_, _) => window.DialogResult = false;
        actions.Children.Add(done);
        root.Children.Add(actions);
        window.Content = root;
        var result = window.ShowDialog();
        if (result == true) await OpenPdfAsync(outputPath);
    }

    private void MinimizeTask_Click(object sender, RoutedEventArgs e)
    {
        _taskMinimized = true;
        TaskOverlay.Visibility = Visibility.Collapsed;
        StatusText.Text = TaskStageText.Text;
    }

    private void BeginTaskPresentation(string title)
    {
        _taskMinimized = false;
        TaskTitleText.Text = HumanizeTaskTitle(title);
        TaskStageText.Text = title.TrimEnd('.');
        TaskPercentText.Text = string.Empty;
        TaskElapsedText.Text = string.Empty;
        TaskProgressBar.IsIndeterminate = true;
        TaskProgressBar.Value = 0;
        TaskCancelButton.IsEnabled = true;
        TaskOverlay.Visibility = Visibility.Visible;
        _taskStopwatch.Restart();
    }

    private void EndTaskPresentation()
    {
        _taskStopwatch.Stop();
        TaskOverlay.Visibility = Visibility.Collapsed;
        _taskMinimized = false;
    }

    private static string HumanizeTaskTitle(string status)
    {
        var text = status.Trim().TrimEnd('.');
        return string.IsNullOrWhiteSpace(text) ? "Working" : text;
    }

    private void UpdateTaskPresentation(int completed, int total, string status)
    {
        TaskStageText.Text = status;
        TaskProgressBar.IsIndeterminate = false;
        TaskProgressBar.Minimum = 0;
        TaskProgressBar.Maximum = Math.Max(1, total);
        TaskProgressBar.Value = Math.Clamp(completed, 0, Math.Max(1, total));
        TaskPercentText.Text = total > 0 ? $"{Math.Clamp((int)Math.Round(completed * 100d / total), 0, 100)}%" : string.Empty;
        if (_taskMinimized) StatusText.Text = status;
    }

    private async void SplitView_Click(object sender, RoutedEventArgs e)
    {
        if (_documentSessions.Count < 2)
        {
            MessageBox.Show(this, "Open at least two PDFs to compare them side by side.", "AsantePDF", MessageBoxButton.OK, MessageBoxImage.Information);
            return;
        }
        var candidates = _documentSessions.Where(x => x.Id != _activeSession?.Id).ToArray();
        var combo = new ComboBox { ItemsSource = candidates.Select(x => Path.GetFileName(x.Path)).ToArray(), SelectedIndex = 0, MinWidth = 300, Margin = new Thickness(0, 8, 0, 10) };
        var window = BuildPromptWindow("Side by side", "Choose the PDF to show beside the current document.", combo, out var ok);
        ok.Click += (_, _) => window.DialogResult = true;
        if (window.ShowDialog() != true || combo.SelectedIndex < 0) return;
        await OpenSplitViewAsync(candidates[combo.SelectedIndex]);
    }

    private async Task OpenSplitViewAsync(DocumentSession session)
    {
        CloseSplitView();
        try
        {
            _secondaryRenderer = PdfRendererFactory.CreateProduction();
            await _secondaryRenderer.OpenAsync(session.Path, _lifetime.Token);
            _secondarySession = session;
            SplitViewerColumn.Width = new GridLength(1, GridUnitType.Star);
            SplitDividerColumn.Width = new GridLength(5);
            SplitDivider.Visibility = Visibility.Visible;
            SplitViewerPanel.Visibility = Visibility.Visible;
            SplitDocumentTitle.Text = Path.GetFileName(session.Path);
            var page = Math.Clamp(session.LastPage, 1, checked((int)_secondaryRenderer.PageCount));
            SecondaryPreviewImage.Source = await _secondaryRenderer.RenderAsync((uint)page, session.PreviewWidth, _lifetime.Token);
        }
        catch (Exception ex)
        {
            App.Log("Split view failed: " + ex);
            CloseSplitView();
            MessageBox.Show(this, ex.Message, "AsantePDF side-by-side view", MessageBoxButton.OK, MessageBoxImage.Warning);
        }
    }

    private void CloseSplitView_Click(object sender, RoutedEventArgs e) => CloseSplitView();
    private void CloseSplitView()
    {
        _secondaryRenderer?.Dispose();
        _secondaryRenderer = null;
        _secondarySession = null;
        SecondaryPreviewImage.Source = null;
        SplitViewerPanel.Visibility = Visibility.Collapsed;
        SplitDivider.Visibility = Visibility.Collapsed;
        SplitViewerColumn.Width = new GridLength(0);
        SplitDividerColumn.Width = new GridLength(0);
    }

    private void PreviewScroll_ScrollChanged(object sender, ScrollChangedEventArgs e)
    {
        if (_syncingScroll || SyncScrollCheckBox.IsChecked != true || SplitViewerPanel.Visibility != Visibility.Visible) return;
        try
        {
            _syncingScroll = true;
            if (PreviewScroll.ScrollableHeight > 0 && SecondaryPreviewScroll.ScrollableHeight > 0)
                SecondaryPreviewScroll.ScrollToVerticalOffset(PreviewScroll.VerticalOffset / PreviewScroll.ScrollableHeight * SecondaryPreviewScroll.ScrollableHeight);
        }
        finally { _syncingScroll = false; }
    }

    private void SecondaryPreviewScroll_ScrollChanged(object sender, ScrollChangedEventArgs e)
    {
        if (_syncingScroll || SyncScrollCheckBox.IsChecked != true || SplitViewerPanel.Visibility != Visibility.Visible) return;
        try
        {
            _syncingScroll = true;
            if (SecondaryPreviewScroll.ScrollableHeight > 0 && PreviewScroll.ScrollableHeight > 0)
                PreviewScroll.ScrollToVerticalOffset(SecondaryPreviewScroll.VerticalOffset / SecondaryPreviewScroll.ScrollableHeight * PreviewScroll.ScrollableHeight);
        }
        finally { _syncingScroll = false; }
    }

    private void Window_Closing(object? sender, CancelEventArgs e)
    {
        if (_closingAccepted) return;
        CaptureActiveSessionState();
        foreach (var session in _documentSessions.Where(x => x.Modified).ToArray())
        {
            var answer = MessageBox.Show(this,
                $"{Path.GetFileName(session.Path)} has unsaved page changes. Close AsantePDF and keep the recoverable session state?",
                "Unsaved changes", MessageBoxButton.YesNoCancel, MessageBoxImage.Warning);
            if (answer == MessageBoxResult.Cancel) { e.Cancel = true; return; }
            if (answer == MessageBoxResult.No)
            {
                session.Modified = false;
                session.Layout.Clear();
            }
        }
        PersistWorkspaceSession();
        _closingAccepted = true;
    }

    private sealed class RecentDocumentCardViewModel : INotifyPropertyChanged
    {
        private BitmapSource? _thumbnail;
        private string _meta;
        public RecentDocumentCardViewModel(RecentDocumentEntry entry)
        {
            Path = entry.Path;
            FileName = System.IO.Path.GetFileName(entry.Path);
            _meta = BuildRecentMeta(entry);
            ResumeText = entry.LastPage > 1 ? $"Resume at page {entry.LastPage:N0}" : "Open document";
        }
        public string Path { get; }
        public string FileName { get; }
        public string ResumeText { get; }
        public string Meta { get => _meta; set { _meta = value; Changed(); } }
        public BitmapSource? Thumbnail { get => _thumbnail; set { _thumbnail = value; Changed(); } }
        public event PropertyChangedEventHandler? PropertyChanged;
        private void Changed([CallerMemberName] string? name = null) => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
    }

    private sealed class DocumentTabViewModel : INotifyPropertyChanged
    {
        private bool _isActive;
        private bool _modified;
        public DocumentTabViewModel(DocumentSession session) { Id = session.Id; FileName = Path.GetFileName(session.Path); }
        public Guid Id { get; }
        public string FileName { get; }
        public bool IsActive { get => _isActive; set { _isActive = value; Changed(nameof(Background)); } }
        public bool Modified { get => _modified; set { _modified = value; Changed(nameof(ModifiedVisibility)); } }
        public Brush Background => (Brush)Application.Current.Resources[IsActive ? "SelectionBrush" : "PanelBackground"];
        public Visibility ModifiedVisibility => Modified ? Visibility.Visible : Visibility.Collapsed;
        public event PropertyChangedEventHandler? PropertyChanged;
        private void Changed([CallerMemberName] string? name = null) => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
    }

    private sealed class DocumentSession
    {
        public Guid Id { get; } = Guid.NewGuid();
        public string Path { get; set; } = string.Empty;
        public int LastPage { get; set; } = 1;
        public uint PreviewWidth { get; set; } = 1100;
        public bool Modified { get; set; }
        public DateTimeOffset LastOpenedUtc { get; set; } = DateTimeOffset.UtcNow;
        public List<SessionPageState> Layout { get; set; } = [];
    }

    private sealed record SessionPageState(int SourcePageNumber, int Rotation);
}
