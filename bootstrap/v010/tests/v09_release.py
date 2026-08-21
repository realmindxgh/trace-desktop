from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]

# Version alignment across app and branded setup shell.
for path in ['package.json','src-tauri/tauri.conf.json','setup-shell/package.json','setup-shell/src-tauri/tauri.conf.json']:
    obj=json.loads((ROOT/path).read_text(encoding='utf-8'))
    assert obj['version']=='0.10.0', (path,obj.get('version'))

# Branded maintenance installer can update/repair or uninstall, but preserves research data.
setup=(ROOT/'setup-shell/src-tauri/src/main.rs').read_text(encoding='utf-8')
for token in ['uninstall_trace','find_uninstaller','projects_preserved','open_setup_log','arg("/S")','Trace.exe']:
    assert token in setup,token
installer=(ROOT/'setup-shell/src/app.js').read_text(encoding='utf-8')
for phrase in ['Update or repair','Uninstall Trace','Your research projects stay put.','Research projects','Preserve','Trace leaves. Your work stays.']:
    assert phrase in installer,phrase
assert "state.action==='uninstall'" in installer
css=(ROOT/'setup-shell/src/styles.css').read_text(encoding='utf-8')
for token in ['.maintenance-choice','.maintenance-card','.preserve-card','.preserve-inline',':root[data-theme="dark"] .setup-dock{background:#fff']:
    assert token in css,token

# Support diagnostics must be privacy-safe by construction.
diag=(ROOT/'src-tauri/src/diagnostics.rs').read_text(encoding='utf-8')
for token in ['raw_source_text_included','source_files_included','coded_quotations_included','participant_attribute_values_included','PRAGMA integrity_check','diagnostic.json']:
    assert token in diag,token
for explicit_false in ['"raw_source_text_included": false','"source_files_included": false','"coded_quotations_included": false','"participant_attribute_values_included": false']:
    assert explicit_false in diag,explicit_false
assert 'plain_text' not in diag
assert 'exact_text' not in diag

app=(ROOT/'src/app.js').read_text(encoding='utf-8')
for token in ['openAppSettings','export_diagnostic_bundle','Privacy-safe diagnostics','release_channel_status','Release infrastructure pending']:
    assert token in app,token

# Release workflow supports optional Authenticode without committing a certificate.
workflow=(ROOT/'.github/workflows/windows-build.yml').read_text(encoding='utf-8')
for token in ['WINDOWS_CERTIFICATE_BASE64','Import-PfxCertificate','prepare_windows_signing.py','signtool','Get-AuthenticodeSignature','v09_release.py']:
    assert token in workflow,token
sign_script=(ROOT/'scripts/prepare_windows_signing.py').read_text(encoding='utf-8')
assert 'certificateThumbprint' in sign_script
assert 'WINDOWS_CERTIFICATE_PASSWORD' not in sign_script
assert not re.search(r'BEGIN (RSA )?PRIVATE KEY',sign_script)

security=(ROOT/'docs/RELEASE-SECURITY.md').read_text(encoding='utf-8')
for phrase in ['Authenticode','updater private key','Research projects','public release']:
    assert phrase.lower() in security.lower(),phrase

print('v0.9 maintenance, diagnostics, and release-security checks passed')
