from pathlib import Path

app_path=Path('src/app.js')
rust_path=Path('src-tauri/src/lib.rs')
css_path=Path('src/styles.css')
test_path=Path('tests/ux_foundation_v2_contract.py')
app=app_path.read_text(encoding='utf-8')
rust=rust_path.read_text(encoding='utf-8')

old="const uiDefaults = {resumeLastProject:false,rememberLayout:true,resumeExactWorkspace:false,gettingStartedDismissed:false,lastProjectRoot:null};"
new="const uiDefaults = {resumeLastProject:false,rememberLayout:true,resumeExactWorkspace:false,gettingStartedDismissed:false,lastProjectRoot:null,recentProjects:[]};"
if old in app:
    app=app.replace(old,new,1)
elif 'recentProjects:[]' not in app:
    raise SystemExit('UI defaults anchor missing')

old=r'''function saveUiPrefs(){try{localStorage.setItem(UI_PREFS_KEY,JSON.stringify(uiPrefs))}catch{}}
function projectHasContent(){return !!(state.importedSources.length||state.codes.length||state.themes.length||state.participants.length||(state.allCodingRefs||[]).length)}'''
new=r'''function saveUiPrefs(){try{localStorage.setItem(UI_PREFS_KEY,JSON.stringify(uiPrefs))}catch{}}
function rememberRecentProject(handle){
  const root=handle?.root||nativeBridge.root;if(!root)return;
  const p=handle?.snapshot?.project||state.project||{};
  const entry={root,title:p.title||'Untitled project',methodology:p.methodology||'',sourceCount:Number(p.source_count??state.importedSources.length??0),codeCount:Number(p.code_count??state.codes.length??0),lastOpened:Date.now()};
  uiPrefs.recentProjects=[entry,...(uiPrefs.recentProjects||[]).filter(x=>x&&x.root!==root)].slice(0,20);uiPrefs.lastProjectRoot=root;saveUiPrefs();
}
function forgetRecentProject(root){uiPrefs.recentProjects=(uiPrefs.recentProjects||[]).filter(x=>x?.root!==root);if(uiPrefs.lastProjectRoot===root)uiPrefs.lastProjectRoot=null;saveUiPrefs();}
function projectHasContent(){return !!(state.importedSources.length||state.codes.length||state.themes.length||state.participants.length||(state.allCodingRefs||[]).length)}'''
if old in app:
    app=app.replace(old,new,1)
elif 'function rememberRecentProject(handle)' not in app:
    raise SystemExit('Recent-project helper anchor missing')

old="async function refreshHomeProjects(){if(!nativeBridge.available){homeProjects=[];if(homeMode)render();return}try{homeProjects=await nativeBridge.invoke('list_local_projects');if(homeMode)render()}catch(err){console.warn('Could not list Trace projects',err);homeProjects=[]}}"
new=r'''async function refreshHomeProjects(){
  if(!nativeBridge.available){homeProjects=[];if(homeMode)render();return}
  try{
    const live=await nativeBridge.invoke('list_local_projects')||[],byRoot=new Map(live.map(x=>[x.root,x]));
    for(const h of live){const p=h.snapshot?.project||{};const remembered=(uiPrefs.recentProjects||[]).find(x=>x.root===h.root);if(!remembered||remembered.title!==p.title||remembered.sourceCount!==p.source_count||remembered.codeCount!==p.code_count){const entry={root:h.root,title:p.title||'Untitled project',methodology:p.methodology||'',sourceCount:Number(p.source_count||0),codeCount:Number(p.code_count||0),lastOpened:remembered?.lastOpened||0};uiPrefs.recentProjects=[entry,...(uiPrefs.recentProjects||[]).filter(x=>x.root!==h.root)].slice(0,20)}}
    const missing=(uiPrefs.recentProjects||[]).filter(x=>x?.root&&!byRoot.has(x.root)).map(x=>({root:x.root,unavailable:true,recent:x,snapshot:{project:{title:x.title||'Unavailable project',methodology:x.methodology||'',source_count:Number(x.sourceCount||0),code_count:Number(x.codeCount||0)}}}));
    homeProjects=[...live,...missing];saveUiPrefs();if(homeMode)render();
  }catch(err){console.warn('Could not list Trace projects',err);homeProjects=(uiPrefs.recentProjects||[]).map(x=>({root:x.root,unavailable:true,recent:x,snapshot:{project:{title:x.title||'Unavailable project',methodology:x.methodology||'',source_count:Number(x.sourceCount||0),code_count:Number(x.codeCount||0)}}}));if(homeMode)render()}
}'''
if old in app:
    app=app.replace(old,new,1)
