from pathlib import Path
import json

root=Path('.')
app_path=root/'src/app.js'
css_path=root/'src/styles.css'
lib_path=root/'src-tauri/src/lib.rs'
conf_path=root/'src-tauri/tauri.conf.json'
setup_app_path=root/'setup-shell/src/app.js'
setup_rs_path=root/'setup-shell/src-tauri/src/main.rs'
trans_test_path=root/'tests/v11_transcription.py'
trans_rs_path=root/'src-tauri/src/transcription.rs'

app=app_path.read_text(encoding='utf-8')
css=css_path.read_text(encoding='utf-8')
lib=lib_path.read_text(encoding='utf-8')
setup_app=setup_app_path.read_text(encoding='utf-8')
setup_rs=setup_rs_path.read_text(encoding='utf-8')
trans_test=trans_test_path.read_text(encoding='utf-8')
trans_rs=trans_rs_path.read_text(encoding='utf-8')

# 1) Physical-UAT blocker: Tauri command arguments are camelCase at the JS boundary.
old="nativeBridge.invoke('load_source_media',{root:nativeBridge.root,source_id:sourceId})"
new="nativeBridge.invoke('load_source_media',{root:nativeBridge.root,sourceId})"
if old in app:
    app=app.replace(old,new,1)
elif new not in app:
    raise SystemExit('load_source_media invoke anchor changed')

# Audit and repair the other top-level Tauri command arguments that use Rust snake_case names.
# Nested input structs intentionally remain snake_case because serde deserializes those fields directly.
invoke_repairs={
    "nativeBridge.invoke('update_code',{root:nativeBridge.root,code_id:id,input:": "nativeBridge.invoke('update_code',{root:nativeBridge.root,codeId:id,input:",
    "nativeBridge.invoke('delete_code',{root:nativeBridge.root,code_id:code.id})": "nativeBridge.invoke('delete_code',{root:nativeBridge.root,codeId:code.id})",
    "nativeBridge.invoke('update_memo',{root:nativeBridge.root,memo_id:id,input})": "nativeBridge.invoke('update_memo',{root:nativeBridge.root,memoId:id,input})",
    "nativeBridge.invoke('delete_memo',{root:nativeBridge.root,memo_id:memo.id})": "nativeBridge.invoke('delete_memo',{root:nativeBridge.root,memoId:memo.id})",
    "nativeBridge.invoke('update_theme',{root:nativeBridge.root,theme_id:id,input})": "nativeBridge.invoke('update_theme',{root:nativeBridge.root,themeId:id,input})",
    "nativeBridge.invoke('delete_theme',{root:nativeBridge.root,theme_id:theme.id})": "nativeBridge.invoke('delete_theme',{root:nativeBridge.root,themeId:theme.id})",
    "nativeBridge.invoke('delete_coding_reference',{root:nativeBridge.root,coding_id:id})": "nativeBridge.invoke('delete_coding_reference',{root:nativeBridge.root,codingId:id})",
    "nativeBridge.invoke('delete_media_selection',{root:nativeBridge.root,selection_id:id})": "nativeBridge.invoke('delete_media_selection',{root:nativeBridge.root,selectionId:id})",
    "nativeBridge.invoke('update_source_collection',{root:nativeBridge.root,collection_id:id,name})": "nativeBridge.invoke('update_source_collection',{root:nativeBridge.root,collectionId:id,name})",
    "nativeBridge.invoke('delete_source_collection',{root:nativeBridge.root,collection_id:id})": "nativeBridge.invoke('delete_source_collection',{root:nativeBridge.root,collectionId:id})",
    "nativeBridge.invoke('unlink_findings_evidence',{root:nativeBridge.root,link_id:linkId})": "nativeBridge.invoke('unlink_findings_evidence',{root:nativeBridge.root,linkId})",
    "nativeBridge.invoke('update_annotation',{root:nativeBridge.root,annotation_id:existing.id,body})": "nativeBridge.invoke('update_annotation',{root:nativeBridge.root,annotationId:existing.id,body})",
    "nativeBridge.invoke('delete_annotation',{root:nativeBridge.root,annotation_id:id})": "nativeBridge.invoke('delete_annotation',{root:nativeBridge.root,annotationId:id})",
    "nativeBridge.invoke('import_trace_package_bytes',{file_name:f.name,bytes_base64:b64})": "nativeBridge.invoke('import_trace_package_bytes',{fileName:f.name,bytesBase64:b64})",
    "nativeBridge.invoke('set_source_participant',{root:nativeBridge.root,source_id:sourceId,participant_id:participantId})": "nativeBridge.invoke('set_source_participant',{root:nativeBridge.root,sourceId,participantId})",
    "nativeBridge.invoke('set_source_collection_member',{root:nativeBridge.root,collection_id:box.dataset.smCollection,source_id:sourceId,member:box.checked})": "nativeBridge.invoke('set_source_collection_member',{root:nativeBridge.root,collectionId:box.dataset.smCollection,sourceId,member:box.checked})",
    "nativeBridge.invoke('delete_source',{root:nativeBridge.root,source_id:sourceId})": "nativeBridge.invoke('delete_source',{root:nativeBridge.root,sourceId})",
    "nativeBridge.invoke('heartbeat_project_session',{root:nativeBridge.root,session_id:nativeSessionId,input:": "nativeBridge.invoke('heartbeat_project_session',{root:nativeBridge.root,sessionId:nativeSessionId,input:",
    "nativeBridge.invoke('end_project_session',{root:nativeBridge.root,session_id:sid})": "nativeBridge.invoke('end_project_session',{root:nativeBridge.root,sessionId:sid})",
}
for old_call,new_call in invoke_repairs.items():
    if old_call in app:
        app=app.replace(old_call,new_call,1)
    elif new_call not in app:
        raise SystemExit(f'Tauri invoke anchor changed: {old_call[:80]}')

