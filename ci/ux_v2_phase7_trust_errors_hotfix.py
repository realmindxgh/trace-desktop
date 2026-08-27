from pathlib import Path

app_path=Path('src/app.js')
css_path=Path('src/styles.css')
test_path=Path('tests/ux_foundation_v2_contract.py')
app=app_path.read_text(encoding='utf-8')

# 1. Replace the basic human-error helper with a reusable, plain-language error component.
old="""function humanError(err,fallback='Trace could not complete that action.'){
  const s=String(err||'').replace(/^Error:\\s*/,'');
  if(/not enough|space/i.test(s))return 'There is not enough free space to complete this action.';
  if(/locked|running/i.test(s))return 'Trace or one of its files is still in use. Close the related window and try again.';
  if(/permission|writable|access/i.test(s))return 'Windows did not allow Trace to write there. Choose another location or check folder permissions.';
  if(/cancel/i.test(s))return 'The action was cancelled.';
  return s&&s.length<220?s:fallback;
}
function confirmResearchAction(message,details='This change affects research project state.'){
  return new Promise(resolve=>{const root=document.querySelector('#modal-root');root.innerHTML=`<div class=\"modal-backdrop\"><section class=\"small-modal confirmation-modal\"><span class=\"eyebrow\">CONFIRM CHANGE</span><h2>${escapeHtml(message)}</h2><p class=\"modal-note\">${escapeHtml(details)}</p><div class=\"modal-actions\"><button class=\"secondary\" id=\"confirm-cancel\">Cancel</button><button class=\"danger-btn\" id=\"confirm-go\">Continue</button></div></section></div>`;const done=v=>{root.innerHTML='';resolve(v)};root.querySelector('#confirm-cancel').onclick=()=>done(false);root.querySelector('#confirm-go').onclick=()=>done(true);activateModalAccessibility(root);});
}
"""
new=r'''function technicalError(err){
  return String(err||'Unknown error').replace(/^Error:\s*/,'').replace(/[\u0000-\u001f]+/g,' ').trim().slice(0,1200);
}
function humanError(err,fallback='Trace could not complete that action.'){
  const s=technicalError(err);
  if(/not enough|no space|disk full|quota/i.test(s))return 'There is not enough free space to complete this action safely.';
  if(/locked|busy|running|in use/i.test(s))return 'Trace or one of its files is still in use. Close the related window and try again.';
  if(/permission|writable|access denied|unauthorized/i.test(s))return 'Windows did not allow Trace to write there. Choose another location or check folder permissions.';
  if(/not found|no such file|cannot find/i.test(s))return 'Trace cannot find one of the files needed for this action. Locate the project or source and try again.';
  if(/corrupt|malformed|invalid database|database disk image/i.test(s))return 'Trace could not safely read this project or file. Keep the original unchanged and try recovery or a verified backup.';
  if(/cancel/i.test(s))return 'The action was cancelled.';
  if(/sqlite|tauri|rust|plugin|invoke|panic|thread|os error|sql/i.test(s))return fallback;
  return s&&s.length<220?s:fallback;
}
function showActionError(title,err,recovery='Try the action again. If it still fails, keep the original research file unchanged and use Diagnostics from Application Settings.'){
  const root=document.querySelector('#modal-root'),plain=humanError(err,'Trace could not complete that action safely.'),technical=technicalError(err);
  root.innerHTML=`<div class="modal-backdrop"><section class="small-modal error-modal" role="alertdialog" aria-modal="true" aria-labelledby="trace-error-title"><span class="eyebrow">TRACE COULD NOT COMPLETE THAT</span><h2 id="trace-error-title">${escapeHtml(title)}</h2><p class="error-summary">${escapeHtml(plain)}</p><div class="error-recovery"><b>What you can do</b><p>${escapeHtml(recovery)}</p></div><details class="technical-details"><summary>Technical details</summary><code>${escapeHtml(technical)}</code></details><div class="modal-actions"><button class="primary" id="error-close">Close</button></div></section></div>`;
  root.querySelector('#error-close').onclick=()=>root.innerHTML='';activateModalAccessibility(root);
}
function showResearchProtection(title,summary,consequences=[]){
  const root=document.querySelector('#modal-root'),impact=(consequences||[]).filter(Boolean);
  root.innerHTML=`<div class="modal-backdrop"><section class="small-modal protection-modal" role="dialog" aria-modal="true"><span class="eyebrow">RESEARCH PROTECTION</span><h2>${escapeHtml(title)}</h2><p class="modal-note">${escapeHtml(summary)}</p>${impact.length?`<div class="change-impact"><b>Protected evidence</b><ul>${impact.map(x=>`<li>${escapeHtml(x)}</li>`).join('')}</ul></div>`:''}<div class="modal-actions"><button class="primary" id="protection-close">Understood</button></div></section></div>`;
  root.querySelector('#protection-close').onclick=()=>root.innerHTML='';activateModalAccessibility(root);
}
function confirmResearchAction(message,details='This change affects research project state.',consequences=[]){
  return new Promise(resolve=>{const root=document.querySelector('#modal-root');const impact=(consequences||[]).filter(Boolean);root.innerHTML=`<div class="modal-backdrop"><section class="small-modal confirmation-modal" role="alertdialog" aria-modal="true"><span class="eyebrow">CONFIRM CHANGE</span><h2>${escapeHtml(message)}</h2><p class="modal-note">${escapeHtml(details)}</p>${impact.length?`<div class="change-impact"><b>This will affect</b><ul>${impact.map(x=>`<li>${escapeHtml(x)}</li>`).join('')}</ul></div>`:''}<div class="modal-actions"><button class="secondary" id="confirm-cancel">Cancel</button><button class="danger-btn" id="confirm-go">Continue</button></div></section></div>`;const done=v=>{root.innerHTML='';resolve(v)};root.querySelector('#confirm-cancel').onclick=()=>done(false);root.querySelector('#confirm-go').onclick=()=>done(true);activateModalAccessibility(root);});
}
function sourceDeleteImpact(src){
  const refs=(state.allCodingRefs||state.codingRefs).filter(r=>r.sourceId===src.id).length;
  const annotations=(state.annotations||[]).filter(a=>a.sourceId===src.id).length;
  const anchors=(state.evidenceAnchors||[]).filter(a=>a.sourceId===src.id).length;
  const media=(state.mediaSelections||[]).filter(a=>a.sourceId===src.id).length;
  const memos=(state.memos||[]).filter(m=>m.targetType==='source'&&m.targetId===src.id).length;
  const collections=(state.sourceCollections||[]).filter(c=>(c.sourceIds||[]).includes(src.id)).length;
  const impact=[];
  if(refs)impact.push(`${refs} coding reference${refs===1?'':'s'}`);
  if(annotations)impact.push(`${annotations} annotation${annotations===1?'':'s'}`);
  if(anchors)impact.push(`${anchors} evidence anchor${anchors===1?'':'s'}`);
  if(media)impact.push(`${media} saved media selection${media===1?'':'s'}`);
  if(memos)impact.push(`${memos} source memo${memos===1?'':'s'}`);
  if(collections)impact.push(`membership in ${collections} collection${collections===1?'':'s'}`);
  if(src.participantId)impact.push('the source-to-participant link');
  return impact;
}
function codeDeleteImpact(code){
  const refs=(state.allCodingRefs||state.codingRefs).filter(r=>r.codeId===code.id).length;
  const themes=(state.themes||[]).filter(t=>(t.codeIds||[]).includes(code.id)).length;
  const media=(state.mediaCodings||[]).filter(r=>r.codeId===code.id).length;
  const memos=(state.memos||[]).filter(m=>m.targetType==='code'&&m.targetId===code.id).length;
  const impact=[];
  if(refs)impact.push(`${refs} coded passage${refs===1?'':'s'}`);
  if(media)impact.push(`${media} coded media selection${media===1?'':'s'}`);
  if(themes)impact.push(`the code link in ${themes} theme${themes===1?'':'s'}`);
  if(memos)impact.push(`${memos} code memo${memos===1?'':'s'}`);
  return impact;
}
'''
if old in app:
    app=app.replace(old,new,1)
