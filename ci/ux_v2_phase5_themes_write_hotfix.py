from pathlib import Path

app_path=Path('src/app.js')
css_path=Path('src/styles.css')
test_path=Path('tests/ux_foundation_v2_contract.py')
app=app_path.read_text(encoding='utf-8')

old_themes="""  if(state.activeSection==='Themes')return `<aside class=\"context-pane\"><div class=\"context-title\"><span>THEMES</span><small>${state.themes.length} candidates</small></div>${state.themes.slice(0,30).map(t=>`<button class=\"context-link\" data-edit-theme=\"${t.id}\"><span>${escapeHtml(t.name)}</span><b>${t.codeIds?.length||0}</b></button>`).join('')||'<div class=\"context-empty\">Themes will appear here as you build them from codes.</div>'}</aside>`;"""
new_themes="""  if(state.activeSection==='Themes')return `<aside class=\"context-pane themes-context-pane\"><div class=\"context-title\"><span>THEMES</span><small>${state.themes.length} candidates</small></div><label class=\"rail-search theme-context-search\">${icon('search',16)}<input id=\"theme-search\" value=\"${escapeHtml(state.themeSearch||'')}\" placeholder=\"Search themes and codes\"></label><button class=\"context-primary\" id=\"new-theme\">${icon('plus',15)} New theme</button><div class=\"themes-context-list\">${state.themes.slice(0,60).map(t=>`<button class=\"context-link\" data-edit-theme=\"${t.id}\"><span>${escapeHtml(t.name)}</span><b>${t.codeIds?.length||0}</b></button>`).join('')||'<div class=\"context-empty\">No themes yet. Develop one when related codes begin to form an interpretive pattern.</div>'}</div><button class=\"context-link context-secondary\" id=\"manage-codes\">${icon('tag',15)}<span>Manage code system</span><b>${state.codes.length}</b></button><div class=\"context-help\"><b>Interpret, do not decorate</b><p>Themes stay tied to researcher-selected codes and inspectable evidence.</p></div></aside>`;"""
if old_themes in app:
    app=app.replace(old_themes,new_themes,1)
elif 'themes-context-pane' not in app:
    raise SystemExit('Theme context anchor missing')

old_write="""  if(state.activeSection==='Write')return `<aside class=\"context-pane\"><div class=\"context-title\"><span>WRITE</span><small>Findings</small></div>${state.findingsSections.slice(0,30).map(x=>`<div class=\"context-note\"><b>${escapeHtml(x.title||'Findings')}</b><small>${relativeTime(x.updatedAt)}</small></div>`).join('')||'<div class=\"context-empty\">Create a findings section when you are ready to write from evidence.</div>'}</aside>`;"""
new_write="""  if(state.activeSection==='Write'){
    const targets=[...state.project.researchQuestionRecords.map((r,i)=>({type:'research_question',id:r.id,title:`Research Question ${i+1}`,subtitle:r.text})),...state.themes.map(t=>({type:'theme',id:t.id,title:t.name,subtitle:'Candidate theme'}))];
    const active=targets.find(t=>state.writeTarget&&t.type===state.writeTarget.type&&t.id===state.writeTarget.id)||targets[0];
    return `<aside class=\"context-pane write-context-pane\"><div class=\"context-title\"><span>WRITE</span><small>${state.findingsSections.length} saved</small></div><div class=\"write-context-list\">${targets.length?targets.map(t=>{const section=state.findingsSections.find(x=>x.targetType===t.type&&(x.targetId||null)===(t.id||null));return `<button class=\"context-link write-context-row ${active&&active.type===t.type&&active.id===t.id?'active':''}\" data-write-target=\"${t.type}:${t.id||''}\" aria-current=\"${active&&active.type===t.type&&active.id===t.id?'page':'false'}\"><span>${escapeHtml(t.title)}</span><small>${section?relativeTime(section.updatedAt):'Not started'}</small></button>`}).join(''):'<div class=\"context-empty\">Add a research question or candidate theme to create a findings outline.</div>'}</div><button class=\"context-link context-secondary\" id=\"export-findings\">${icon('download',15)}<span>Export findings</span></button><div class=\"context-help\"><b>Write from evidence</b><p>Keep the draft beside linked coded passages so interpretations remain traceable.</p></div></aside>`;
  }"""
