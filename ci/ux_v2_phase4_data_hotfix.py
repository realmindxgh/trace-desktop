from pathlib import Path

app_path=Path('src/app.js')
css_path=Path('src/styles.css')
test_path=Path('tests/ux_foundation_v2_contract.py')
app=app_path.read_text(encoding='utf-8')

old_data_context="""  if(state.activeSection==='Data')return `<aside class=\"context-pane\"><div class=\"context-title\"><span>DATA</span><small>${state.importedSources.length} sources</small></div><button class=\"context-link active\">${icon('folder',16)}<span>Sources</span><b>${state.importedSources.length}</b></button><button class=\"context-link\">${icon('info',16)}<span>Participants</span><b>${state.participants.length}</b></button><button class=\"context-link\">${icon('folder',16)}<span>Collections</span><b>${state.sourceCollections.length}</b></button><button class=\"context-link\">${icon('upload',16)}<span>Imports</span><b>${state.importQueue.length}</b></button><div class=\"context-help\"><b>Bring data in</b><p>Organise research material before interpretation.</p></div></aside>`;"""
new_data_context="""  if(state.activeSection==='Data'){
    const view=state.dataContext||'sources';
    const items=[['sources','folder','Sources',state.importedSources.length],['participants','info','Participants',state.participants.length],['collections','folder','Collections',state.sourceCollections.length],['imports','upload','Imports',state.importQueue.length]];
    return `<aside class=\"context-pane data-context-pane\"><div class=\"context-title\"><span>DATA</span><small>${state.importedSources.length} sources</small></div>${items.map(([id,ic,label,count])=>`<button class=\"context-link ${view===id?'active':''}\" data-data-context=\"${id}\" aria-current=\"${view===id?'page':'false'}\">${icon(ic,16)}<span>${label}</span><b>${count}</b></button>`).join('')}<div class=\"context-help\"><b>${view==='participants'?'Cases and attributes':view==='collections'?'Organise source sets':view==='imports'?'Bring data in':'Research material'}</b><p>${view==='participants'?'Review real participant records and their project attributes.':view==='collections'?'Group sources without moving or duplicating originals.':view==='imports'?'Import files and review per-file outcomes.':'Find, filter and open the material in this project.'}</p></div></aside>`;
  }"""
if old_data_context in app:
    app=app.replace(old_data_context,new_data_context,1)
elif 'data-data-context' not in app:
    raise SystemExit('Could not locate Data context-pane implementation')

old_hydrate="mediaPayloads:state.mediaPayloads||{},sourceFilter:state.sourceFilter||'all',activeCollectionId:state.activeCollectionId||null,dataSearch:state.dataSearch||''"
new_hydrate="mediaPayloads:state.mediaPayloads||{},sourceFilter:state.sourceFilter||'all',activeCollectionId:state.activeCollectionId||null,dataContext:state.dataContext||'sources',dataSearch:state.dataSearch||''"
if old_hydrate in app:
    app=app.replace(old_hydrate,new_hydrate,1)
elif new_hydrate not in app:
    raise SystemExit('Could not locate native hydration Data state')

if 'function renderDataSourcesWorkspace(){' not in app:
    if 'function renderDataWorkspace(){' not in app:
        raise SystemExit('Could not locate Data workspace function')
    app=app.replace('function renderDataWorkspace(){','function renderDataSourcesWorkspace(){',1)

