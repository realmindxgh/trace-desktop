param([Parameter(Mandatory=$true)][string]$Root)
$ErrorActionPreference = 'Stop'

function Replace-Exact([string]$Path,[string]$Old,[string]$New) {
    $text = Get-Content $Path -Raw
    if (-not $text.Contains($Old)) { throw "Expected compiler-fix text not found in $Path`n$Old" }
    $text = $text.Replace($Old,$New)
    Set-Content -Path $Path -Value $text -Encoding UTF8
}

$appState = Join-Path $Root 'src\PdfRescue.App\Services\AppStateStore.cs'
$text = Get-Content $appState -Raw
if ($text -notmatch '(?m)^using System\.IO;\s*$') {
    $text = "using System.IO;`r`n" + $text
    Set-Content -Path $appState -Value $text -Encoding UTF8
}

$renderer = Join-Path $Root 'src\PdfRescue.App\PdfiumPdfRenderer.cs'
Replace-Exact $renderer `
    'if (!fpdf_text.FPDFTextGetCharBox(textPage, i, ref left, ref right, ref bottom, ref top)) continue;' `
    'if (fpdf_text.FPDFTextGetCharBox(textPage, i, ref left, ref right, ref bottom, ref top) == 0) continue;'

$workspace = Join-Path $Root 'src\PdfRescue.App\ModernWorkspace.cs'
Replace-Exact $workspace `
    'SecondaryPreviewImage.Source = await _secondaryRenderer.RenderAsync((uint)page, session.PreviewWidth, _lifetime.Token);' `
    'SecondaryPreviewImage.Source = await _secondaryRenderer.RenderAsync(page, session.PreviewWidth, _lifetime.Token);'

$textSearch = Join-Path $Root 'src\PdfRescue.App\TextSearchSelection.cs'
$text = Get-Content $textSearch -Raw
if ($text -notmatch '(?m)^using System\.IO;\s*$') {
    $text = "using System.IO;`r`nusing IOPath = System.IO.Path;`r`n" + $text
} elseif ($text -notmatch 'using IOPath = System\.IO\.Path;') {
    $text = $text -replace '(?m)^using System\.IO;\s*$', "using System.IO;`r`nusing IOPath = System.IO.Path;"
}
$text = $text.Replace('Path.Combine(Path.GetTempPath(), "AsantePDF", "text-highlight", Guid.NewGuid().ToString("N"))','IOPath.Combine(IOPath.GetTempPath(), "AsantePDF", "text-highlight", Guid.NewGuid().ToString("N"))')
$text = $text.Replace('Path.Combine(tempDir, $"step-{i:000}.pdf")','IOPath.Combine(tempDir, $"step-{i:000}.pdf")')
Set-Content -Path $textSearch -Value $text -Encoding UTF8

Write-Host 'AsantePDF compiler fix 6 applied.' -ForegroundColor Green

$fix7 = Join-Path (Split-Path -Parent $PSScriptRoot) 'asantepdf-fix7\apply-fix7.ps1'
if (-not (Test-Path $fix7)) { throw "AsantePDF fix 7 script not found: $fix7" }
& $fix7 -Root $Root