if old_write in app:
    app=app.replace(old_write,new_write,1)
elif 'write-context-pane' not in app:
    raise SystemExit('Write context anchor missing')

old_head="""<div class=\"head-actions\"><label class=\"workspace-search theme-search\">${icon('search',15)}<input id=\"theme-search\" value=\"${escapeHtml(state.themeSearch||'')}\" placeholder=\"Search themes and codes\"></label><button class=\"primary\" id=\"new-theme\">${icon('plus',16)} New theme</button><button class=\"secondary\" id=\"manage-codes\">Manage codes</button>${state.project.codingMode==='ai'?`<button class=\"secondary\" id=\"explore-themes\">${icon('spark',16)} Explore with AI</button>`:''}</div>"""
if old_head in app:
    app=app.replace(old_head,'',1)

old_outline="""<aside class=\"findings-outline\"><b>Findings outline</b>${targets.length?targets.map(t=>`<button data-write-target=\"${t.type}:${t.id||''}\" class=\"${t.type===target.type&&t.id===target.id?'active':''}\"><span>${escapeHtml(t.title)}</span><small>${escapeHtml(t.subtitle||'')}</small></button>`).join(''):'<p>Add a research question or candidate theme to build the outline.</p>'}</aside>"""
if old_outline in app:
    app=app.replace(old_outline,'',1)

app_path.write_text(app,encoding='utf-8')

css=css_path.read_text(encoding='utf-8')
if '/* UX_V2_PHASE5_THEMES_WRITE_CONTEXT */' not in css:
    css += r'''

/* UX_V2_PHASE5_THEMES_WRITE_CONTEXT */
.themes-context-pane,.write-context-pane{display:flex;flex-direction:column;min-height:0}.themes-context-list,.write-context-list{display:flex;flex-direction:column;gap:3px;min-height:0;overflow:auto;margin:5px 0;flex:1}.context-primary{margin:4px 0 7px;border:0;border-radius:9px;min-height:38px;background:var(--accent,var(--blue));color:#fff;font:inherit;font-weight:700;display:flex;align-items:center;justify-content:center;gap:7px;cursor:pointer}.context-secondary{margin-top:5px}.write-context-row{display:grid!important;grid-template-columns:minmax(0,1fr)!important;gap:3px!important;align-items:start!important}.write-context-row span{font-size:var(--trace-font-ui,15px);white-space:normal}.write-context-row small{font-size:12px;color:var(--muted)}.write-workspace{grid-template-columns:minmax(420px,1fr) minmax(300px,.72fr)!important}.write-evidence{grid-column:auto!important}.themes-page .page-head .head-actions:empty{display:none}
@media(max-width:1050px){.write-workspace{grid-template-columns:1fr!important}.write-evidence{grid-column:1!important;min-height:auto}}
'''
    css_path.write_text(css,encoding='utf-8')

test=test_path.read_text(encoding='utf-8')
for assertion in [
    "assert 'themes-context-pane' in app\n",
    "assert 'write-context-pane' in app\n",
    "assert 'UX_V2_PHASE5_THEMES_WRITE_CONTEXT' in css\n",
]:
    if assertion not in test:
        test+='\n'+assertion
test_path.write_text(test,encoding='utf-8')

check=app_path.read_text(encoding='utf-8')
for required in ('themes-context-pane','theme-context-search','write-context-pane','write-context-list'):
    if required not in check:
        raise SystemExit(f'Themes/Write contextual architecture missing: {required}')
print('Phase 5 Themes and Write contextual navigation hotfix applied')
