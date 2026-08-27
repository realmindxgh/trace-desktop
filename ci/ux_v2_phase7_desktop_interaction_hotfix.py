from pathlib import Path

app_path=Path('src/app.js')
css_path=Path('src/styles.css')
contract_path=Path('tests/ux_foundation_v2_contract.py')
browser_path=Path('tests/ux_foundation_v2.mjs')
app=app_path.read_text(encoding='utf-8')
css=css_path.read_text(encoding='utf-8')
contract=contract_path.read_text(encoding='utf-8')

anchor="function projectHasContent(){return !!(state.importedSources.length||state.codes.length||state.themes.length||state.participants.length||(state.allCodingRefs||[]).length)}\nfunction currentSource(){return state.importedSources.find(s=>s.id===state.activeSourceId)||null}"
replacement="""function projectHasContent(){return !!(state.importedSources.length||state.codes.length||state.themes.length||state.participants.length||(state.allCodingRefs||[]).length)}
function prepareWorkspaceForOpen(){
  if(!uiPrefs.rememberLayout){state.leftRailWidth=285;state.inspectorWidth=340;state.leftRailCollapsed=false;state.inspectorCollapsed=false;}
  if(!uiPrefs.resumeExactWorkspace){state.activeSection='Overview';state.activeSourceId=null;state.openSourceTabs=[];state.activeParticipant=null;state.dataContext='sources';state.transcriptSearch='';state.dataSearch='';state.codeSearch='';state.themeSearch='';state.analysisSearch='';state.writeTarget=null;state.transcriptScrollBySource={};state.inspectorTab='info';}
}
function currentSource(){return state.importedSources.find(s=>s.id===state.activeSourceId)||null}"""
if anchor in app:
    app=app.replace(anchor,replacement,1)
elif 'function prepareWorkspaceForOpen()' not in app:
    raise SystemExit('Workspace-memory insertion anchor changed')

old="document.querySelector('#resume-current')?.addEventListener('click',()=>{homeMode=false;render()});"
new="document.querySelector('#resume-current')?.addEventListener('click',()=>{prepareWorkspaceForOpen();homeMode=false;saveState('Resumed current project');render()});"
if old in app:
    app=app.replace(old,new,1)
elif "prepareWorkspaceForOpen();homeMode=false" not in app:
    raise SystemExit('Resume-current anchor changed')

old="await endNativeSession();recoveryNotice=null;hydrateFromNativeSnapshot(handle);homeMode=false;rememberRecentProject(handle);if(!state.importedSources.length)state.activeSection='Overview';await beginNativeSession();await refreshNativeBackups();await refreshActionAvailability();render();"
new="await endNativeSession();recoveryNotice=null;hydrateFromNativeSnapshot(handle);prepareWorkspaceForOpen();homeMode=false;rememberRecentProject(handle);if(!state.importedSources.length)state.activeSection='Overview';await beginNativeSession();await refreshNativeBackups();await refreshActionAvailability();render();"
if old in app:
    app=app.replace(old,new,1)
elif 'hydrateFromNativeSnapshot(handle);prepareWorkspaceForOpen();homeMode=false' not in app:
    raise SystemExit('Native-project resume anchor changed')

startup_article="""<article class=\"settings-card\"><span class=\"settings-icon\">${icon('exchange',18)}</span><div><b>Startup</b><p>Home is the default. Resume the last project only when you explicitly opt in.</p></div><label class=\"check-label inline-check\"><input id=\"resume-last-project\" type=\"checkbox\" ${uiPrefs.resumeLastProject?'checked':''}> Resume my last project on startup</label></article>"""
memory_article=startup_article+"""<article class=\"settings-card workspace-memory-card\"><span class=\"settings-icon\">${icon('menu',18)}</span><div><b>Workspace memory</b><p>Layout memory and exact-workspace resume are separate. Keep pane sizes without reopening a transient source or selection unless you explicitly choose to.</p></div><label class=\"check-label inline-check\"><input id=\"remember-layout\" type=\"checkbox\" ${uiPrefs.rememberLayout?'checked':''}> Remember my layout between sessions</label><label class=\"check-label inline-check\"><input id=\"resume-exact-workspace\" type=\"checkbox\" ${uiPrefs.resumeExactWorkspace?'checked':''}> Resume exactly where I was inside the project</label></article>"""
if startup_article in app:
    app=app.replace(startup_article,memory_article,1)
elif 'id="remember-layout"' not in app:
    raise SystemExit('Application Settings startup anchor changed')