elif 'unavailable:true,recent:x' not in app:
    raise SystemExit('refreshHomeProjects anchor missing')

old="<div class=\"recent-grid\">${projects.length?projects.map((h,i)=>`<button class=\"recent-project\" data-home-project=\"${i}\"><span class=\"recent-icon\">${icon('folder',20)}</span><div><b>${escapeHtml(h.snapshot.project.title)}</b><small>${escapeHtml(h.snapshot.project.methodology||'Qualitative research')} · ${h.snapshot.project.source_count} source${h.snapshot.project.source_count===1?'':'s'} · ${h.snapshot.project.code_count} codes</small></div><em>Open →</em></button>`).join(''):`<div class=\"home-empty\"><b>No local projects yet</b><span>Create one when you are ready. Trace will not seed demo research into production.</span></div>`}</div>"
new="<div class=\"recent-grid\">${projects.length?projects.map((h,i)=>h.unavailable?`<article class=\"recent-project unavailable-project\"><span class=\"recent-icon\">${icon('folder',20)}</span><div><b>${escapeHtml(h.snapshot.project.title)}</b><small>Project location is unavailable · ${escapeHtml(h.root||'Previous location')}</small><div class=\"missing-project-actions\"><button class=\"secondary tiny\" data-locate-project=\"${i}\">Locate</button><button class=\"text-btn\" data-remove-project=\"${i}\">Remove from list</button><button class=\"text-btn\" data-restore-project=\"${i}\">Restore backup</button></div></div><em>Needs attention</em></article>`:`<button class=\"recent-project\" data-home-project=\"${i}\"><span class=\"recent-icon\">${icon('folder',20)}</span><div><b>${escapeHtml(h.snapshot.project.title)}</b><small>${escapeHtml(h.snapshot.project.methodology||'Qualitative research')} · ${h.snapshot.project.source_count} source${h.snapshot.project.source_count===1?'':'s'} · ${h.snapshot.project.code_count} codes</small></div><em>Open →</em></button>`).join(''):`<div class=\"home-empty\"><b>No local projects yet</b><span>Create one when you are ready. Trace will not seed demo research into production.</span></div>`}</div>"
if old in app:
    app=app.replace(old,new,1)
elif 'data-locate-project' not in app:
    raise SystemExit('Home recent-grid anchor missing')

old="async function switchToNativeHandle(handle){\n  await endNativeSession();recoveryNotice=null;hydrateFromNativeSnapshot(handle);homeMode=false;uiPrefs.lastProjectRoot=handle?.root||nativeBridge.root||null;saveUiPrefs();if(!state.importedSources.length)state.activeSection='Overview';await beginNativeSession();await refreshNativeBackups();await refreshActionAvailability();render();\n}"
new="async function switchToNativeHandle(handle){\n  await endNativeSession();recoveryNotice=null;hydrateFromNativeSnapshot(handle);homeMode=false;rememberRecentProject(handle);if(!state.importedSources.length)state.activeSection='Overview';await beginNativeSession();await refreshNativeBackups();await refreshActionAvailability();render();\n}"
if old in app:
    app=app.replace(old,new,1)
elif 'rememberRecentProject(handle)' not in app:
    raise SystemExit('switchToNativeHandle anchor missing')

anchor="async function openProjectSwitcher(){goHome();}"
if 'async function locateLocalProject(' not in app:
    helpers=r'''async function pickAndOpenLocalProject(){
  if(!nativeBridge.available){showToast('Opening a project folder requires the installed desktop app.');return null}
  try{const handle=await nativeBridge.invoke('pick_local_project_folder');if(!handle)return null;await switchToNativeHandle(handle);showToast('Project opened');return handle}catch(err){showActionError?.('Project could not be opened',err,'Choose a Trace project folder containing trace.sqlite, or restore a verified backup.');return null}
}
async function locateLocalProject(index){const missing=homeProjects[index];const oldRoot=missing?.root;const handle=await pickAndOpenLocalProject();if(handle&&oldRoot&&handle.root!==oldRoot){forgetRecentProject(oldRoot);rememberRecentProject(handle)}}
function removeUnavailableProject(index){const item=homeProjects[index];if(!item?.unavailable)return;forgetRecentProject(item.root);homeProjects=homeProjects.filter((_,i)=>i!==index);render()}
async function restoreUnavailableProject(index){const item=homeProjects[index];if(!item?.unavailable)return;if(state.backups?.length){openBackupSettings();return}document.querySelector('#trace-import')?.click()}

'''
    if anchor not in app: raise SystemExit('Project switcher anchor missing')
    app=app.replace(anchor,helpers+anchor,1)

