from pathlib import Path

app_path=Path('src/app.js')
css_path=Path('src/styles.css')
contract_path=Path('tests/ux_foundation_v2_contract.py')
browser_path=Path('tests/ux_foundation_v2.mjs')
app=app_path.read_text(encoding='utf-8')
css=css_path.read_text(encoding='utf-8')
contract=contract_path.read_text(encoding='utf-8')

start=app.find('async function importFiles(files){')
end=app.find('\nasync function importOneFile(f){', start)
if start<0 or end<0: raise SystemExit('importFiles boundaries changed')
new_import=r'''async function importFiles(files){
  const sourceIdsBefore=new Set(state.importedSources.map(s=>s.id)),participantsBefore=state.participants.length;let imported=0,failed=0,skipped=0,firstSourceId=null;
  for(const f of files){const item=importQueueItem(f);state.importQueue=[...(state.importQueue||[]),item].slice(-40);render();try{if(duplicateSourceForFile(f)&&!await confirmResearchAction(`${f.name} appears to be already imported. Import another copy?`)){item.status='skipped';item.message='Duplicate skipped';skipped++;render();continue;}item.status='working';item.message='Importing…';render();await importOneFile(f);item.status='ok';item.message='Imported successfully';imported++;if(!firstSourceId){const added=state.importedSources.find(s=>!sourceIdsBefore.has(s.id));if(added)firstSourceId=added.id;}}catch(err){item.status='error';item.message=humanError(err,`${f.name} could not be imported. Check the file and try again.`);item.technicalDetails=technicalError(err);failed++;}render();}
  state.lastImportSummary={imported,failed,skipped,total:files.length,newParticipants:Math.max(0,state.participants.length-participantsBefore),firstSourceId,at:Date.now()};saveState('Completed import batch');render();
}'''
app=app[:start]+new_import+app[end:]

anchor="function duplicateSourceForFile(f){return state.importedSources.find(s=>s.name===f.name && (!s.sizeBytes || !f.size || Number(s.sizeBytes)===Number(f.size)));}"
summary_fn=r'''function renderImportCompletion(){const x=state.lastImportSummary;if(!x||!x.total)return '';const bits=[`${x.imported} imported`,x.newParticipants?`${x.newParticipants} participant${x.newParticipants===1?'':'s'} added`:null,x.failed?`${x.failed} need${x.failed===1?'s':''} attention`:null,x.skipped?`${x.skipped} skipped`:null].filter(Boolean);return `<section class="import-completion" aria-live="polite"><div><span class="eyebrow">IMPORT COMPLETE</span><h3>${escapeHtml(bits.join(' · '))}</h3><p>Your project is ready for the next useful step. Trace keeps each file result above for anything that needs attention.</p></div><div class="import-completion-actions">${x.firstSourceId?`<button class="secondary" id="import-open-first" data-source-id="${x.firstSourceId}">Open first source</button><button class="primary" id="import-begin-coding" data-source-id="${x.firstSourceId}">Begin coding</button>`:''}${x.newParticipants?'<button class="secondary" id="import-review-participants">Review participants</button>':''}<button class="text-btn" id="dismiss-import-summary">Dismiss</button></div></section>`;}'''
if anchor in app:
    app=app.replace(anchor,anchor+'\n'+summary_fn,1)
elif 'function renderImportCompletion()' not in app:
    raise SystemExit('Import completion helper anchor changed')

old='${pendingMedia?`<section class="media-import-next-actions"'
if old in app and '${renderImportCompletion()}' not in app:
    app=app.replace(old,'${renderImportCompletion()}\n    '+old,1)
old='${renderImportQueue()}<section class="import-type-grid">'
if old in app:
    app=app.replace(old,'${renderImportQueue()}${renderImportCompletion()}<section class="import-type-grid">',1)
elif app.count('${renderImportCompletion()}')<2:
    raise SystemExit('Imports workspace completion anchor changed')

old="document.querySelector('#clear-import-queue')?.addEventListener('click',()=>{state.importQueue=[];render()});"
new=old+"document.querySelector('#import-open-first')?.addEventListener('click',e=>{activateSource(e.currentTarget.dataset.sourceId);state.activeSection='Data';render()});document.querySelector('#import-begin-coding')?.addEventListener('click',e=>{activateSource(e.currentTarget.dataset.sourceId,false);state.activeSection='Code';saveState('Started coding after import');render()});document.querySelector('#import-review-participants')?.addEventListener('click',()=>{state.dataContext='participants';saveState('Reviewed participants after import');render()});document.querySelector('#dismiss-import-summary')?.addEventListener('click',()=>{state.lastImportSummary=null;saveState('Dismissed import summary');render()});"
if old in app:
    app=app.replace(old,new,1)
elif '#import-begin-coding' not in app:
    raise SystemExit('Import completion binding anchor changed')

start=app.find('async function applyCode(codeId,aiSuggestionId=null,finish=true){')
end=app.find('\nasync function ',start+10)
if start<0: raise SystemExit('applyCode anchor changed')
segment=app[start:end if end>start else len(app)]
if 'firstProjectCoding' not in segment:
    segment=segment.replace("async function applyCode(codeId,aiSuggestionId=null,finish=true){", "async function applyCode(codeId,aiSuggestionId=null,finish=true){\n  const firstProjectCoding=(state.allCodingRefs||state.codingRefs||[]).length===0;",1)
    segment=segment.replace("if(finish){showToast('Passage coded'); removeFloatingTools(); window.getSelection()?.removeAllRanges(); render();}", "if(finish){showToast(firstProjectCoding?'Passage coded. When related ideas begin to repeat, Themes is the next place to organise them.':'Passage coded'); removeFloatingTools(); window.getSelection()?.removeAllRanges(); render();}",1)
    app=app[:start]+segment+app[end if end>start else len(app):]
