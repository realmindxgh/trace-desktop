param(
    [Parameter(Mandatory = $true)]
    [string]$Root
)

$ErrorActionPreference = 'Stop'
$xamlPath = Join-Path $Root 'src\PdfRescue.App\MainWindow.xaml'
if (-not (Test-Path $xamlPath)) { throw "MainWindow.xaml was not found at $xamlPath" }

$xaml = Get-Content $xamlPath -Raw
$before = $xaml

# WPF defers DataTemplate content inside Window.Resources. Static Style references inside
# those templates can trip ResourceDictionary.DeferrableContent during MainWindow startup.
# Resolve command/control styles dynamically instead. This also makes theme switching safer.
$xaml = [regex]::Replace(
    $xaml,
    'Style="\{StaticResource\s+([^}]+)\}"',
    'Style="{DynamicResource $1}"')

if ($xaml -eq $before) { throw 'Fix 7 did not find any StaticResource Style references to harden.' }
if ($xaml -match 'Style="\{StaticResource\s+') { throw 'StaticResource Style references remain after Fix 7.' }

Set-Content $xamlPath $xaml -Encoding UTF8
Write-Host 'AsantePDF WPF startup resource fix 7 applied.' -ForegroundColor Green