insert_anchor='\nfunction formatBytes(n)'
if 'function renderDataParticipantsWorkspace(){' not in app:
    if insert_anchor not in app:
        raise SystemExit('Could not locate Data workspace insertion anchor')
    extra=r'''

function renderDataParticipantsWorkspace(){
  const vars=state.variables||[];
  return `<div class="page-layout data-subworkspace"><section class="page-head compact"><span class="eyebrow">DATA · PARTICIPANTS</span><h1>People and cases in this project.</h1><p>Participant records only appear when the project actually contains them. Attributes stay attached to the participant rather than being invented from source names.</p><div class="head-actions"><button class="secondary" id="add-attribute">+ Participant attribute</button><button class="primary" id="participants-import">Import survey data</button></div></section>${state.participants.length?`<div class="participant-table-wrap"><table class="participant-table"><thead><tr><th>Participant</th><th>Linked sources</th>${vars.slice(0,4).map(v=>`<th>${escapeHtml(v.name)}</th>`).join('')}<th></th></tr></thead><tbody>${state.participants.map(p=>{const owner=p.internalId||p.id;const linked=state.importedSources.filter(s=>s.participantId===owner).length;return `<tr><th>${escapeHtml(p.id||'Participant')}</th><td>${linked}</td>${vars.slice(0,4).map(v=>`<td>${escapeHtml(participantVariableValue(p,v.id))}</td>`).join('')}<td><button class="text-btn" data-open-participant="${escapeHtml(p.id||'')}">View profile</button></td></tr>`}).join('')}</tbody></table></div>`:`<article class="empty-wide data-truth-empty"><span>${icon('info',24)}</span><h3>No participants yet</h3><p>Trace will not create placeholder participants. Import survey/case data or link a source to a real participant when your study requires cases.</p><button class="primary" id="participants-import-empty">Import participant data</button></article>`}</div>`;
}

function renderDataCollectionsWorkspace(){
  return `<div class="page-layout data-subworkspace"><section class="page-head compact"><span class="eyebrow">DATA · COLLECTIONS</span><h1>Organise sources without moving them.</h1><p>Collections are project-level sets for comparison and navigation. A source can belong to more than one collection while the original remains untouched.</p><div class="head-actions"><button class="primary" id="new-collection">+ New collection</button></div></section>${state.sourceCollections.length?`<div class="collection-workspace-grid">${state.sourceCollections.map(c=>`<article><div><span>${icon('folder',20)}</span><h3>${escapeHtml(c.name)}</h3><p>${c.sourceIds?.length||0} source${(c.sourceIds?.length||0)===1?'':'s'}</p></div><div><button class="secondary tiny" data-open-collection="${c.id}">View sources</button><button class="text-btn" data-manage-collection="${c.id}">Manage</button></div></article>`).join('')}</div>`:`<article class="empty-wide data-truth-empty"><span>${icon('folder',24)}</span><h3>No collections yet</h3><p>Create a set when you need to compare or revisit a meaningful group of sources. Collections never duplicate your research files.</p><button class="primary" id="new-collection-empty">Create collection</button></article>`}</div>`;
}

function renderDataImportsWorkspace(){
  return `<div class="page-layout data-subworkspace"><section class="page-head compact"><span class="eyebrow">DATA · IMPORTS</span><h1>Bring research material into Trace.</h1><p>Each file reports its own outcome. Audio and video remain local and can be transcribed in the desktop app.</p><div class="head-actions"><button class="primary" id="data-import">Choose files</button></div></section><div class="import-drop-zone import-workspace-drop" id="import-drop-zone" tabindex="0" role="button" aria-label="Drop research files here or press Enter to choose files">${icon('upload',22)}<div><b>Drop documents, surveys, PDFs or media here</b><small>TXT, MD, DOCX, CSV, XLSX, PDF, images, audio and video. Multiple files are supported.</small></div><button class="secondary" id="drop-browse">Browse files</button></div>${renderImportQueue()}<section class="import-type-grid"><article><b>Documents & PDFs</b><p>Transcripts, DOCX, text and PDF research material.</p></article><article><b>Survey data</b><p>CSV/XLSX tables can create participants and attributes when those records are truly present.</p></article><article><b>Audio & video</b><p>Add media and transcribe locally when required.</p></article><article><b>Qualitative projects</b><p>Use the advanced interoperability controls in Sources for .trace and REFI-QDA exchange.</p></article></section></div>`;
}

function renderDataWorkspace(){
  const view=state.dataContext||'sources';
  if(view==='participants')return renderDataParticipantsWorkspace();
  if(view==='collections')return renderDataCollectionsWorkspace();
  if(view==='imports')return renderDataImportsWorkspace();
  return renderDataSourcesWorkspace();
}
'''
    app=app.replace(insert_anchor,extra+insert_anchor,1)

