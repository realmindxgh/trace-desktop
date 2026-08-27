from pathlib import Path

app_path=Path('src/app.js')
contract_path=Path('tests/ux_foundation_v2_contract.py')
browser_path=Path('tests/ux_foundation_v2.mjs')
app=app_path.read_text(encoding='utf-8')
contract=contract_path.read_text(encoding='utf-8')

old="const uiDefaults = {resumeLastProject:false,rememberLayout:true,resumeExactWorkspace:false,gettingStartedDismissed:false,lastProjectRoot:null,recentProjects:[]};"
new="const uiDefaults = {resumeLastProject:false,rememberLayout:true,resumeExactWorkspace:false,gettingStartedDismissed:false,lastProjectRoot:null,recentProjects:[],defaultTranscriptionLanguage:'auto',defaultTranscriptionModel:null,projectPreferences:{}};"
if old in app:
    app=app.replace(old,new,1)
elif 'defaultTranscriptionLanguage' not in app:
    raise SystemExit('UI defaults anchor changed')

anchor="function saveUiPrefs(){try{localStorage.setItem(UI_PREFS_KEY,JSON.stringify(uiPrefs))}catch{}}"
addition="""function saveUiPrefs(){try{localStorage.setItem(UI_PREFS_KEY,JSON.stringify(uiPrefs))}catch{}}
function getProjectPreferences(projectId=state.project?.id){const id=projectId||'unopened';return {participantTerm:'Participant',exportFilePrefix:safeName(state.project?.title||'Trace_project'),includeEvidenceAppendix:true,...(uiPrefs.projectPreferences?.[id]||{})};}
function setProjectPreferences(prefs,projectId=state.project?.id){const id=projectId||'unopened';uiPrefs.projectPreferences={...(uiPrefs.projectPreferences||{}),[id]:{...getProjectPreferences(id),...prefs}};saveUiPrefs();}
function effectiveTranscriptionModel(){return state.transcriptionModel||uiPrefs.defaultTranscriptionModel||null;}
function effectiveTranscriptionLanguage(){return state.transcriptionLanguage||uiPrefs.defaultTranscriptionLanguage||'auto';}"""
if anchor in app:
    app=app.replace(anchor,addition,1)
elif 'function getProjectPreferences(' not in app:
    raise SystemExit('UI preference helper anchor changed')

app=app.replace("const model=state.transcriptionModel;\n  if(!src||!['audio','video'].includes(src.kind))", "const model=effectiveTranscriptionModel();\n  if(!src||!['audio','video'].includes(src.kind))",1)
app=app.replace("const language=(document.querySelector('#transcription-language')?.value||state.transcriptionLanguage||'auto').trim()||'auto';", "const language=(document.querySelector('#transcription-language')?.value||effectiveTranscriptionLanguage()).trim()||'auto';",1)
app=app.replace("const model=state.transcriptionModel;\n  const busy=transcriptionBusySourceId===src.id;", "const model=effectiveTranscriptionModel();\n  const busy=transcriptionBusySourceId===src.id;",1)
app=app.replace("value=\"${escapeHtml(state.transcriptionLanguage||'auto')}\"", "value=\"${escapeHtml(effectiveTranscriptionLanguage())}\"",1)

media_anchor="function importQueueItem(file,status='queued',message='Waiting'){return {id:crypto.randomUUID(),name:file.name,size:file.size||0,status,message};}"
media_fn=r'''function offerMediaImportChoice(sourceId){
  const src=state.importedSources.find(x=>x.id===sourceId);if(!src||!['audio','video'].includes(src.kind))return Promise.resolve('added');
  return new Promise(resolve=>{const root=document.querySelector('#modal-root');root.innerHTML=`<div class="modal-backdrop"><section class="small-modal media-import-choice" role="dialog" aria-modal="true" aria-labelledby="media-import-choice-title"><button class="modal-close" id="media-choice-close" aria-label="Add without transcription">${icon('close',18)}</button><span class="eyebrow">${escapeHtml(src.kind.toUpperCase())} IMPORTED</span><h2 id="media-import-choice-title">What would you like Trace to do next?</h2><p class="modal-note"><b>${escapeHtml(src.name)}</b> is safely in the project. Transcription runs locally on this computer and never uploads the recording.</p><div class="media-import-choice-actions"><button class="secondary" id="media-add-without-transcription">Add without transcription</button><button class="primary" id="media-transcribe-now">Transcribe now</button></div></section></div>`;
    const finish=value=>{root.innerHTML='';resolve(value)};
    root.querySelector('#media-choice-close').onclick=()=>finish('added');
    root.querySelector('#media-add-without-transcription').onclick=()=>finish('added');
    root.querySelector('#media-transcribe-now').onclick=async()=>{root.innerHTML='';state.activeSourceId=sourceId;activateSource(sourceId,false);render();if(!effectiveTranscriptionModel()?.path)await chooseWhisperModel();if(effectiveTranscriptionModel()?.path)await transcribeActiveSource();resolve('transcribed');};
    activateModalAccessibility(root);
  });
}'''
if media_anchor in app:
    app=app.replace(media_anchor,media_fn+'\n'+media_anchor,1)