old="document.querySelector('#home-open')?.addEventListener('click',()=>document.querySelector('[data-home-project]')?.focus());"
new="document.querySelector('#home-open')?.addEventListener('click',pickAndOpenLocalProject);"
if old in app:
    app=app.replace(old,new,1)
elif "addEventListener('click',pickAndOpenLocalProject)" not in app:
    raise SystemExit('Home Open binding anchor missing')

old="document.querySelectorAll('[data-home-project]').forEach(btn=>btn.addEventListener('click',async()=>{const h=homeProjects[Number(btn.dataset.homeProject)];if(h)await switchToNativeHandle(h)}));"
new=old+"\n  document.querySelectorAll('[data-locate-project]').forEach(btn=>btn.addEventListener('click',()=>locateLocalProject(Number(btn.dataset.locateProject))));document.querySelectorAll('[data-remove-project]').forEach(btn=>btn.addEventListener('click',()=>removeUnavailableProject(Number(btn.dataset.removeProject))));document.querySelectorAll('[data-restore-project]').forEach(btn=>btn.addEventListener('click',()=>restoreUnavailableProject(Number(btn.dataset.restoreProject))));"
if old in app and 'data-locate-project]' not in app:
    app=app.replace(old,new,1)

rust_anchor='#[tauri::command]\nasync fn pick_whisper_model(app:tauri::AppHandle)->Result<Option<WhisperModelInfo>,String>{'
if 'async fn pick_local_project_folder' not in rust:
    fn=r'''#[tauri::command]
async fn pick_local_project_folder(app:tauri::AppHandle)->Result<Option<NativeProjectHandle>,String>{
    use tauri_plugin_dialog::DialogExt;
    let chosen=app.dialog().file().set_title("Open Trace project").blocking_pick_folder();
    match chosen {
        None=>Ok(None),
        Some(folder)=>{
            let path=folder.into_path().map_err(|_|"The selected project is not a normal local folder.".to_string())?;
            if !path.join("trace.sqlite").is_file(){return Err("That folder does not contain a Trace project. Choose the folder that contains trace.sqlite.".into());}
            let root=path.to_string_lossy().to_string();
            let snapshot=db::load_snapshot(&root).map_err(|e|format!("Trace found the project database but could not open it safely: {e}"))?;
            Ok(Some(NativeProjectHandle{root,snapshot}))
        }
    }
}

'''
    if rust_anchor not in rust: raise SystemExit('Rust picker insertion anchor missing')
    rust=rust.replace(rust_anchor,fn+rust_anchor,1)

handler='create_trace_project,create_local_project,list_local_projects,load_trace_project,update_project_details,'
if 'pick_local_project_folder' not in rust.split('.invoke_handler',1)[-1]:
    if handler not in rust: raise SystemExit('Rust invoke handler anchor missing')
    rust=rust.replace(handler,'create_trace_project,create_local_project,list_local_projects,pick_local_project_folder,load_trace_project,update_project_details,',1)

app_path.write_text(app,encoding='utf-8');rust_path.write_text(rust,encoding='utf-8')
css=css_path.read_text(encoding='utf-8')
if '/* UX_V2_RECENT_PROJECT_RECOVERY */' not in css:
    css += r'''

/* UX_V2_RECENT_PROJECT_RECOVERY */
.unavailable-project{border-style:dashed!important;cursor:default!important}.unavailable-project>em{color:var(--warning,#a15c00);font-style:normal;font-weight:700}.missing-project-actions{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:9px}.missing-project-actions button{min-height:30px}.unavailable-project small{overflow-wrap:anywhere}
'''
    css_path.write_text(css,encoding='utf-8')

t=test_path.read_text(encoding='utf-8')
for assertion in [
    "assert 'recentProjects:[]' in app\n",
    "assert 'pickAndOpenLocalProject' in app\n",
    "assert 'data-locate-project' in app\n",
    "assert 'Remove from list' in app\n",
    "assert 'Restore backup' in app\n",
    "assert 'pick_local_project_folder' in rust\n",
    "assert 'UX_V2_RECENT_PROJECT_RECOVERY' in css\n",
]:
    if assertion not in t:t+='\n'+assertion
# expose Rust file to the existing static contract script if not already present
if "rust = Path('src-tauri/src/lib.rs').read_text" not in t:
    t="from pathlib import Path\n"+t.replace('from pathlib import Path\n','',1)
    insert="rust = Path('src-tauri/src/lib.rs').read_text(encoding='utf-8')\n"
    pos=t.find("app = ")
    if pos<0: raise SystemExit('Static contract app load anchor missing')
    t=t[:pos]+insert+t[pos:]
test_path.write_text(t,encoding='utf-8')
print('Recent-project locate/remove/restore resilience hotfix applied')
