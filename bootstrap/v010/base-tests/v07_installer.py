from pathlib import Path
import json, sqlite3, tempfile
ROOT=Path(__file__).resolve().parents[1]

conf=json.loads((ROOT/'src-tauri/tauri.conf.json').read_text())
assert conf['version']=='0.9.0'
assert any('trace' in x.get('ext',[]) for x in conf['bundle']['fileAssociations'])

setup=(ROOT/'setup-shell/src-tauri/src/main.rs').read_text()
for token in ['setup_preflight','REQUIRED_FREE_BYTES','INSTALLING','configure_desktop_shortcut','TraceSetup.log','cmd.arg("/S")','cmd.arg(format!("/D={target}"))']:
    assert token in setup,token
assert 'cmd.arg("/NS")' not in setup
assert 'cmd.arg("/R")' not in setup
assert 'if INSTALLING.load' in setup

installer_js=(ROOT/'setup-shell/src/app.js').read_text()
for phrase in ['Ready to update','Retry','Create a desktop shortcut','recovered' if False else 'Update / repair Trace','setup_preflight']:
    assert phrase in installer_js,phrase
css=(ROOT/'setup-shell/src/styles.css').read_text()
for token in ['.preflight-card','.existing-card',':root[data-theme="dark"] .setup-dock{background:#fff']:
    assert token in css,token

schema=(ROOT/'database/schema.sql').read_text()
for table in ['action_history','workspace_state']:
    assert f'CREATE TABLE IF NOT EXISTS {table}' in schema
with tempfile.NamedTemporaryFile(suffix='.sqlite') as f:
    c=sqlite3.connect(f.name);c.executescript(schema)
    names={r[0] for r in c.execute("select name from sqlite_master where type='table'")}
    assert {'action_history','workspace_state'} <= names

rust=(ROOT/'src-tauri/src/db.rs').read_text()
for fn in ['record_action','undo_last_action','redo_last_action','begin_project_session','heartbeat_project_session','end_project_session']:
    assert f'fn {fn}' in rust or f'pub fn {fn}' in rust,fn
lib=(ROOT/'src-tauri/src/lib.rs').read_text()
for command in ['action_availability','undo_last_action','redo_last_action','begin_project_session','heartbeat_project_session','end_project_session']:
    assert command in lib,command
app=(ROOT/'src/app.js').read_text()
for token in ['openProjectSwitcher','undoResearchAction','redoResearchAction','beginNativeSession','recovery-banner','project-switch']:
    assert token in app,token
print('v0.9 release-hardening contract checks passed')