elif 'function offerMediaImportChoice(' not in app:
    raise SystemExit('Media-choice insertion anchor changed')

old="if(nativeBridge.available&&nativeBridge.root){const id=await nativeBridge.invoke('import_binary_source',{root:nativeBridge.root,input:{name:f.name,participant_label:state.activeParticipant||null,kind,bytes_base64:bytesBase64}});await reloadNativeProject();state.activeSourceId=id;activateSource(id,false);await loadMediaForSource(id);await maybeAutoBackup();return;}"
new="if(nativeBridge.available&&nativeBridge.root){const id=await nativeBridge.invoke('import_binary_source',{root:nativeBridge.root,input:{name:f.name,participant_label:state.activeParticipant||null,kind,bytes_base64:bytesBase64}});await reloadNativeProject();state.activeSourceId=id;activateSource(id,false);await loadMediaForSource(id);await maybeAutoBackup();if(['audio','video'].includes(kind))await offerMediaImportChoice(id);return;}"
if old in app:
    app=app.replace(old,new,1)
elif "await offerMediaImportChoice(id)" not in app:
    raise SystemExit('Binary import media-choice anchor changed')

start=app.find('async function openProjectSettings(){')
end=app.find('\nfunction openCommandPalette(){',start)
if start<0 or end<0: raise SystemExit('Project Settings function boundaries changed')
new_project=r'''async function openProjectSettings(){
  if(!state.project?.id)return;
  const prefs=getProjectPreferences();
  const root=document.querySelector('#modal-root');root.innerHTML=`<div class="modal-backdrop"><section class="project-modal settings-modal"><button class="modal-close" id="project-settings-close">${icon('close',18)}</button><span class="eyebrow">PROJECT SETTINGS</span><h2>Study details and project-specific behaviour.</h2><div class="form-grid"><label>Project title<input id="project-title-input" value="${escapeHtml(state.project.title||'')}"></label><label>Methodology<input id="project-method-input" value="${escapeHtml(state.project.methodology||'')}" placeholder="Optional"></label><label class="span2">Research focus / notes<textarea id="project-focus-input" placeholder="Optional project description or study notes">${escapeHtml(state.project.description||'')}</textarea></label><label>Participant / case terminology<input id="project-participant-term" value="${escapeHtml(prefs.participantTerm)}" placeholder="Participant"></label><label>Findings export file prefix<input id="project-export-prefix" value="${escapeHtml(prefs.exportFilePrefix)}" placeholder="${escapeHtml(safeName(state.project.title||'Trace_project'))}"></label><label class="span2 check-label"><input id="project-export-evidence" type="checkbox" ${prefs.includeEvidenceAppendix?'checked':''}> Include a Trace evidence appendix in findings exports</label></div><div class="project-settings-links"><button class="secondary" id="project-settings-participants">Manage participants & attributes</button><button class="secondary" id="project-settings-backups">Backup settings</button></div><div class="modal-actions"><button class="secondary" id="project-settings-cancel">Cancel</button><button class="primary" id="project-settings-save">Save project settings</button></div></section></div>`;
  const close=()=>root.innerHTML='';root.querySelector('#project-settings-close').onclick=close;root.querySelector('#project-settings-cancel').onclick=close;root.querySelector('#project-settings-participants').onclick=()=>{close();state.activeSection='Data';state.dataContext='participants';render()};root.querySelector('#project-settings-backups').onclick=()=>{close();openBackupSettings()};
  root.querySelector('#project-settings-save').onclick=async()=>{const title=root.querySelector('#project-title-input').value.trim();if(!title)return;const methodology=root.querySelector('#project-method-input').value.trim()||null;const description=root.querySelector('#project-focus-input').value.trim();const participantTerm=root.querySelector('#project-participant-term').value.trim()||'Participant';const exportFilePrefix=root.querySelector('#project-export-prefix').value.trim()||safeName(title);const includeEvidenceAppendix=!!root.querySelector('#project-export-evidence').checked;try{if(nativeBridge.available&&nativeBridge.root){await nativeBridge.invoke('update_project_details',{root:nativeBridge.root,input:{title,methodology}});await reloadNativeProject()}else{state.project.title=title;state.project.methodology=methodology}state.project.description=description;setProjectPreferences({participantTerm,exportFilePrefix,includeEvidenceAppendix});saveState('Updated project settings');close();render();showToast('Project settings saved')}catch(err){showActionError('Project settings could not be saved',err,'Trace could not save these project settings. Try again without closing the project.')}};activateModalAccessibility(root);
}'''
app=app[:start]+new_project+app[end:]