if 'When related ideas begin to repeat, Themes is the next place' not in app: raise SystemExit('First-coding transition guidance was not applied')

appearance_anchor="</article><article class=\"settings-card\"><span class=\"settings-icon\">${icon('exchange',18)}</span><div><b>Startup</b>"
appearance_card="</article><article class=\"settings-card appearance-settings-card\"><span class=\"settings-icon\">${icon('palette',18)}</span><div><b>Appearance</b><p>Choose the application appearance here as well as from the quick top-bar toggle.</p></div><div class=\"display-size-picker\"><button data-app-theme=\"light\" class=\"${state.theme==='light'?'active':''}\">Light</button><button data-app-theme=\"dark\" class=\"${state.theme==='dark'?'active':''}\">Dark</button></div></article><article class=\"settings-card\"><span class=\"settings-icon\">${icon('exchange',18)}</span><div><b>Startup</b>"
if appearance_anchor in app:
    app=app.replace(appearance_anchor,appearance_card,1)
elif 'data-app-theme="light"' not in app:
    raise SystemExit('Appearance settings anchor changed')

shortcuts_anchor="</article><article class=\"settings-card transcription-defaults-card\">"
shortcuts_card="</article><article class=\"settings-card shortcut-settings-card\"><span class=\"settings-icon\">${icon('search',18)}</span><div><b>Keyboard shortcuts</b><p>Ctrl+K command palette · Ctrl+F search · Ctrl+Shift+C new code · Ctrl+Shift+M memo · Ctrl+Shift+I import · Alt+←/→ source tabs.</p></div><button class=\"secondary tiny\" id=\"settings-open-command-palette\">Open command palette</button></article><article class=\"settings-card transcription-defaults-card\">"
if shortcuts_anchor in app:
    app=app.replace(shortcuts_anchor,shortcuts_card,1)
elif 'shortcut-settings-card' not in app:
    raise SystemExit('Shortcut settings anchor changed')

settings_event_anchor="modal.querySelectorAll('[data-display-size]').forEach(btn=>btn.onclick=()=>{state.displaySize=btn.dataset.displaySize;saveState('Changed display size');document.documentElement.dataset.textSize=state.displaySize;modal.querySelectorAll('[data-display-size]').forEach(x=>x.classList.toggle('active',x.dataset.displaySize===state.displaySize))});"
settings_events=settings_event_anchor+"\n  modal.querySelectorAll('[data-app-theme]').forEach(btn=>btn.onclick=()=>{state.theme=btn.dataset.appTheme;saveState('Changed appearance');document.documentElement.dataset.theme=state.theme;modal.querySelectorAll('[data-app-theme]').forEach(x=>x.classList.toggle('active',x.dataset.appTheme===state.theme))});modal.querySelector('#settings-open-command-palette')?.addEventListener('click',()=>{close();openCommandPalette()});"
if settings_event_anchor in app:
    app=app.replace(settings_event_anchor,settings_events,1)
elif "[data-app-theme]" not in app:
    raise SystemExit('Application Settings event anchor changed')

marker='/* UX_V2_FINAL_CLOSURE */'
if marker not in css:
    css += r'''

/* UX_V2_FINAL_CLOSURE */
.import-completion{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:16px 18px;background:var(--panel2);border:1px solid var(--line);border-radius:8px}.import-completion h3{margin:2px 0 4px;font-size:17px}.import-completion p{margin:0;color:var(--muted);font-size:13px;line-height:1.45}.import-completion-actions{display:flex;align-items:center;gap:8px;flex-wrap:wrap;justify-content:flex-end}@media(max-width:900px){.import-completion{align-items:stretch;flex-direction:column}.import-completion-actions{justify-content:flex-start}}
'''

app_path.write_text(app,encoding='utf-8')
css_path.write_text(css,encoding='utf-8')
for assertion in [
    "assert 'function renderImportCompletion()' in app and 'IMPORT COMPLETE' in app\n",
    "assert 'Open first source' in app and 'Begin coding' in app and 'Review participants' in app\n",
    "assert 'When related ideas begin to repeat, Themes is the next place' in app\n",
    "assert 'data-app-theme=\"light\"' in app and 'shortcut-settings-card' in app\n",
    "assert 'UX_V2_FINAL_CLOSURE' in css\n",
]:
    if assertion not in contract: contract+='\n'+assertion
contract_path.write_text(contract,encoding='utf-8')

if browser_path.exists():
    b=browser_path.read_text(encoding='utf-8')
    old="if(!await page.locator('#default-whisper-model').count())errors.push('Application Settings is missing default Whisper model control');"
    new=old+"\n  if(!await page.locator('[data-app-theme=\"light\"]').count())errors.push('Application Settings is missing appearance controls');\n  if(!await page.locator('#settings-open-command-palette').count())errors.push('Application Settings is missing shortcut discoverability');"
    if old in b and 'Application Settings is missing appearance controls' not in b:b=b.replace(old,new,1)
    browser_path.write_text(b,encoding='utf-8')
print('Final import guidance, appearance/shortcut settings and research-journey transition guidance applied')