elif 'function showActionError(' not in app:
    raise SystemExit('humanError/confirmation anchor changed')

# 2. Make transcription failures/replacement protections explicit.
app=app.replace("if(existing&&transcriptHasProtectedEvidence(src)){showToast('This transcript is protected by existing coded or annotated evidence.');return;}",
                "if(existing&&transcriptHasProtectedEvidence(src)){const refs=(state.allCodingRefs||state.codingRefs).filter(r=>r.sourceId===src.id).length,anns=(state.annotations||[]).filter(a=>a.sourceId===src.id).length,anchors=(state.evidenceAnchors||[]).filter(a=>a.sourceId===src.id).length;showResearchProtection('Re-transcription is locked because research evidence depends on this transcript.','Trace will not replace transcript text while doing so could detach coding or annotations from their evidence.',[refs?`${refs} coding reference${refs===1?'':'s'}`:null,anns?`${anns} annotation${anns===1?'':'s'}`:null,anchors?`${anchors} evidence anchor${anchors===1?'':'s'}`:null]);return;}",1)
app=app.replace("if(existing&&!await confirmResearchAction('Replace the current transcript? Trace will preserve the original media, but the existing transcript text will be replaced.'))return;",
                "if(existing&&!await confirmResearchAction('Replace the current transcript?','The original audio/video file will remain unchanged, but the existing transcript text and timestamps will be replaced.',[`${(src.segments||[]).length} existing transcript segment${(src.segments||[]).length===1?'':'s'}`]))return;",1)