old="modal.querySelector('#settings-done').onclick=()=>{uiPrefs.resumeLastProject=!!modal.querySelector('#resume-last-project')?.checked;saveUiPrefs();close()};"
new="modal.querySelector('#settings-done').onclick=()=>{uiPrefs.resumeLastProject=!!modal.querySelector('#resume-last-project')?.checked;uiPrefs.rememberLayout=!!modal.querySelector('#remember-layout')?.checked;uiPrefs.resumeExactWorkspace=!!modal.querySelector('#resume-exact-workspace')?.checked;saveUiPrefs();close()};"
if old in app:
    app=app.replace(old,new,1)
elif 'uiPrefs.rememberLayout=' not in app:
    raise SystemExit('Application Settings save anchor changed')

menu_anchor="async function openProjectSwitcher(){goHome();}"
menu_code=r'''function closeTraceContextMenu(){document.querySelector('#trace-context-menu')?.remove();}
function openTraceContextMenu(items,x,y){
  closeTraceContextMenu();
  const menu=document.createElement('div');menu.id='trace-context-menu';menu.className='trace-context-menu';menu.setAttribute('role','menu');
  menu.innerHTML=items.map((item,i)=>item.separator?'<div class="context-menu-separator" role="separator"></div>':`<button role="menuitem" data-context-index="${i}" class="${item.danger?'danger':''}">${escapeHtml(item.label)}${item.shortcut?`<kbd>${escapeHtml(item.shortcut)}</kbd>`:''}</button>`).join('');
  document.body.appendChild(menu);const r=menu.getBoundingClientRect();menu.style.left=Math.max(8,Math.min(x,window.innerWidth-r.width-8))+'px';menu.style.top=Math.max(8,Math.min(y,window.innerHeight-r.height-8))+'px';
  const buttons=[...menu.querySelectorAll('[role="menuitem"]')];buttons.forEach(btn=>btn.onclick=()=>{const item=items[Number(btn.dataset.contextIndex)];closeTraceContextMenu();item?.action?.();});
  menu.addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();closeTraceContextMenu();return;}if(!['ArrowDown','ArrowUp','Home','End'].includes(e.key))return;e.preventDefault();const ix=Math.max(0,buttons.indexOf(document.activeElement));const next=e.key==='Home'?0:e.key==='End'?buttons.length-1:(ix+(e.key==='ArrowDown'?1:-1)+buttons.length)%buttons.length;buttons[next]?.focus();});
  buttons[0]?.focus();
}
function bindResearchContextMenus(){
  document.addEventListener('contextmenu',e=>{
    if(e.target.closest('input,textarea,select,[contenteditable="true"]'))return;
    const source=e.target.closest('[data-source]');if(source){e.preventDefault();const id=source.dataset.source;openTraceContextMenu([{label:'Open in Code',action:()=>{state.activeSection='Code';activateSource(id)}},{label:'Manage source…',action:()=>openSourceManager(id)},{separator:true},{label:sourceProp(id).archived?'Restore from archive':'Archive / organise…',action:()=>openSourceManager(id)}],e.clientX,e.clientY);return;}
    const codeEl=e.target.closest('[data-edit-code]');if(codeEl){e.preventDefault();const id=codeEl.dataset.editCode,code=state.codes.find(x=>x.id===id);openTraceContextMenu([{label:'Edit code…',action:()=>openCodeEditor(id)},{label:'Inspect coded evidence',action:()=>{state.analysisCodeFilter=id;state.activeSection='Analyse';render()}},{separator:true},{label:`Code: ${code?.name||'Untitled'}`,action:()=>openCodeEditor(id)}],e.clientX,e.clientY);return;}
    const themeEl=e.target.closest('.theme-card,[data-edit-theme]');if(themeEl){const id=themeEl.dataset.editTheme||themeEl.querySelector('[data-edit-theme]')?.dataset.editTheme;if(id){e.preventDefault();openTraceContextMenu([{label:'Inspect supporting evidence',action:()=>openThemeEvidence(id)},{label:'Edit theme…',action:()=>openThemeEditor(id)}],e.clientX,e.clientY);return;}}
    const collection=e.target.closest('[data-manage-collection]');if(collection){e.preventDefault();const id=collection.dataset.manageCollection;openTraceContextMenu([{label:'Manage collection…',action:()=>openCollectionEditor(id)},{label:'View sources',action:()=>{state.activeCollectionId=id;state.dataContext='sources';render()}}],e.clientX,e.clientY);}
  });
  document.addEventListener('pointerdown',e=>{if(!e.target.closest('#trace-context-menu'))closeTraceContextMenu();});
  window.addEventListener('blur',closeTraceContextMenu);
}

async function openProjectSwitcher(){goHome();}'''
if menu_anchor in app:
    app=app.replace(menu_anchor,menu_code,1)
elif 'function bindResearchContextMenus()' not in app:
    raise SystemExit('Context-menu insertion anchor changed')