# 2) Ship a verified balanced local Whisper model and discover it automatically.
old="let recoveryNotice = null;\nlet transcriptionBusySourceId = null;"
new="let recoveryNotice = null;\nlet transcriptionBusySourceId = null;\nlet bundledTranscriptionModel = null;"
if old in app:
    app=app.replace(old,new,1)
elif 'let bundledTranscriptionModel = null;' not in app:
    raise SystemExit('transcription global anchor changed')

old="function effectiveTranscriptionModel(){return state.transcriptionModel||uiPrefs.defaultTranscriptionModel||null;}"
new="function effectiveTranscriptionModel(){return state.transcriptionModel||uiPrefs.defaultTranscriptionModel||bundledTranscriptionModel||null;}"
if old in app:
    app=app.replace(old,new,1)
elif new not in app:
    raise SystemExit('effective transcription model anchor changed')

anchor="function effectiveTranscriptionLanguage(){return state.transcriptionLanguage||uiPrefs.defaultTranscriptionLanguage||'auto';}"
addition="""function effectiveTranscriptionLanguage(){return state.transcriptionLanguage||uiPrefs.defaultTranscriptionLanguage||'auto';}\nasync function initBundledTranscriptionModel(){\n  if(!nativeBridge.available)return;\n  try{\n    const model=await nativeBridge.invoke('bundled_whisper_model');\n    bundledTranscriptionModel=model?{path:model.path,name:model.name,sizeBytes:model.size_bytes}:null;\n  }catch(err){console.warn('Included transcription model unavailable',err);bundledTranscriptionModel=null;}\n}"""
if anchor in app:
    app=app.replace(anchor,addition,1)
elif 'async function initBundledTranscriptionModel()' not in app:
    raise SystemExit('bundled model initialization anchor changed')

old="async function initNativeBridge(){\n  if(!nativeBridge.available){homeMode=!state.project?.id;return;}\n  try{"
new="async function initNativeBridge(){\n  if(!nativeBridge.available){homeMode=!state.project?.id;return;}\n  await initBundledTranscriptionModel();\n  try{"
if old in app:
    app=app.replace(old,new,1)
elif 'await initBundledTranscriptionModel();' not in app:
    raise SystemExit('native bridge bundled-model anchor changed')

# Make bundled model feel native to the product rather than asking ordinary users to source a model file.
old="const modal=document.querySelector('#modal-root'),defaultModel=uiPrefs.defaultTranscriptionModel;"
new="const modal=document.querySelector('#modal-root'),customDefaultModel=uiPrefs.defaultTranscriptionModel,defaultModel=customDefaultModel||bundledTranscriptionModel;"
if old in app:
    app=app.replace(old,new,1)
