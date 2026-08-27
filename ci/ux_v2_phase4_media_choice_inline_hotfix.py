from pathlib import Path
import runpy

app_path=Path('src/app.js')
css_path=Path('src/styles.css')
contract_path=Path('tests/ux_foundation_v2_contract.py')
app=app_path.read_text(encoding='utf-8')
css=css_path.read_text(encoding='utf-8')
contract=contract_path.read_text(encoding='utf-8')

start=app.find('function offerMediaImportChoice(sourceId){')
end=app.find("\nfunction importQueueItem(file,status='queued'",start)
if start<0 or end<0: raise SystemExit('Media choice function boundaries changed')
new_fn=r'''function offerMediaImportChoice(sourceId){state.pendingMediaTranscriptionSourceId=sourceId;render();return Promise.resolve('offered');}
function dismissPendingMediaChoice(){state.pendingMediaTranscriptionSourceId=null;saveState('Kept media without transcription');render();}
async function transcribePendingMedia(sourceId){state.pendingMediaTranscriptionSourceId=null;state.activeSection='Code';activateSource(sourceId,false);render();if(!effectiveTranscriptionModel()?.path)await chooseWhisperModel();if(effectiveTranscriptionModel()?.path)await transcribeActiveSource();}'''
app=app[:start]+new_fn+app[end:]

old="function renderDataSourcesWorkspace(){\n  const sources=visibleSources();const bp=state.backupPolicy||{enabled:true,intervalMinutes:15,keepCount:20,lastBackupAt:null};\n  const activeCollection=state.sourceCollections.find(c=>c.id===state.activeCollectionId);"
new="function renderDataSourcesWorkspace(){\n  const sources=visibleSources();const bp=state.backupPolicy||{enabled:true,intervalMinutes:15,keepCount:20,lastBackupAt:null};\n  const activeCollection=state.sourceCollections.find(c=>c.id===state.activeCollectionId);\n  const pendingMedia=state.importedSources.find(s=>s.id===state.pendingMediaTranscriptionSourceId&&['audio','video'].includes(s.kind));"
if old in app:
    app=app.replace(old,new,1)
elif 'const pendingMedia=state.importedSources.find' not in app:
    raise SystemExit('Data Sources pending-media anchor changed')

old="    <div class=\"import-drop-zone\" id=\"import-drop-zone\""
new="    ${pendingMedia?`<section class=\"media-import-next-actions\" aria-live=\"polite\"><div><span class=\"eyebrow\">${escapeHtml(pendingMedia.kind.toUpperCase())} IMPORTED</span><h3>${escapeHtml(pendingMedia.name)} is safely in the project.</h3><p>Would you like to create searchable, codable text now? Transcription runs locally on this computer and never uploads the recording.</p></div><div><button class=\"secondary\" id=\"media-import-add\">Add without transcription</button><button class=\"primary\" id=\"media-import-transcribe\" data-source-id=\"${pendingMedia.id}\">Transcribe now</button></div></section>`:''}\n    <div class=\"import-drop-zone\" id=\"import-drop-zone\""
if old in app:
    app=app.replace(old,new,1)
elif 'media-import-next-actions' not in app:
    raise SystemExit('Data Sources media-choice render anchor changed')

old="document.querySelector('#clear-import-queue')?.addEventListener('click',()=>{state.importQueue=[];render()});}"
new="document.querySelector('#clear-import-queue')?.addEventListener('click',()=>{state.importQueue=[];render()});document.querySelector('#media-import-add')?.addEventListener('click',dismissPendingMediaChoice);document.querySelector('#media-import-transcribe')?.addEventListener('click',e=>transcribePendingMedia(e.currentTarget.dataset.sourceId));}"
if old in app:
    app=app.replace(old,new,1)
elif "#media-import-transcribe" not in app:
    raise SystemExit('Import binding anchor changed')

marker='/* UX_V2_PHASE4_MEDIA_IMPORT_CHOICE */'
if marker not in css:
    css += r'''

/* UX_V2_PHASE4_MEDIA_IMPORT_CHOICE */
.media-import-next-actions{display:flex;align-items:center;justify-content:space-between;gap:22px;padding:16px 18px;background:var(--panel2);border:1px solid var(--line);border-radius:8px}
.media-import-next-actions h3{margin:2px 0 4px;font-size:17px}.media-import-next-actions p{margin:0;color:var(--muted);font-size:13px;line-height:1.45;max-width:760px}.media-import-next-actions>div:last-child{display:flex;gap:8px;flex:0 0 auto}
@media(max-width:900px){.media-import-next-actions{align-items:stretch;flex-direction:column}.media-import-next-actions>div:last-child{justify-content:flex-start;flex-wrap:wrap}}
'''

app_path.write_text(app,encoding='utf-8')
css_path.write_text(css,encoding='utf-8')
for assertion in [
    "assert 'media-import-next-actions' in app\n",
    "assert 'Transcribe now' in app and 'Add without transcription' in app\n",
    "assert 'function transcribePendingMedia' in app\n",
    "assert 'UX_V2_PHASE4_MEDIA_IMPORT_CHOICE' in css\n",
]:
    if assertion not in contract: contract+='\n'+assertion
contract_path.write_text(contract,encoding='utf-8')

# This is the last UI transform in the visual-evidence chain, so install the approved visual
# comparator only after all final CSS/render changes have been applied.
runpy.run_path('../control/ci/ux_v2_phase8_visual_regression_hotfix.py',run_name='__main__')
print('Non-blocking audio/video import transcription choice and approved visual-regression gate applied')