old="window.addEventListener('beforeunload',()=>{endNativeSession()});\nfunction moveSourceTab(delta){"
new="window.addEventListener('beforeunload',()=>{endNativeSession()});\nbindResearchContextMenus();\nfunction moveSourceTab(delta){"
if old in app:
    app=app.replace(old,new,1)
elif 'bindResearchContextMenus();\nfunction moveSourceTab' not in app:
    raise SystemExit('Context-menu bind anchor changed')

marker='/* UX_V2_PHASE7_DESKTOP_INTERACTION */'
if marker not in css:
    css += r'''

/* UX_V2_PHASE7_DESKTOP_INTERACTION */
.trace-context-menu{position:fixed;z-index:10000;min-width:210px;max-width:320px;padding:6px;background:var(--panel);border:1px solid var(--line);border-radius:8px;box-shadow:0 16px 42px rgba(15,23,42,.20);display:grid;gap:2px}
.trace-context-menu button{min-height:34px;width:100%;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:7px 10px;border:0;border-radius:5px;background:transparent;color:var(--text);font:inherit;text-align:left;cursor:pointer}
.trace-context-menu button:hover,.trace-context-menu button:focus-visible{background:var(--panel2);outline:2px solid var(--focus,#3f6fd8);outline-offset:-2px}
.trace-context-menu button.danger{color:var(--danger,#a83232)}
.trace-context-menu kbd{font-size:12px;color:var(--muted);font-family:inherit}
.context-menu-separator{height:1px;background:var(--line);margin:4px 2px}
.workspace-memory-card{align-content:start}.workspace-memory-card .inline-check{grid-column:2 / -1;margin-top:4px}
'''

app_path.write_text(app,encoding='utf-8')
css_path.write_text(css,encoding='utf-8')
for assertion in [
    "assert 'function prepareWorkspaceForOpen()' in app\n",
    "assert 'remember-layout' in app and 'resume-exact-workspace' in app\n",
    "assert 'function openTraceContextMenu' in app and 'bindResearchContextMenus' in app\n",
    "assert 'UX_V2_PHASE7_DESKTOP_INTERACTION' in css\n",
]:
    if assertion not in contract: contract += '\n'+assertion
contract_path.write_text(contract,encoding='utf-8')

if browser_path.exists():
    b=browser_path.read_text(encoding='utf-8')
    insert=r'''

async function desktopInteractionUx(){
  const ctx=await browser.newContext({viewport:{width:1366,height:768}});
  await ctx.addInitScript(()=>localStorage.setItem('trace-v010-state',JSON.stringify({project:{id:'p',title:'Desktop interaction study',methodology:'RTA',codingMode:'manual',researchQuestions:[],researchQuestionRecords:[]},activeSection:'Data',dataContext:'sources',activeSourceId:'s1',openSourceTabs:['s1'],participants:[],transcript:[],importedSources:[{id:'s1',name:'Interview 01.txt',kind:'text',lines:1,segments:[{id:'seg1',text:'Access was difficult'}],codings:[]}],codes:[{id:'c1',name:'Access',description:'',color:'#4466aa'}],coders:[],codingRefs:[],allCodingRefs:[],memos:[],annotations:[],themes:[],findingsSections:[],findingsEvidence:[],sourceProperties:[],sourceCollections:[],importQueue:[],backups:[],audit:[],mediaSelections:[],mediaCodings:[],mediaPayloads:{},savedAt:Date.now()})));
  const page=await ctx.newPage();await page.goto(base,{waitUntil:'networkidle'});
  await page.click('#rail-settings');
  if(!await page.locator('#remember-layout').count())errors.push('Application Settings does not expose Remember my layout');
  if(!await page.locator('#resume-exact-workspace').count())errors.push('Application Settings does not separate exact-workspace resume');
  await page.click('#settings-close');
  await page.locator('[data-source="s1"]').click({button:'right'});
  const menu=page.locator('#trace-context-menu');
  if(!await menu.count())errors.push('source right-click did not open the standard context menu');
  if(!await menu.getByText('Manage source…',{exact:true}).count())errors.push('source context menu is missing Manage source');
  await page.keyboard.press('Escape');
  if(await menu.count())errors.push('Escape did not dismiss the context menu');
  await ctx.close();
}
'''
    needle="await fresh();await emptyProject();await populated();await contextualData();await keyboardProductivity();await contextualShell();await researcherJourney();await trustSafetyUx();await browser.close();"
    replacement=insert+'\n'+needle.replace('await browser.close();','await desktopInteractionUx();await browser.close();')
    if 'async function desktopInteractionUx()' not in b:
        if needle not in b: raise SystemExit('Browser-contract final invocation anchor changed')
        b=b.replace(needle,replacement,1)
        browser_path.write_text(b,encoding='utf-8')
print('Desktop interaction, layout memory and exact-workspace resume patch applied')