app=app.replace("}catch(err){showToast('Local transcription failed: '+String(err));}","}catch(err){showActionError('Local transcription failed.',err,'Check the local Whisper model, confirm the media file is still available, and try again. Your original media remains unchanged.');}",1)
app=app.replace("}catch(err){showToast('Could not use that Whisper model: '+String(err));}","}catch(err){showActionError('Trace could not use that transcription model.',err,'Choose a valid local Whisper model file and try again.');}",1)
app=app.replace("}catch(err){console.warn('Media preview unavailable',err);showToast('Media preview unavailable: '+String(err));}","}catch(err){console.warn('Media preview unavailable',err);showActionError('Media preview is unavailable.',err,'Confirm the source file still exists in this project. The imported research record has not been changed.');}",1)

# Expose a clear protection explanation instead of a dead disabled re-transcription control.
app=app.replace('<button class="primary" id="transcribe-source" ${busy||!model||protectedTranscript?\'disabled\':\'\'}>${actionLabel}</button>',
                '${protectedTranscript?`<button class="secondary" id="transcription-protection">Why re-transcription is locked</button>`:`<button class="primary" id="transcribe-source" ${busy||!model?\'disabled\':\'\'}>${actionLabel}</button>`}',1)
old_bind="document.querySelector('#source-manage')?.addEventListener('click',()=>state.activeSourceId&&openSourceManager(state.activeSourceId));document.querySelector('#choose-whisper-model')?.addEventListener('click',chooseWhisperModel);document.querySelector('#transcribe-source')?.addEventListener('click',transcribeActiveSource);"
new_bind="document.querySelector('#source-manage')?.addEventListener('click',()=>state.activeSourceId&&openSourceManager(state.activeSourceId));document.querySelector('#choose-whisper-model')?.addEventListener('click',chooseWhisperModel);document.querySelector('#transcribe-source')?.addEventListener('click',transcribeActiveSource);document.querySelector('#transcription-protection')?.addEventListener('click',()=>transcribeActiveSource());"
if old_bind in app:
    app=app.replace(old_bind,new_bind,1)
elif "#transcription-protection" not in app:
    raise SystemExit('Transcription protection event anchor changed')

# 3. Humanise import queue errors and provide technical disclosure per failed file.
old_queue="function renderImportQueue(){const q=state.importQueue||[];if(!q.length)return '';return `<div class=\"import-queue\" aria-live=\"polite\"><div class=\"section-title-row\"><div><span class=\"eyebrow\">IMPORT QUEUE</span><h3>File results</h3></div><button class=\"text-btn\" id=\"clear-import-queue\">Clear</button></div>${q.slice(-12).map(x=>`<article class=\"import-result ${x.status}\"><span>${x.status==='ok'?'✓':x.status==='error'?'!':x.status==='skipped'?'↷':'…'}</span><div><b>${escapeHtml(x.name)}</b><small>${escapeHtml(x.message||x.status)}</small></div></article>`).join('')}</div>`;}"
new_queue="function renderImportQueue(){const q=state.importQueue||[];if(!q.length)return '';return `<div class=\"import-queue\" aria-live=\"polite\"><div class=\"section-title-row\"><div><span class=\"eyebrow\">IMPORT QUEUE</span><h3>File results</h3></div><button class=\"text-btn\" id=\"clear-import-queue\">Clear</button></div>${q.slice(-12).map(x=>`<article class=\"import-result ${x.status}\"><span>${x.status==='ok'?'✓':x.status==='error'?'!':x.status==='skipped'?'↷':'…'}</span><div><b>${escapeHtml(x.name)}</b><small>${escapeHtml(x.message||x.status)}</small>${x.status==='error'&&x.technical?`<details class=\"import-technical\"><summary>Technical details</summary><code>${escapeHtml(x.technical)}</code></details>`:''}</div></article>`).join('')}</div>`;}"
if old_queue in app:
    app=app.replace(old_queue,new_queue,1)
