from pathlib import Path

p=Path('src/app.js')
cssp=Path('src/styles.css')
tp=Path('tests/ux_foundation_v2_contract.py')
s=p.read_text(encoding='utf-8')

old=r'''function humanError(err,fallback='Trace could not complete that action.'){
  const s=String(err||'').replace(/^Error:\s*/,'');
  if(/not enough|space/i.test(s))return 'There is not enough free space to complete this action.';
  if(/locked|running/i.test(s))return 'Trace or one of its files is still in use. Close the related window and try again.';
  if(/permission|writable|access/i.test(s))return 'Windows did not allow Trace to write there. Choose another location or check folder permissions.';
  if(/cancel/i.test(s))return 'The action was cancelled.';
  return s&&s.length<220?s:fallback;
}
'''
new=r'''function technicalError(err){
  return String(err||'').replace(/^Error:\s*/,'').replace(/[\r\n]+/g,' ').trim().slice(0,1600);
}
function humanError(err,fallback='Trace could not complete that action.'){
  const s=technicalError(err);
  if(/not enough|no space|disk full|storage.*full/i.test(s))return 'There is not enough free space to complete this action.';
  if(/locked|already running|in use/i.test(s))return 'Trace or one of its files is still in use. Close the related window and try again.';
  if(/permission|writable|access denied|denied by windows/i.test(s))return 'Windows did not allow Trace to write there. Choose another location or check folder permissions.';
  if(/not found|missing file|does not exist/i.test(s))return 'Trace could not find a file it needs. Check that the project or source has not been moved, then try again.';
  if(/cancel/i.test(s))return 'The action was cancelled.';
  if(/tauri|rust|sqlite|database|plugin|serde|panic|proc macro|invoke|webview|os error|src[\\/]|\.rs:\d+|stack trace/i.test(s))return fallback;
  return s&&s.length<180?s:fallback;
}
function showActionError(title,err,fallback='Trace could not complete that action.'){
  const root=document.querySelector('#modal-root'),summary=humanError(err,fallback),technical=technicalError(err);
  root.innerHTML=`<div class="modal-backdrop"><section class="small-modal error-state-modal" role="alertdialog" aria-modal="true" aria-labelledby="trace-error-title"><span class="eyebrow">ACTION NEEDS ATTENTION</span><h2 id="trace-error-title">${escapeHtml(title)}</h2><p class="modal-note">${escapeHtml(summary)}</p>${technical&&technical!==summary?`<details class="technical-details"><summary>Technical details</summary><pre>${escapeHtml(technical)}</pre></details>`:''}<div class="modal-actions"><button class="primary" id="error-close">Close</button></div></section></div>`;
  root.querySelector('#error-close').onclick=()=>root.innerHTML='';activateModalAccessibility(root);
}
function showResearchNotice(title,details){
  return new Promise(resolve=>{const root=document.querySelector('#modal-root');root.innerHTML=`<div class="modal-backdrop"><section class="small-modal research-notice" role="dialog" aria-modal="true"><span class="eyebrow">RESEARCH DATA PROTECTION</span><h2>${escapeHtml(title)}</h2><p class="modal-note">${escapeHtml(details)}</p><div class="modal-actions"><button class="primary" id="notice-close">Close</button></div></section></div>`;root.querySelector('#notice-close').onclick=()=>{root.innerHTML='';resolve()};activateModalAccessibility(root);});
}
'''
if old not in s:
    raise SystemExit('humanError anchor missing')
s=s.replace(old,new,1)

old="if(existing&&transcriptHasProtectedEvidence(src)){showToast('This transcript is protected by existing coded or annotated evidence.');return;}\n  if(existing&&!await confirmResearchAction('Replace the current transcript? Trace will preserve the original media, but the existing transcript text will be replaced.'))return;"
new=r'''if(existing&&transcriptHasProtectedEvidence(src)){
    const coded=(state.allCodingRefs||state.codingRefs).filter(r=>r.sourceId===src.id).length,notes=(state.annotations||[]).filter(a=>a.sourceId===src.id).length,anchors=(state.evidenceAnchors||[]).filter(a=>a.sourceId===src.id).length;
    await showResearchNotice('This transcript cannot be replaced while evidence is attached.',`${coded} coded passage${coded===1?'':'s'}, ${notes} annotation${notes===1?'':'s'} and ${anchors} linked evidence reference${anchors===1?'':'s'} depend on the current transcript. Trace is blocking retranscription so those research links cannot be silently orphaned.`);return;
  }
  if(existing&&!await confirmResearchAction('Replace the current transcript?','The original media will remain unchanged, but the existing transcript text and timestamps will be replaced. This cannot be undone through transcript history.'))return;'''
