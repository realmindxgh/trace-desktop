from pathlib import Path

app_path=Path('src/app.js')
css_path=Path('src/styles.css')
test_path=Path('tests/ux_foundation_v2_contract.py')
app=app_path.read_text(encoding='utf-8')

if "  codeSearch: ''," not in app:
    anchor="  dataSearch: '',\n"
    if anchor not in app:
        raise SystemExit('Could not locate search-state anchor')
    app=app.replace(anchor,anchor+"  codeSearch: '',\n",1)

if 'function renderCodeContextRail(){' not in app:
    anchor='\nfunction renderCodeWorkspace(){'
    if anchor not in app:
        raise SystemExit('Could not locate Code workspace anchor')
    fn=r'''

function renderCodeContextRail(){
  const q=(state.codeSearch||'').trim().toLowerCase();
  const codes=state.codes.filter(c=>!q||`${c.name} ${c.description||''}`.toLowerCase().includes(q));
  const refs=state.allCodingRefs||state.codingRefs;
  const recent=(state.openSourceTabs||[]).map(id=>state.importedSources.find(s=>s.id===id)).filter(Boolean).slice(-5).reverse();
  return `<aside class="data-rail context-pane code-system-pane"><div class="rail-title"><span>CODE SYSTEM</span><button class="rail-collapse" id="toggle-left-rail" title="Collapse code system" aria-label="Collapse code system">‹</button></div><label class="rail-search">${icon('search',16)}<input id="code-context-search" value="${escapeHtml(state.codeSearch||'')}" placeholder="Search codes"></label><div class="code-context-list">${codes.length?codes.map(c=>`<button class="code-context-row" data-code-context="${c.id}" style="--depth:${c.parentId?1:0}"><i style="--chip:${c.color}"></i><span>${escapeHtml(c.name)}</span><small>${refs.filter(r=>r.codeId===c.id).length}</small></button>`).join(''):`<div class="rail-empty">${state.codes.length?'No codes match this search.':'No codes yet.'}<small>${state.codes.length?'Change the search to find another code.':'Create your first code or select a passage and code it.'}</small></div>`}</div><button class="import-source code-create-action" id="code-context-new">${icon('plus',15)} New code</button><div class="code-source-launcher"><b>OPEN SOURCES</b>${recent.length?recent.map(s=>`<button data-open-code-source="${s.id}" class="${s.id===state.activeSourceId?'active':''}"><span>${escapeHtml(s.name)}</span><small>${sourceKindLabel(s.kind)}</small></button>`).join(''):`<p>Open research material from Data. Source tabs will remain available here while you code.</p>`}<button class="text-btn" id="code-context-data">Browse all sources →</button></div></aside>`;
}
'''
    app=app.replace(anchor,fn+anchor,1)

app=app.replace('${renderDataRail()}<div class="pane-resizer left-resizer"','${renderCodeContextRail()}<div class="pane-resizer left-resizer"',1)
app=app.replace('<div class="tri-layout media-layout">${renderDataRail()}','<div class="tri-layout media-layout">${renderCodeContextRail()}',1)
app=app.replace("'Pick a source from the context pane.'","'Open a source from Data, the command palette, or a recent source tab.'")

# Analyse navigation belongs in the contextual pane. Keep one navigation system
# instead of duplicating the same five query tabs in the main canvas.
old_analyse_context="""  if(state.activeSection==='Analyse')return `<aside class=\"context-pane\"><div class=\"context-title\"><span>ANALYSE</span><small>Queries</small></div>${[['matrix','Matrix'],['cooccurrence','Co-occurrence'],['negative','Negative cases'],['groups','Groups'],['intercoder','Intercoder']].map(([id,label])=>`<button class=\"context-link ${state.analysisTab===id?'active':''}\" data-analysis-tab=\"${id}\"><span>${label}</span></button>`).join('')}<div class=\"context-help\"><b>Ask a focused question</b><p>Every result remains tied to coded evidence.</p></div></aside>`;"""
new_analyse_context="""  if(state.activeSection==='Analyse')return `<aside class=\"context-pane analyse-context-pane\"><div class=\"context-title\"><span>ANALYSE</span><small>Queries</small></div><div class=\"analysis-tabs context-analysis-tabs\">${[['matrix','Matrix'],['cooccurrence','Co-occurrence'],['negative','Negative cases'],['groups','Groups'],['intercoder','Intercoder']].map(([id,label])=>`<button class=\"context-link ${state.analysisTab===id?'active':''}\" data-analysis-tab=\"${id}\" aria-current=\"${state.analysisTab===id?'page':'false'}\"><span>${label}</span></button>`).join('')}</div><div class=\"context-help\"><b>Ask a focused question</b><p>Every result remains tied to coded evidence.</p></div></aside>`;"""
if old_analyse_context in app:
    app=app.replace(old_analyse_context,new_analyse_context,1)
elif 'context-analysis-tabs' not in app:
    raise SystemExit('Could not locate Analyse contextual navigation')

main_analysis_tabs="""<nav class=\"analysis-tabs\">${[['matrix','Matrix'],['cooccurrence','Co-occurrence'],['negative','Negative cases'],['groups','Groups'],['intercoder','Intercoder']].map(([id,label])=>`<button data-analysis-tab=\"${id}\" class=\"${tab===id?'active':''}\">${label}</button>`).join('')}</nav>"""
if main_analysis_tabs in app:
    app=app.replace(main_analysis_tabs,'',1)

