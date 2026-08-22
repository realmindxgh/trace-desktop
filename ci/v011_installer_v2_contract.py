from pathlib import Path
import json, re, sys

root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
app=(root/'setup-shell/src/app.js').read_text(encoding='utf-8')
css=(root/'setup-shell/src/styles.css').read_text(encoding='utf-8')
main=(root/'setup-shell/src-tauri/src/main.rs').read_text(encoding='utf-8')
conf=json.loads((root/'setup-shell/src-tauri/tauri.conf.json').read_text(encoding='utf-8'))
cap=json.loads((root/'setup-shell/src-tauri/capabilities/default.json').read_text(encoding='utf-8'))
package=json.loads((root/'setup-shell/package.json').read_text(encoding='utf-8'))
cargo=(root/'setup-shell/src-tauri/Cargo.toml').read_text(encoding='utf-8')

assert '0.9.0' not in app, 'stale 0.9.0 remains in setup UI'
assert "bridge.invoke('setup_version')" in app, 'UI version is not sourced from native package version'
assert 'core:event:default' in cap.get('permissions',[]), 'Tauri event listen ACL permission missing'
assert cap.get('windows')==['main'], 'setup capability must be scoped to main window'
assert 'async function listenForProgress()' in app and 'console.warn' in app, 'progress event listener must fail open'
assert 'unlisten=await listenForProgress()' in app, 'GUI install path must use guarded progress listener'
assert "await bridge.invoke('install_trace'" in app, 'GUI does not invoke install_trace'
assert 'fn perform_install(' in main and 'perform_install(Some(&app),options)' in main, 'GUI install is not routed through shared implementation'
assert 'fn perform_uninstall(' in main and 'perform_uninstall(Some(&app),install_dir)' in main, 'GUI uninstall is not routed through shared implementation'
assert 'fn ci_gui_request()' in main and 'fn ci_gui_result(' in main, 'real WebView CI GUI path hook missing'
assert "bridge.invoke('ci_gui_request')" in app and 'state.ciGui' in app, 'frontend GUI-path CI hook missing'
assert 'state.ciGui.install_dir' in app or 'state.ciGui?.install_dir' in app, 'CI GUI hook must consume Rust install_dir instead of relying only on camelCase'
assert "document.querySelector('#next')?.click()" in app, 'CI GUI path must click the real primary installer button'
assert '.setup-main' in css and 'grid-template-rows:1fr 66px' in css, 'footer must be part of layout, not a floating overlay'
assert '.setup-stage' in css and 'overflow:hidden' in css, 'installer stage must not use browser scrolling'
assert 'position:absolute' not in re.search(r'\.setup-dock\{([^}]*)\}',css).group(1), 'setup footer still floats over content'
assert 'theme-toggle' not in app, 'installer theme toggle should not be exposed'
assert 'AI only when invited' not in app, 'installer welcome should not advertise unrelated AI setting'
assert conf['app']['windows'][0]['width']==960 and conf['app']['windows'][0]['height']==620, 'installer v2 window geometry mismatch'
assert package['version']=='0.11.0' and conf['version']=='0.11.0', 'setup manifest version mismatch'
m=re.search(r'^version\s*=\s*"([^"]+)"',cargo,re.M)
assert m and m.group(1)=='0.11.0', 'setup Cargo version mismatch'
print('Trace v0.11 installer v2 contract OK')
