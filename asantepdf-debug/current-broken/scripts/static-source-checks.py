#!/usr/bin/env python3
from __future__ import annotations
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / 'src' / 'PdfRescue.App'
errors: list[str] = []

for project in ROOT.rglob('*.csproj'):
    try:
        ET.parse(project)
    except Exception as exc:
        errors.append(f'Invalid project XML {project.relative_to(ROOT)}: {exc}')

xaml_files = list(APP.glob('*.xaml'))
resource_keys: set[str] = set()
resource_refs: list[tuple[Path, str]] = []
for xaml in xaml_files:
    text = xaml.read_text(encoding='utf-8')
    try:
        ET.fromstring(text)
    except Exception as exc:
        errors.append(f'Invalid XAML XML {xaml.relative_to(ROOT)}: {exc}')
    resource_keys.update(re.findall(r'x:Key="([^"]+)"', text))
    resource_refs.extend((xaml, key) for key in re.findall(r'StaticResource\s+([^}\s]+)', text))

for xaml, key in resource_refs:
    if key not in resource_keys:
        errors.append(f'Missing StaticResource {key} used by {xaml.relative_to(ROOT)}')

main_xaml = (APP / 'MainWindow.xaml').read_text(encoding='utf-8')
main_cs = '\n'.join(path.read_text(encoding='utf-8') for path in APP.glob('*.cs'))
handler_attrs = ('Click','SelectionChanged','DragOver','Drop','PreviewKeyDown','PreviewMouseLeftButtonDown',
                 'PreviewMouseMove','MouseLeftButtonDown','MouseMove','MouseLeftButtonUp','KeyDown','Closing',
                 'ScrollChanged','ContextMenuOpening','MouseDoubleClick')
handlers: set[str] = set()
for attr in handler_attrs:
    handlers.update(re.findall(fr'(?<![A-Za-z0-9_]){attr}="([A-Za-z_][A-Za-z0-9_]*)"', main_xaml))
for handler in sorted(handlers):
    if not re.search(fr'\b{re.escape(handler)}\s*\(', main_cs):
        errors.append(f'XAML handler has no code-behind method: {handler}')

icon = ROOT / 'assets' / 'asantepdf.ico'
if not icon.exists() or icon.stat().st_size < 1000:
    errors.append('assets/asantepdf.ico is missing or invalid.')



workflow = (ROOT / '.github' / 'workflows' / 'windows-release.yml').read_text(encoding='utf-8')
if 'cache: true' in workflow and 'packages.lock.json' not in workflow:
    errors.append('setup-dotnet cache is enabled without a packages.lock.json dependency path; the action will fail before build.')
if 'global-json-file: global.json' not in workflow:
    errors.append('Windows release workflow must use checked-in global.json for the pinned .NET SDK.')

final_gate = (APP / 'Services' / 'FinalCandidateSelfTest.cs').read_text(encoding='utf-8')
for required_gate in (
    'ConversionSelfTest.RunAsync', 'FinishingSelfTest.RunAsync', 'MarkupSelfTest.RunAsync',
    'FormsBatchSelfTest.RunAsync', 'PermanentRedactAsync', 'RecognizeWithBundledTesseractAsync',
    'MergeAsync', 'SplitAsync', 'ProtectAsync', 'DecryptAsync'):
    if required_gate not in final_gate:
        errors.append(f'Final candidate gate is missing required release exercise: {required_gate}')

# Guard against known PDFsharp 6.2 form API mismatches that were present in the RC2 archive.
form_service = (APP / 'Services' / 'PdfFormService.cs').read_text(encoding='utf-8')
if 'PdfSharp.Pdf.AcroForms' in form_service:
    errors.append('PdfFormService uses obsolete/nonexistent PdfSharp.Pdf.AcroForms namespace; use PdfSharp.Pdf.OldAcroForms.')
if 'PdfAcroField' in form_service:
    errors.append('PdfFormService uses nonexistent PdfAcroField base type; current PDFsharp uses PdfFormField.')
if 'PdfSharp.Pdf.OldAcroForms' not in form_service or 'PdfFormField' not in form_service:
    errors.append('PdfFormService is missing the current PDFsharp OldAcroForms/PdfFormField API surface.')

required = [
    APP / 'IPdfRenderer.cs',
    APP / 'PdfiumPdfRenderer.cs',
    APP / 'Services' / 'PdfFinishingService.cs',
    APP / 'Services' / 'PdfFormService.cs',
    APP / 'Services' / 'FinalCandidateSelfTest.cs',
    ROOT / 'installer' / 'PdfRescue.iss',
]
for path in required:
    if not path.exists():
        errors.append(f'Required release source is missing: {path.relative_to(ROOT)}')

# Guard the new product UX contract. Home must be the no-document surface; premium/upgrade UI is forbidden.
for forbidden in ('Unlock Premium', 'Upgrade to Premium', 'Subscribe now'):
    if forbidden.lower() in main_xaml.lower():
        errors.append(f'Forbidden paid-tier UI is present: {forbidden}')
if 'x:Name="HomeView"' not in main_xaml or 'x:Name="WorkspaceView"' not in main_xaml:
    errors.append('MainWindow must contain separate HomeView and WorkspaceView surfaces.')
if 'x:Name="ThemeToggleButton"' not in main_xaml:
    errors.append('Visible theme toggle is missing.')
if 'x:Name="DocumentTabsItems"' not in main_xaml:
    errors.append('Tabbed document workspace is missing.')
if 'x:Name="TaskOverlay"' not in main_xaml:
    errors.append('Shared task/progress overlay is missing.')
installer_text = (ROOT / 'installer' / 'PdfRescue.iss').read_text(encoding='utf-8')
if 'Name: "openwith"' in installer_text or 'Tasks: openwith' in installer_text:
    errors.append('PDF Open With integration must be mandatory, not an installer task.')
if 'RestartIfNeededByRun=no' not in installer_text:
    errors.append('Installer must suppress avoidable restart prompts.')
if 'AsantePDF Setup' not in installer_text:
    errors.append('Installer has not been rebranded to AsantePDF.')

if errors:
    print('AsantePDF static source checks FAILED')
    for error in errors:
        print(f' - {error}')
    sys.exit(1)

print(f'AsantePDF static source checks passed. {len(handlers)} XAML handlers checked, '
      f'{len(resource_refs)} StaticResource uses checked, {len(list(ROOT.rglob("*.csproj")))} projects parsed.')