if old not in s:
    raise SystemExit('transcription protection anchor missing')
s=s.replace(old,new,1)

old="function renderImportQueue(){const q=state.importQueue||[];if(!q.length)return '';return `<div class=\"import-queue\" aria-live=\"polite\"><div class=\"section-title-row\"><div><span class=\"eyebrow\">IMPORT QUEUE</span><h3>File results</h3></div><button class=\"text-btn\" id=\"clear-import-queue\">Clear</button></div>${q.slice(-12).map(x=>`<article class=\"import-result ${x.status}\"><span>${x.status==='ok'?'✓':x.status==='error'?'!':x.status==='skipped'?'↷':'…'}</span><div><b>${escapeHtml(x.name)}</b><small>${escapeHtml(x.message||x.status)}</small></div></article>`).join('')}</div>`;}"
new="function renderImportQueue(){const q=state.importQueue||[];if(!q.length)return '';return `<div class=\"import-queue\" aria-live=\"polite\"><div class=\"section-title-row\"><div><span class=\"eyebrow\">IMPORT QUEUE</span><h3>File results</h3></div><button class=\"text-btn\" id=\"clear-import-queue\">Clear</button></div>${q.slice(-12).map(x=>`<article class=\"import-result ${x.status}\"><span>${x.status==='ok'?'✓':x.status==='error'?'!':x.status==='skipped'?'↷':'…'}</span><div><b>${escapeHtml(x.name)}</b><small>${escapeHtml(x.message||x.status)}</small>${x.status==='error'&&x.technicalDetails?`<details class=\"import-error-details\"><summary>Technical details</summary><code>${escapeHtml(x.technicalDetails)}</code></details>`:''}</div></article>`).join('')}</div>`;}"
if old not in s:
    raise SystemExit('import queue renderer anchor missing')
s=s.replace(old,new,1)
old=r"catch(err){console.error(err);item.status='error';item.message=String(err).replace(/^Error:\s*/,'');}"
new="catch(err){item.status='error';item.message=humanError(err,`${f.name} could not be imported. Check the file and try again.`);item.technicalDetails=technicalError(err);}"
if old not in s:
    raise SystemExit('import error anchor missing')
s=s.replace(old,new,1)

repls={
"catch(err){showToast('Could not use that Whisper model: '+String(err));}":"catch(err){showActionError('Whisper model could not be opened',err,'Trace could not use that local transcription model. Choose a valid Whisper model file and try again.');}",
"catch(err){showToast('Local transcription failed: '+String(err));}":"catch(err){showActionError('Local transcription did not finish',err,'Trace could not complete local transcription. Check the media file and model, then try again.');}",
"catch(err){showToast('Could not save code: '+String(err));}};":"catch(err){showActionError('Code could not be saved',err,'Trace could not save that code. Your existing coding has not been changed.');}};",
"catch(err){showToast('Could not delete code: '+String(err));}});":"catch(err){showActionError('Code could not be deleted',err,'Trace left the code and its research links unchanged.');}});",
"catch(err){showToast('Could not save memo: '+String(err));}};":"catch(err){showActionError('Memo could not be saved',err,'Trace could not save that memo. Copy any unsaved text before closing this message.');}};",
"catch(err){showToast('Could not save theme: '+String(err));}};":"catch(err){showActionError('Theme could not be saved',err,'Trace could not save that candidate theme. Existing codes and evidence are unchanged.');}};",
"catch(err){showToast('Could not remove coding: '+String(err));}}":"catch(err){showActionError('Coding could not be removed',err,'Trace left the coded passage unchanged.');}}",
"catch(err){showToast('Could not delete annotation: '+String(err));}}":"catch(err){showActionError('Annotation could not be deleted',err,'Trace left the annotation unchanged.');}}",
"catch(err){showToast('Restore failed: '+String(err));}}":"catch(err){showActionError('Backup could not be restored',err,'Trace could not restore that backup as a new project. Your current project is unchanged.');}}",
"catch(err){showToast(String(err));}\n}\nasync function redoResearchAction":"catch(err){showActionError('Undo could not be completed',err,'Trace could not undo the last research action. Your project remains in its current state.');}\n}\nasync function redoResearchAction",
"catch(err){showToast(String(err));}\n}\nasync function beginNativeSession":"catch(err){showActionError('Redo could not be completed',err,'Trace could not redo the research action. Your project remains in its current state.');}\n}\nasync function beginNativeSession",
}
for a,b in repls.items():
    if a in s:
        s=s.replace(a,b,1)