elif 'customDefaultModel=uiPrefs.defaultTranscriptionModel' not in app:
    raise SystemExit('settings model anchor changed')

old="<div><b>Default local transcription</b><p>Set defaults for new audio/video sources. A project can still override these while transcribing.</p></div><label>Default language code<input id=\"default-transcription-language\" value=\"${escapeHtml(uiPrefs.defaultTranscriptionLanguage||'auto')}\" placeholder=\"auto, en, fr, tw…\"></label><div class=\"default-model-actions\"><button class=\"secondary tiny\" id=\"default-whisper-model\">${defaultModel?`Change ${escapeHtml(defaultModel.name)}`:'Choose default Whisper model'}</button>${defaultModel?'<button class=\"text-btn\" id=\"clear-default-whisper\">Clear default</button>':''}</div>"
new="<div><b>Local transcription</b><p>${bundledTranscriptionModel?'Trace includes a balanced offline Whisper model, so audio and video can be transcribed without extra setup.':'The included transcription model is unavailable in this build. You can still choose a compatible local Whisper model.'}</p></div><label>Default language<input id=\"default-transcription-language\" value=\"${escapeHtml(uiPrefs.defaultTranscriptionLanguage||'auto')}\" placeholder=\"auto, en, fr…\" spellcheck=\"false\"></label><div class=\"default-model-actions\"><span class=\"model-status\">${defaultModel?`${escapeHtml(defaultModel.name)} · ${formatBytes(defaultModel.sizeBytes)}`:'No model available'}</span><button class=\"secondary tiny\" id=\"default-whisper-model\">${customDefaultModel?'Change custom model':'Choose another model'}</button>${customDefaultModel?'<button class=\"text-btn\" id=\"clear-default-whisper\">Use included model</button>':''}</div>"
if old in app:
    app=app.replace(old,new,1)
elif 'Trace includes a balanced offline Whisper model' not in app:
    raise SystemExit('settings transcription card anchor changed')

# Remove the misleading Twi example until the engine/model language table explicitly verifies it.
app=app.replace('placeholder="auto, en, fr, tw…"','placeholder="auto, en, fr…"')

# 3) Repair malformed settings grid placement found on the real machine.
css_append="""
/* Physical UAT: settings controls must occupy the content column, never the 34px icon column. */
.settings-card>.inline-check{grid-column:2;justify-self:stretch;min-width:0}
.transcription-defaults-card>label,.transcription-defaults-card>.default-model-actions{grid-column:2;min-width:0}
.transcription-defaults-card>label{display:grid;gap:6px;color:var(--muted);font-size:12px}
.transcription-defaults-card>label input{width:100%;min-width:0;height:36px;border:1px solid var(--line);border-radius:9px;background:var(--panel);color:var(--ink);padding:0 10px;font:inherit;outline:0}
.transcription-defaults-card>label input:focus{border-color:color-mix(in srgb,var(--blue) 55%,var(--line));box-shadow:0 0 0 3px color-mix(in srgb,var(--blue) 10%,transparent)}
.default-model-actions{display:grid;gap:7px;justify-items:start;align-items:start}
.default-model-actions .model-status{display:block;max-width:100%;font-size:11px;line-height:1.4;color:var(--muted);overflow-wrap:anywhere}
.default-model-actions .secondary{max-width:100%;white-space:normal;text-align:left}
"""
if '.settings-card>.inline-check{grid-column:2' not in css:
    css=css.rstrip()+"\n"+css_append.strip()+"\n"

# 4) Native bundled-model discovery.
anchor="#[tauri::command]\nasync fn transcribe_source_locally(root:String,input:LocalTranscriptionInput)->Result<LocalTranscriptionResult,String>{"
command="""#[tauri::command]\nfn bundled_whisper_model(app:tauri::AppHandle)->Result<Option<WhisperModelInfo>,String>{\n    let resource_dir=app.path().resource_dir().map_err(|e|e.to_string())?;\n    let mut candidates=vec![\n        resource_dir.join(\"models\").join(\"ggml-base-q5_1.bin\"),\n        resource_dir.join(\"resources\").join(\"models\").join(\"ggml-base-q5_1.bin\"),\n    ];\n    if let Ok(exe)=std::env::current_exe(){if let Some(dir)=exe.parent(){candidates.push(dir.join(\"resources\").join(\"models\").join(\"ggml-base-q5_1.bin\"));}}\n    for path in candidates{\n        if path.is_file(){let mut info=transcription::inspect_model(&path)?;info.name=\"Trace Balanced (included)\".into();return Ok(Some(info));}\n    }\n    Ok(None)\n}\n\n#[tauri::command]\nasync fn transcribe_source_locally(root:String,input:LocalTranscriptionInput)->Result<LocalTranscriptionResult,String>{"""
if anchor in lib:
    lib=lib.replace(anchor,command,1)