event_anchor="  document.querySelectorAll('[data-section]').forEach(btn=>btn.addEventListener('click',()=>{homeMode=false;state.activeSection=btn.dataset.section;saveState('Opened '+state.activeSection);heartbeatNativeSession();render();}));\n"
event_insert=event_anchor+"  document.querySelectorAll('[data-data-context]').forEach(btn=>btn.addEventListener('click',()=>{state.dataContext=btn.dataset.dataContext||'sources';saveState('Opened Data '+state.dataContext);render();}));\n  document.querySelectorAll('[data-open-collection]').forEach(btn=>btn.addEventListener('click',()=>{state.dataContext='sources';state.activeCollectionId=btn.dataset.openCollection||null;saveState('Opened collection');render();}));\n  document.querySelectorAll('[data-open-participant]').forEach(btn=>btn.addEventListener('click',()=>{state.activeParticipant=btn.dataset.openParticipant||null;openParticipantProfile();}));\n  document.querySelector('#participants-import')?.addEventListener('click',openImporter);document.querySelector('#participants-import-empty')?.addEventListener('click',openImporter);document.querySelector('#new-collection-empty')?.addEventListener('click',createCollection);\n"
if event_anchor in app and "document.querySelectorAll('[data-data-context]')" not in app:
    app=app.replace(event_anchor,event_insert,1)
elif "document.querySelectorAll('[data-data-context]')" not in app:
    raise SystemExit('Could not locate global Data navigation binding anchor')

app_path.write_text(app,encoding='utf-8')

css=css_path.read_text(encoding='utf-8')
marker='/* UX_V2_PHASE4_DATA_CONTEXT */'
if marker not in css:
    css += r'''

/* UX_V2_PHASE4_DATA_CONTEXT */
.data-subworkspace{max-width:none}.data-context-pane .context-link[aria-current="page"]{background:color-mix(in srgb,var(--blue) 10%,var(--panel));color:var(--blue)}
.participant-table-wrap{border:1px solid var(--line);border-radius:14px;overflow:auto;background:var(--panel)}.participant-table{width:100%;border-collapse:collapse;min-width:720px}.participant-table th,.participant-table td{padding:13px 15px;border-bottom:1px solid var(--line);text-align:left;font-size:var(--trace-font-ui,15px)}.participant-table thead th{font-size:var(--trace-font-small,13px);color:var(--muted);background:var(--panel2);position:sticky;top:0}.participant-table tbody th{color:var(--ink)}.participant-table tbody tr:last-child>*{border-bottom:0}
.collection-workspace-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}.collection-workspace-grid article{border:1px solid var(--line);background:var(--panel);padding:18px;border-radius:14px;display:flex;justify-content:space-between;gap:18px;align-items:flex-start}.collection-workspace-grid h3{margin:8px 0 4px;color:var(--ink)}.collection-workspace-grid p{margin:0;color:var(--muted)}.collection-workspace-grid article>div:last-child{display:flex;gap:6px;align-items:center}
.import-workspace-drop{min-height:150px;margin-top:4px}.import-type-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin-top:18px}.import-type-grid article{border-top:1px solid var(--line);padding:15px 2px}.import-type-grid b{color:var(--ink)}.import-type-grid p{color:var(--muted);line-height:1.5}.data-truth-empty{margin-top:8px}
@media(max-width:900px){.import-type-grid{grid-template-columns:1fr}.collection-workspace-grid{grid-template-columns:1fr}}
'''
    css_path.write_text(css,encoding='utf-8')

test=test_path.read_text(encoding='utf-8')
for assertion in [
    "assert 'data-data-context' in app\n",
    "assert 'renderDataParticipantsWorkspace' in app\n",
    "assert 'renderDataCollectionsWorkspace' in app\n",
    "assert 'renderDataImportsWorkspace' in app\n",
    "assert 'UX_V2_PHASE4_DATA_CONTEXT' in css\n",
]:
    if assertion not in test:
        test += '\n'+assertion
test_path.write_text(test,encoding='utf-8')

check=app_path.read_text(encoding='utf-8')
for required in ('data-data-context','renderDataParticipantsWorkspace','renderDataCollectionsWorkspace','renderDataImportsWorkspace',"dataContext=btn.dataset.dataContext"):
    if required not in check:
        raise SystemExit(f'Phase 4 Data contract missing: {required}')
print('Phase 4 Data contextual workspace hotfix applied')