old="const participants=snap.participants.map((p,i)=>({\n    id:p.label || `Participant ${i+1}`,"
new="const participantTerm=getProjectPreferences(snap.project.id).participantTerm||'Participant';\n  const participants=snap.participants.map((p,i)=>({\n    id:p.label || `${participantTerm} ${i+1}`,"
if old in app:
    app=app.replace(old,new,1)
elif 'const participantTerm=getProjectPreferences(snap.project.id)' not in app:
    raise SystemExit('Participant terminology hydrate anchor changed')

old="function exportFindingsMarkdown(){const sections=state.findingsSections.slice().sort((a,b)=>(a.title||'').localeCompare(b.title||''));if(!sections.length){showToast('Save at least one findings section first');return;}const md=`# ${state.project.title}\n\n${sections.map(sec=>`## ${sec.title}\n\n${sec.body||''}`).join('\n\n')}`;downloadBlob(`${safeName(state.project.title)}_findings.md`,new Blob([md],{type:'text/markdown'}));showToast('Findings Markdown exported');}"
new="function exportFindingsMarkdown(){const sections=state.findingsSections.slice().sort((a,b)=>(a.title||'').localeCompare(b.title||''));if(!sections.length){showToast('Save at least one findings section first');return;}const prefs=getProjectPreferences(),evidence=prefs.includeEvidenceAppendix?(state.findingsEvidence||[]):[];const appendix=evidence.length?`\n\n## Trace evidence appendix\n\n${evidence.map((x,i)=>`${i+1}. ${x.evidenceType||'evidence'} · ${x.evidenceId||'unknown'}`).join('\n')}`:'';const md=`# ${state.project.title}\n\n${sections.map(sec=>`## ${sec.title}\n\n${sec.body||''}`).join('\n\n')}${appendix}`;downloadBlob(`${safeName(prefs.exportFilePrefix||state.project.title)}_findings.md`,new Blob([md],{type:'text/markdown'}));showToast('Findings Markdown exported');}"
if old in app:
    app=app.replace(old,new,1)
elif 'Trace evidence appendix' not in app:
    raise SystemExit('Findings export settings anchor changed')