elif 'import-technical' not in app:
    raise SystemExit('Import queue renderer anchor changed')
old_import="async function importFiles(files){for(const f of files){const item=importQueueItem(f);state.importQueue=[...(state.importQueue||[]),item].slice(-40);render();try{if(duplicateSourceForFile(f)&&!await confirmResearchAction(`${f.name} appears to be already imported. Import another copy?`)){item.status='skipped';item.message='Duplicate skipped';render();continue;}item.status='working';item.message='Importing…';render();await importOneFile(f);item.status='ok';item.message='Imported successfully';}catch(err){console.error(err);item.status='error';item.message=String(err).replace(/^Error:\\s*/,'');}render();}}"
new_import="async function importFiles(files){for(const f of files){const item=importQueueItem(f);state.importQueue=[...(state.importQueue||[]),item].slice(-40);render();try{if(duplicateSourceForFile(f)&&!await confirmResearchAction(`${f.name} appears to be already imported. Import another copy?`,'Trace can keep both copies, but duplicate sources can make coding and counts harder to interpret.')){item.status='skipped';item.message='Duplicate skipped';render();continue;}item.status='working';item.message=`Importing ${f.name}…`;render();await importOneFile(f);item.status='ok';item.message='Imported successfully';item.technical='';}catch(err){console.error(err);item.status='error';item.message=humanError(err,'Trace could not import this file safely.');item.technical=technicalError(err);}render();}}"
if old_import in app:
    app=app.replace(old_import,new_import,1)
elif "item.technical=technicalError(err)" not in app:
    raise SystemExit('Import handler anchor changed')

# 4. Strengthen destructive confirmations and replace raw exceptions in high-value research actions.
old_code="root.querySelector('#ce-delete')?.addEventListener('click',async()=>{if(!await confirmResearchAction(`Delete code \"${code.name}\"? Its coding references will also be removed.`))return;"
new_code="root.querySelector('#ce-delete')?.addEventListener('click',async()=>{if(!await confirmResearchAction(`Delete code \"${code.name}\"?`,'The code itself will be removed. Source text and media stay in the project.',codeDeleteImpact(code)))return;"
if old_code in app: app=app.replace(old_code,new_code,1)
app=app.replace("}catch(err){showToast('Could not delete code: '+String(err));}});","}catch(err){showActionError('Trace could not delete that code.',err,'Nothing else should be changed. Review the code and try again.');}});",1)

old_theme="root.querySelector('#te-delete')?.addEventListener('click',async()=>{if(!await confirmResearchAction(`Delete candidate theme \"${theme.name}\"? Codes and coded passages will remain.`))return;"
new_theme="root.querySelector('#te-delete')?.addEventListener('click',async()=>{const linkedWriting=(state.findingsSections||[]).filter(x=>x.targetType==='theme'&&x.targetId===theme.id).length;if(!await confirmResearchAction(`Delete candidate theme \"${theme.name}\"?`,'Codes and coded passages will remain. The interpretive grouping itself will be removed.',[`${(theme.codeIds||[]).length} linked code${(theme.codeIds||[]).length===1?'':'s'}`,linkedWriting?`${linkedWriting} findings section${linkedWriting===1?'':'s'} currently organised under this theme`:null]))return;"
if old_theme in app: app=app.replace(old_theme,new_theme,1)
app=app.replace("}catch(err){showToast('Could not delete theme');}});","}catch(err){showActionError('Trace could not delete that theme.',err,'The theme should remain unchanged. Try again after reviewing its linked codes and writing.');}});",1)