old='if(!await confirmResearchAction(`Delete code "${code.name}"? Its coding references will also be removed.`))return;'
new='const refCount=(state.allCodingRefs||state.codingRefs).filter(r=>r.codeId===code.id).length,themeCount=state.themes.filter(t=>(t.codeIds||[]).includes(code.id)).length;if(!await confirmResearchAction(`Delete code "${code.name}"?`,`${refCount} coded passage${refCount===1?\'\':\'s\'} will lose this code and ${themeCount} candidate theme${themeCount===1?\'\':\'s\'} will lose the relationship. Source text, notes and memos will remain.`))return;'
if old not in s:
    raise SystemExit('code delete warning anchor missing')
s=s.replace(old,new,1)

old='if(!await confirmResearchAction(`Delete ${src.name}? Coding and evidence attached to this source will also be removed.`))return;'
new='const sourceRefs=(state.allCodingRefs||state.codingRefs).filter(r=>r.sourceId===sourceId).length,sourceNotes=(state.annotations||[]).filter(a=>a.sourceId===sourceId).length,sourceMemos=state.memos.filter(m=>m.targetType===\'source\'&&m.targetId===sourceId).length,participantLabel=state.participants.find(p=>(p.internalId||p.id)===src.participantId)?.id||null;if(!await confirmResearchAction(`Delete ${src.name}?`,`${sourceRefs} coded passage${sourceRefs===1?\'\':\'s\'}, ${sourceNotes} annotation${sourceNotes===1?\'\':\'s\'} and ${sourceMemos} source memo${sourceMemos===1?\'\':\'s\'} are linked to this source${participantLabel?` and its ${participantLabel} relationship`:\'\'}. Trace will remove those source-linked records with the source.`))return;'
if old not in s:
    raise SystemExit('source delete warning anchor missing')
s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
css=cssp.read_text(encoding='utf-8')
if '/* UX_V2_PHASE7_TRUST_STATES */' not in css:
    css += r'''

/* UX_V2_PHASE7_TRUST_STATES */
.technical-details,.import-error-details{margin-top:12px;border-top:1px solid var(--line);padding-top:10px;color:var(--muted)}.technical-details summary,.import-error-details summary{cursor:pointer;font-weight:700;color:var(--text)}.technical-details pre{white-space:pre-wrap;word-break:break-word;max-height:180px;overflow:auto;background:var(--panel2);padding:10px;border-radius:7px;font-size:12px}.import-error-details code{display:block;white-space:normal;word-break:break-word;margin-top:6px;font-size:12px}.error-state-modal .modal-note,.research-notice .modal-note{line-height:1.55}
'''
    cssp.write_text(css,encoding='utf-8')
t=tp.read_text(encoding='utf-8')
for a in [
    "assert 'function showActionError' in app\n",
    "assert 'Technical details' in app\n",
    "assert 'RESEARCH DATA PROTECTION' in app\n",
    "assert 'UX_V2_PHASE7_TRUST_STATES' in css\n",
]:
    if a not in t:
        t+='\n'+a
tp.write_text(t,encoding='utf-8')
print('Phase 7 trust/error/destructive-state hotfix applied')