start=app.find('async function openAppSettings(){')
end=app.find('\n\nasync function pickAndOpenLocalProject()',start)
if start<0 or end<0: raise SystemExit('Application Settings function boundaries changed')
new_app=r'''async function openAppSettings(){
  let release={configured:false,current_version:'0.12.1',channel:'stable',message:'Signed automatic updates are prepared for release infrastructure.'};if(nativeBridge.available){try{release=await nativeBridge.invoke('release_channel_status')}catch{}}
  const modal=document.querySelector('#modal-root'),defaultModel=uiPrefs.defaultTranscriptionModel;
  modal.innerHTML=`<div class="modal-backdrop"><section class="project-modal settings-modal"><button class="modal-close" id="settings-close">${icon('close',18)}</button><div class="settings-head"><img src="./assets/trace-mark.png" alt=""><div><span class="eyebrow">APPLICATION SETTINGS</span><h2>How Trace behaves on this computer.</h2><p>Project-specific study details, participants, exports and backup policy live in Project Settings.</p></div></div><div class="settings-grid"><article class="settings-card display-settings-card"><span class="settings-icon">${icon('palette',18)}</span><div><b>Interface size</b><p>Choose a comfortable reading density without relying on Windows scaling alone.</p></div><div class="display-size-picker"><button data-display-size="compact" class="${state.displaySize==='compact'?'active':''}">Compact</button><button data-display-size="comfortable" class="${(state.displaySize||'comfortable')==='comfortable'?'active':''}">Comfortable</button><button data-display-size="large" class="${state.displaySize==='large'?'active':''}">Large</button></div></article><article class="settings-card"><span class="settings-icon">${icon('exchange',18)}</span><div><b>Startup</b><p>Home is the default. Resume the last project only when you explicitly opt in.</p></div><label class="check-label inline-check"><input id="resume-last-project" type="checkbox" ${uiPrefs.resumeLastProject?'checked':''}> Resume my last project on startup</label></article><article class="settings-card workspace-memory-card"><span class="settings-icon">${icon('menu',18)}</span><div><b>Workspace memory</b><p>Layout memory and exact-workspace resume are separate. Keep pane sizes without reopening a transient source or selection unless you explicitly choose to.</p></div><label class="check-label inline-check"><input id="remember-layout" type="checkbox" ${uiPrefs.rememberLayout?'checked':''}> Remember my layout between sessions</label><label class="check-label inline-check"><input id="resume-exact-workspace" type="checkbox" ${uiPrefs.resumeExactWorkspace?'checked':''}> Resume exactly where I was inside the project</label></article><article class="settings-card transcription-defaults-card"><span class="settings-icon">${icon('data',18)}</span><div><b>Default local transcription</b><p>Set defaults for new audio/video sources. A project can still override these while transcribing.</p></div><label>Default language code<input id="default-transcription-language" value="${escapeHtml(uiPrefs.defaultTranscriptionLanguage||'auto')}" placeholder="auto, en, fr, tw…"></label><div class="default-model-actions"><button class="secondary tiny" id="default-whisper-model">${defaultModel?`Change ${escapeHtml(defaultModel.name)}`:'Choose default Whisper model'}</button>${defaultModel?'<button class="text-btn" id="clear-default-whisper">Clear default</button>':''}</div></article><article class="settings-card"><span class="settings-icon">${icon('download',18)}</span><div><b>Updates · ${escapeHtml(release.channel||'stable')}</b><p>${escapeHtml(release.message||'Update status unavailable.')}</p></div><span class="settings-status ${release.configured?'ready':'quiet'}">Version ${escapeHtml(release.current_version||'0.12.1')}</span></article><article class="settings-card"><span class="settings-icon">${icon('bug',18)}</span><div><b>Privacy-safe diagnostics</b><p>Export technical health information without transcript text, coded quotations or participant attribute values.</p></div><button class="secondary tiny" id="export-diagnostics">Export diagnostics</button></article></div><div class="modal-actions"><button class="primary" id="settings-done">Done</button></div></section></div>`;
  const close=()=>modal.innerHTML='';modal.querySelector('#settings-close').onclick=close;modal.querySelector('#settings-done').onclick=()=>{uiPrefs.resumeLastProject=!!modal.querySelector('#resume-last-project')?.checked;uiPrefs.rememberLayout=!!modal.querySelector('#remember-layout')?.checked;uiPrefs.resumeExactWorkspace=!!modal.querySelector('#resume-exact-workspace')?.checked;uiPrefs.defaultTranscriptionLanguage=(modal.querySelector('#default-transcription-language')?.value||'auto').trim()||'auto';saveUiPrefs();close()};
  modal.querySelectorAll('[data-display-size]').forEach(btn=>btn.onclick=()=>{state.displaySize=btn.dataset.displaySize;saveState('Changed display size');document.documentElement.dataset.textSize=state.displaySize;modal.querySelectorAll('[data-display-size]').forEach(x=>x.classList.toggle('active',x.dataset.displaySize===state.displaySize))});
  modal.querySelector('#default-whisper-model').onclick=async()=>{if(!nativeBridge.available){showToast('Default model selection is available in the installed desktop app.');return;}try{const model=await nativeBridge.invoke('pick_whisper_model');if(!model)return;uiPrefs.defaultTranscriptionModel={path:model.path,name:model.name,sizeBytes:model.size_bytes};uiPrefs.defaultTranscriptionLanguage=(modal.querySelector('#default-transcription-language')?.value||'auto').trim()||'auto';saveUiPrefs();close();openAppSettings()}catch(err){showActionError('Default Whisper model could not be saved',err,'Choose a valid local Whisper model file and try again.')}};
  modal.querySelector('#clear-default-whisper')?.addEventListener('click',()=>{uiPrefs.defaultTranscriptionModel=null;saveUiPrefs();close();openAppSettings()});
  modal.querySelector('#export-diagnostics').onclick=async()=>{try{if(nativeBridge.available&&nativeBridge.root){const r=await nativeBridge.invoke('export_diagnostic_bundle',{root:nativeBridge.root});showToast(`Diagnostics saved to ${r.file_name}`)}else showToast('Diagnostics are available in the installed desktop app.')}catch(err){showActionError('Diagnostics could not be exported',err,'Trace could not create the privacy-safe diagnostics bundle.')}};activateModalAccessibility(modal);
}'''
app=app[:start]+new_app+app[end:]