old_source="root.querySelector('#sm-delete').onclick=async()=>{if(!await confirmResearchAction(`Delete ${src.name}? Coding and evidence attached to this source will also be removed.`))return;"
new_source="root.querySelector('#sm-delete').onclick=async()=>{if(!await confirmResearchAction(`Delete ${src.name}?`,'The imported source record will be removed from this project. The original external file is not modified.',sourceDeleteImpact(src)))return;"
if old_source in app: app=app.replace(old_source,new_source,1)
app=app.replace("}catch(err){showToast('Could not delete source');return;}","}catch(err){showActionError('Trace could not delete that source.',err,'The source should remain in the project. Review its linked evidence and try again.');return;}",1)
app=app.replace("}catch(err){showToast('Could not update source: '+String(err));return;}","}catch(err){showActionError('Trace could not update that source.',err,'The existing source remains unchanged. Check the participant/collection selection and try again.');return;}",1)

repls={
"}catch(err){showToast('Could not save code: '+String(err));}};":"}catch(err){showActionError('Trace could not save that code.',err,'Review the code name and try again. No coding should be lost.');}};",
"}catch(err){showToast('Could not remove coding: '+String(err));}":"}catch(err){showActionError('Trace could not remove that coding reference.',err,'The coded passage should remain unchanged. Try again.');}",
"}catch(err){showToast('Could not delete selection: '+String(err));}":"}catch(err){showActionError('Trace could not delete that media selection.',err,'The saved evidence selection should remain unchanged. Try again.');}",
"}catch(err){showToast('Restore failed: '+String(err));}":"}catch(err){showActionError('Trace could not restore that backup.',err,'Keep the current project open and choose another verified backup or export diagnostics. The current project was not replaced.');}",
"}catch(err){showToast(String(err));}\n}":"}catch(err){showActionError('Trace could not undo that action.',err,'The project remains at its current state. Review the last action and try again.');}\n}",
"}catch(err){showToast(String(err));}\n}\nasync function beginNativeSession":"}catch(err){showActionError('Trace could not redo that action.',err,'The project remains at its current state. Review the action history and try again.');}\n}\nasync function beginNativeSession",
}
for a,b in repls.items():
    if a in app: app=app.replace(a,b,1)

app_path.write_text(app,encoding='utf-8')

css=css_path.read_text(encoding='utf-8')
if '/* UX_V2_TRUST_ERROR_SYSTEM */' not in css:
    css += r'''

/* UX_V2_TRUST_ERROR_SYSTEM */
.error-modal .error-summary{font-size:var(--trace-font-ui,15px);line-height:1.55;color:var(--ink);margin:8px 0 14px}.error-recovery{padding:12px 13px;background:var(--panel2);border-radius:8px}.error-recovery b{font-size:13px}.error-recovery p{margin:5px 0 0;color:var(--muted);line-height:1.5}.technical-details,.import-technical{margin-top:12px;font-size:12.5px}.technical-details summary,.import-technical summary{cursor:pointer;color:var(--muted);font-weight:650}.technical-details code,.import-technical code{display:block;white-space:pre-wrap;overflow-wrap:anywhere;margin-top:8px;padding:9px 10px;border-radius:6px;background:var(--panel2);color:var(--muted);font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:12px;max-height:160px;overflow:auto}.change-impact{margin-top:12px;padding:11px 13px;background:var(--panel2);border-radius:8px}.change-impact b{font-size:13px}.change-impact ul{margin:7px 0 0 18px;padding:0;color:var(--muted);line-height:1.5}.import-result>div{min-width:0}.import-technical{margin-top:6px}
'''
    css_path.write_text(css,encoding='utf-8')

test=test_path.read_text(encoding='utf-8')
for assertion in [
    "assert 'function showActionError' in app\n",
    "assert 'function showResearchProtection' in app\n",
    "assert 'function sourceDeleteImpact' in app\n",
    "assert 'function codeDeleteImpact' in app\n",
    "assert 'Technical details' in app\n",
    "assert 'UX_V2_TRUST_ERROR_SYSTEM' in css\n",
]:
    if assertion not in test:
        test+='\n'+assertion
test_path.write_text(test,encoding='utf-8')

check=app_path.read_text(encoding='utf-8')
for required in ('showActionError','showResearchProtection','sourceDeleteImpact','codeDeleteImpact','import-technical','This will affect'):
    if required not in check:
        raise SystemExit(f'Trust/error UX contract missing: {required}')
print('Phase 7 trust, destructive-action and human-error hotfix applied')