elif 'fn bundled_whisper_model(' not in lib:
    raise SystemExit('native bundled model command anchor changed')

old='preview_survey_file,import_survey_file,pick_whisper_model,transcribe_source_locally,create_annotation'
new='preview_survey_file,import_survey_file,pick_whisper_model,bundled_whisper_model,transcribe_source_locally,create_annotation'
if old in lib:
    lib=lib.replace(old,new,1)
elif 'pick_whisper_model,bundled_whisper_model,transcribe_source_locally' not in lib:
    raise SystemExit('Tauri command registration anchor changed')

conf=json.loads(conf_path.read_text(encoding='utf-8'))
resources=conf.setdefault('bundle',{}).setdefault('resources',[])
model_resource='resources/models/ggml-base-q5_1.bin'
if isinstance(resources,list):
    if model_resource not in resources: resources.append(model_resource)
else:
    raise SystemExit('Unexpected tauri bundle.resources shape')
conf_path.write_text(json.dumps(conf,indent=2)+"\n",encoding='utf-8')

# 4b) A real Whisper inference smoke runs in CI when a model and spoken WAV are supplied.
trans_rs=trans_rs.replace("Use a code such as en, fr, tw, or choose Auto.", "Use a supported Whisper language code such as en or fr, or choose Auto.")
real_test="""    #[test]
    fn real_whisper_inference_when_ci_fixture_is_provided() {
        let model=match std::env::var(\"TRACE_TEST_WHISPER_MODEL\"){Ok(v)=>PathBuf::from(v),Err(_)=>return};
        let media=match std::env::var(\"TRACE_TEST_TRANSCRIPTION_WAV\"){Ok(v)=>PathBuf::from(v),Err(_)=>return};
        let decoded=decode_media(&media).expect(\"CI speech WAV should decode\");
        let (segments,_)=run_whisper(&model,&decoded.pcm_16khz_mono,None).expect(\"Whisper should transcribe the CI speech fixture\");
        let text=segments.iter().map(|s|s.text.as_str()).collect::<Vec<_>>().join(\" \ ");
        assert!(!text.trim().is_empty(),\"Whisper returned no transcript text\");
        assert!(text.split_whitespace().count()>=2,\"Whisper transcript was implausibly short: {text}\");
    }

""".replace('join(\" \\ \")','join(\" \")')
anchor="""    #[test]
    fn model_inspection_rejects_tiny_files() {"""
if 'real_whisper_inference_when_ci_fixture_is_provided' not in trans_rs:
    if anchor not in trans_rs: raise SystemExit('transcription test anchor changed')
    trans_rs=trans_rs.replace(anchor,real_test+anchor,1)

# 5) Same-version setup is a repair, not an "update" to the same number.
old='let mode=if partial{"repair"}else if existing{"update"}else{"install"}.to_string();'
new='let same_version=installed_version.as_deref().map(|v|v.trim().trim_start_matches("Trace ")==env!("CARGO_PKG_VERSION")).unwrap_or(false);\n  let mode=if partial||same_version{"repair"}else if existing{"update"}else{"install"}.to_string();'
if old in setup_rs:
    setup_rs=setup_rs.replace(old,new,1)
elif 'let same_version=installed_version.as_deref()' not in setup_rs:
    raise SystemExit('setup mode anchor changed')

old='else if partial{"This Trace installation is incomplete. Setup can repair the application files without touching research projects.".to_string()}else if existing{"Trace is already installed here. Setup will update or repair this installation without touching research projects.".to_string()}'
new='else if partial{"This Trace installation is incomplete. Setup can repair the application files without touching research projects.".to_string()}else if same_version{"This version of Trace is already installed. Setup can repair the application files and Windows integration without touching research projects.".to_string()}else if existing{"Trace is already installed here. Setup will update this installation without touching research projects.".to_string()}'
if old in setup_rs:
    setup_rs=setup_rs.replace(old,new,1)