app_path.write_text(app,encoding='utf-8')
for assertion in [
    "assert 'Transcribe now' in app and 'Add without transcription' in app\n",
    "assert 'default-transcription-language' in app and 'default-whisper-model' in app\n",
    "assert 'project-participant-term' in app and 'project-export-prefix' in app and 'project-export-evidence' in app\n",
    "assert 'function effectiveTranscriptionModel()' in app\n",
    "assert 'Trace evidence appendix' in app\n",
]:
    if assertion not in contract: contract+='\n'+assertion
contract_path.write_text(contract,encoding='utf-8')

if browser_path.exists():
    b=browser_path.read_text(encoding='utf-8')
    if 'async function projectAndTranscriptionSettingsUx()' not in b:
        fn=r'''

async function projectAndTranscriptionSettingsUx(){
  const ctx=await browser.newContext({viewport:{width:1440,height:900}});
  await ctx.addInitScript(()=>localStorage.setItem('trace-v010-state',JSON.stringify({project:{id:'settings-project',title:'Settings study',methodology:'RTA',codingMode:'manual',researchQuestions:[],researchQuestionRecords:[]},activeSection:'Overview',participants:[],transcript:[],importedSources:[],codes:[],coders:[],codingRefs:[],allCodingRefs:[],memos:[],annotations:[],themes:[],findingsSections:[],findingsEvidence:[],sourceProperties:[],sourceCollections:[],importQueue:[],backups:[],audit:[],mediaSelections:[],mediaCodings:[],mediaPayloads:{},savedAt:Date.now()})));
  const page=await ctx.newPage();await page.goto(base,{waitUntil:'networkidle'});
  await page.click('#rail-settings');
  if(!await page.locator('#default-transcription-language').count())errors.push('Application Settings is missing default transcription language');
  if(!await page.locator('#default-whisper-model').count())errors.push('Application Settings is missing default Whisper model control');
  await page.click('#settings-close');
  await page.click('#project-settings');
  if(!await page.locator('#project-participant-term').count())errors.push('Project Settings is missing participant/case configuration');
  if(!await page.locator('#project-export-prefix').count())errors.push('Project Settings is missing project-specific export configuration');
  if(!await page.locator('#project-export-evidence').count())errors.push('Project Settings is missing evidence-export preference');
  await page.click('#project-settings-close');
  await ctx.close();
}
'''
        needle='await desktopInteractionUx();await browser.close();'
        if needle not in b: raise SystemExit('Final browser invocation anchor changed')
        b=b.replace(needle,'await desktopInteractionUx();await projectAndTranscriptionSettingsUx();await browser.close();',1)
        call='await desktopInteractionUx();await projectAndTranscriptionSettingsUx();await browser.close();'
        idx=b.rfind(call)
        if idx<0: raise SystemExit('Could not locate new browser call')
        b=b[:idx]+fn+'\n'+b[idx:]
        browser_path.write_text(b,encoding='utf-8')
print('Media import choice, transcription defaults, participant configuration and project export settings applied')