event_anchor="  document.querySelector('#toggle-left-rail')?.addEventListener('click',()=>{state.leftRailCollapsed=!state.leftRailCollapsed;saveState('Toggled source panel');render();});\n"
if "document.querySelector('#code-context-search')" not in app:
    insertion=event_anchor+"  document.querySelector('#code-context-search')?.addEventListener('input',e=>{state.codeSearch=e.target.value;try{localStorage.setItem(STORAGE_KEY,JSON.stringify(persistableState()));}catch{}render();queueMicrotask(()=>{const el=document.querySelector('#code-context-search');if(el){el.focus();el.setSelectionRange(el.value.length,el.value.length)}})});document.querySelectorAll('[data-code-context]').forEach(btn=>btn.addEventListener('click',()=>openCodeEditor(btn.dataset.codeContext)));document.querySelector('#code-context-new')?.addEventListener('click',()=>openCodeEditor());document.querySelectorAll('[data-open-code-source]').forEach(btn=>btn.addEventListener('click',()=>activateSource(btn.dataset.openCodeSource)));document.querySelector('#code-context-data')?.addEventListener('click',()=>{state.activeSection='Data';state.dataContext='sources';saveState('Opened Data sources');render();});\n"
    if event_anchor not in app:
        raise SystemExit('Could not locate Code context event anchor')
    app=app.replace(event_anchor,insertion,1)

old="dataContext:state.dataContext||'sources',dataSearch:state.dataSearch||'',themeSearch:state.themeSearch||''"
new="dataContext:state.dataContext||'sources',dataSearch:state.dataSearch||'',codeSearch:state.codeSearch||'',themeSearch:state.themeSearch||''"
if old in app:
    app=app.replace(old,new,1)
elif new not in app:
    raise SystemExit('Could not locate native search-state hydration')

app_path.write_text(app,encoding='utf-8')

css=css_path.read_text(encoding='utf-8')
marker='/* UX_V2_PHASE5_CODE_CONTEXT */'
if marker not in css:
    css += r'''

/* UX_V2_PHASE5_CODE_CONTEXT */
.code-system-pane{display:flex;flex-direction:column;min-height:0}.code-context-list{display:flex;flex-direction:column;gap:2px;overflow:auto;min-height:90px;flex:1;padding:2px 0 8px}.code-context-row{border:0;background:transparent;color:var(--text);min-height:36px;border-radius:8px;padding:7px 8px 7px calc(8px + var(--depth,0)*14px);display:grid;grid-template-columns:8px minmax(0,1fr) auto;gap:8px;align-items:center;text-align:left}.code-context-row:hover{background:var(--panel2)}.code-context-row i{width:8px;height:8px;border-radius:3px;background:var(--chip)}.code-context-row span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:var(--trace-font-ui,15px)}.code-context-row small{color:var(--muted);font-size:var(--trace-font-small,13px)}.code-create-action{flex:0 0 auto}.code-source-launcher{border-top:1px solid var(--line);padding:13px 5px 4px;display:flex;flex-direction:column;gap:4px}.code-source-launcher>b{font-size:12.5px;letter-spacing:.08em;color:var(--muted);padding:0 5px 4px}.code-source-launcher>button:not(.text-btn){border:0;background:transparent;color:var(--text);padding:7px 6px;border-radius:7px;text-align:left;display:flex;flex-direction:column}.code-source-launcher>button:not(.text-btn):hover,.code-source-launcher>button.active{background:var(--panel2)}.code-source-launcher span{font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}.code-source-launcher small,.code-source-launcher p{font-size:12px;color:var(--muted);margin:0;line-height:1.4}.code-source-launcher .text-btn{text-align:left;padding:7px 5px}
/* UX_V2_PHASE5_ANALYSE_CONTEXT */
.context-analysis-tabs{display:flex!important;flex-direction:column!important;width:100%!important;gap:3px!important;overflow:visible!important}.context-analysis-tabs button{width:100%!important;min-width:0!important;white-space:normal!important;overflow:visible!important;text-align:left!important}
'''
    css_path.write_text(css,encoding='utf-8')
elif 'UX_V2_PHASE5_ANALYSE_CONTEXT' not in css:
    css += r'''

/* UX_V2_PHASE5_ANALYSE_CONTEXT */
.context-analysis-tabs{display:flex!important;flex-direction:column!important;width:100%!important;gap:3px!important;overflow:visible!important}.context-analysis-tabs button{width:100%!important;min-width:0!important;white-space:normal!important;overflow:visible!important;text-align:left!important}
'''
    css_path.write_text(css,encoding='utf-8')

test=test_path.read_text(encoding='utf-8')
for assertion in [
    "assert 'renderCodeContextRail' in app\n",
    "assert 'data-code-context' in app\n",
    "assert 'context-analysis-tabs' in app\n",
    "assert 'UX_V2_PHASE5_CODE_CONTEXT' in css\n",
    "assert 'UX_V2_PHASE5_ANALYSE_CONTEXT' in css\n",
]:
    if assertion not in test:
        test+='\n'+assertion
test_path.write_text(test,encoding='utf-8')

check=app_path.read_text(encoding='utf-8')
for req in ('renderCodeContextRail','data-code-context','code-context-search','Browse all sources','context-analysis-tabs'):
    if req not in check:
        raise SystemExit(f'Phase 5 contextual architecture contract missing: {req}')
print('Phase 5 Code-system and Analyse contextual navigation hotfix applied')