elif 'This version of Trace is already installed.' not in setup_rs:
    raise SystemExit('setup message anchor changed')

# Frontend labels respect preflight.mode=repair throughout the setup journey.
setup_app=setup_app.replace("return maintenance?[['Welcome','Meet Trace'],['Options','Choose setup'],['Review','Confirm changes'],[state.action==='uninstall'?'Remove':'Update',state.action==='uninstall'?'Remove Trace':'Update Trace']]:baseSteps", "return maintenance?[['Welcome','Meet Trace'],['Options','Choose setup'],['Review','Confirm changes'],[state.action==='uninstall'?'Remove':modeWord(),state.action==='uninstall'?'Remove Trace':`${modeWord()} Trace`]]:baseSteps")
setup_app=setup_app.replace("p.can_install?(p.existing_install?'Ready to update':'Ready to install')", "p.can_install?(p.mode==='repair'?'Ready to repair':p.existing_install?'Ready to update':'Ready to install')")
setup_app=setup_app.replace("${state.preflight.existing_install?'Keep this location to update the existing installation.':'Trace can remember this location for future updates.'}", "${state.preflight.mode==='repair'?'Keep this location to repair the existing installation.':state.preflight.existing_install?'Keep this location to update the existing installation.':'Trace can remember this location for future updates.'}")
setup_app=setup_app.replace("Nothing will touch your research projects during ${p.existing_install?'this update':'installation'}.", "Nothing will touch your research projects during ${p.mode==='repair'?'this repair':p.existing_install?'this update':'installation'}.")
setup_app=setup_app.replace("<span>Action</span><b>${p.existing_install?'Update / repair Trace':'Install Trace'}</b>", "<span>Action</span><b>${p.mode==='repair'?'Repair Trace':p.existing_install?'Update Trace':'Install Trace'}</b>")
setup_app=setup_app.replace("state.phase=state.action==='uninstall'?'Trace removed; projects preserved':state.preflight.existing_install?'Trace updated successfully':'Installation complete'", "state.phase=state.action==='uninstall'?'Trace removed; projects preserved':state.preflight.mode==='repair'?'Trace repaired successfully':state.preflight.existing_install?'Trace updated successfully':'Installation complete'")
setup_app=setup_app.replace("[48,state.preflight.existing_install?'Updating Trace':'Installing Trace']", "[48,state.preflight.mode==='repair'?'Repairing Trace':state.preflight.existing_install?'Updating Trace':'Installing Trace']")

# Strengthen the transcription regression so this particular boundary cannot silently return.
extra="""
# Physical-UAT release blockers: real media bridge casing, included model provisioning and sane settings layout.
assert "load_source_media',{root:nativeBridge.root,sourceId}" in app
assert "import_trace_package_bytes',{fileName:f.name,bytesBase64:b64}" in app
assert 'sessionId:nativeSessionId' in app
assert 'collectionId:box.dataset.smCollection' in app
assert "unlink_findings_evidence',{root:nativeBridge.root,linkId}" in app
assert "update_annotation',{root:nativeBridge.root,annotationId:existing.id,body}" in app
assert "update_source',{root:nativeBridge.root,input:{source_id:sourceId" in app
assert "load_source_media',{root:nativeBridge.root,source_id:sourceId}" not in app
assert 'bundled_whisper_model' in lib
assert 'Trace Balanced (included)' in lib
assert 'resources/models/ggml-base-q5_1.bin' in (ROOT/'src-tauri/tauri.conf.json').read_text(encoding='utf-8')
assert '.settings-card>.inline-check{grid-column:2' in styles
assert '.transcription-defaults-card>label' in styles
"""
if 'Physical-UAT release blockers' not in trans_test:
    trans_test=trans_test.rstrip()+"\n"+extra.strip()+"\n"

app_path.write_text(app,encoding='utf-8')
css_path.write_text(css,encoding='utf-8')
lib_path.write_text(lib,encoding='utf-8')
setup_app_path.write_text(setup_app,encoding='utf-8')
setup_rs_path.write_text(setup_rs,encoding='utf-8')
trans_test_path.write_text(trans_test,encoding='utf-8')
trans_rs_path.write_text(trans_rs,encoding='utf-8')
print('Applied Trace physical-UAT release blockers hotfix.')
