from pathlib import Path

app_path=Path('src/app.js')
css_path=Path('src/styles.css')
test_path=Path('tests/ux_foundation_v2_contract.py')
app=app_path.read_text(encoding='utf-8')

old="window.addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'){e.preventDefault();openCommandPalette();return}if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='f'){e.preventDefault();focusContextSearch();}});"
new=r'''function moveSourceTab(delta){
  const ids=(state.openSourceTabs||[]).filter(id=>state.importedSources.some(s=>s.id===id));
  if(!ids.length)return;
  let ix=Math.max(0,ids.indexOf(state.activeSourceId));
  ix=(ix+delta+ids.length)%ids.length;
  state.activeSection='Code';activateSource(ids[ix]);
}
window.addEventListener('keydown',e=>{
  const mod=e.ctrlKey||e.metaKey,key=e.key.toLowerCase();
  if(mod&&key==='k'){e.preventDefault();openCommandPalette();return}
  if(mod&&key==='f'){e.preventDefault();focusContextSearch();return}
  if(mod&&e.shiftKey&&key==='c'){e.preventDefault();openCodeEditor();return}
  if(mod&&e.shiftKey&&key==='m'){e.preventDefault();openMemoEditor();return}
  if(mod&&e.shiftKey&&key==='i'){e.preventDefault();openImporter();return}
  if(e.altKey&&e.key==='ArrowRight'){e.preventDefault();moveSourceTab(1);return}
  if(e.altKey&&e.key==='ArrowLeft'){e.preventDefault();moveSourceTab(-1);return}
  if(mod&&key==='z'&&!e.shiftKey&&nativeBridge.available){e.preventDefault();undoResearchAction();return}
  if(mod&&(key==='y'||(key==='z'&&e.shiftKey))&&nativeBridge.available){e.preventDefault();redoResearchAction();return}
});'''
if old in app:
    app=app.replace(old,new,1)
elif 'function moveSourceTab(delta)' not in app:
    raise SystemExit('Could not locate global keyboard shortcut handler')

old_commands="const root=document.querySelector('#modal-root');const commands=[['Import source','import'],['Create code','code'],['New memo','memo'],['Search this workspace','search'],['Project settings','project-settings'],['Backup project','backup'],['Open Trace Home','home'],['Trace AI','ai']];"
new_commands="const root=document.querySelector('#modal-root');const commands=[['Import source','import','Ctrl+Shift+I'],['Create code','code','Ctrl+Shift+C'],['New memo','memo','Ctrl+Shift+M'],['Search this workspace','search','Ctrl+F'],['Project settings','project-settings',''],['Backup project','backup',''],['Open Trace Home','home',''],['Trace AI','ai','']];"
if old_commands in app:
    app=app.replace(old_commands,new_commands,1)

old_map="${commands.map(([label,id])=>`<button data-command=\"${id}\"><span>${escapeHtml(label)}</span></button>`).join('')}"
new_map="${commands.map(([label,id,shortcut])=>`<button data-command=\"${id}\"><span>${escapeHtml(label)}</span>${shortcut?`<kbd>${escapeHtml(shortcut)}</kbd>`:''}</button>`).join('')}"
if old_map in app:
    app=app.replace(old_map,new_map,1)

app_path.write_text(app,encoding='utf-8')
css=css_path.read_text(encoding='utf-8')
if '/* UX_V2_PHASE7_SHORTCUTS */' not in css:
    css += '\n/* UX_V2_PHASE7_SHORTCUTS */\n.command-list button{display:flex!important;align-items:center;justify-content:space-between;gap:18px}.command-list kbd{font-size:12px;color:var(--muted);font-family:inherit;border:1px solid var(--line);border-radius:5px;padding:2px 6px;background:var(--panel2)}\n'
    css_path.write_text(css,encoding='utf-8')

test=test_path.read_text(encoding='utf-8')
for assertion in [
    "assert 'function moveSourceTab(delta)' in app\n",
    "assert \"key==='c'\" in app\n",
    "assert 'UX_V2_PHASE7_SHORTCUTS' in css\n",
]:
    if assertion not in test:
        test+='\n'+assertion
test_path.write_text(test,encoding='utf-8')
print('Phase 7 keyboard productivity hotfix applied')
