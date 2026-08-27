from pathlib import Path

app_path=Path('src/app.js')
css_path=Path('src/styles.css')
test_path=Path('tests/ux_foundation_v2_contract.py')
app=app_path.read_text(encoding='utf-8')

if 'function renderModeInspector(){' not in app:
    anchor='\nfunction renderProjectSection(){'
    if anchor not in app:
        raise SystemExit('Could not locate mode-shell inspector anchor')
    fn=r'''

function renderModeInspector(){
  const close=`<button class="inspector-collapse" id="toggle-inspector" title="Collapse inspector" aria-label="Collapse inspector">›</button>`;
  const top=label=>`<div class="inspector-top mode-inspector-top"><div><small>INSPECTOR</small><b>${label}</b></div>${close}</div>`;
  if(state.activeSection==='Data'){
    const src=currentSource(),p=state.participants.find(x=>(x.internalId||x.id)===state.activeParticipant||x.id===state.activeParticipant);
    if((state.dataContext||'sources')==='participants')return `<aside class="inspector mode-inspector">${top('Participant context')}<section class="inspect-block">${p?`<h4>${escapeHtml(p.id||'Participant')}</h4><p>${escapeHtml(p.role||'Participant record')}</p><dl><dt>Linked sources</dt><dd>${state.importedSources.filter(s=>s.participantId===(p.internalId||p.id)).length}</dd><dt>Attributes</dt><dd>${state.variables?.length||0}</dd></dl>`:'<h4>No participant selected</h4><p>Select a real participant record to inspect its linked sources and attributes. Trace does not invent a placeholder case.</p>'}</section></aside>`;
    return `<aside class="inspector mode-inspector">${top('Data context')}<section class="inspect-block"><h4>${src?escapeHtml(src.name):'Project data'}</h4>${src?`<dl><dt>Type</dt><dd>${escapeHtml(sourceKindLabel(src.kind))}</dd><dt>Participant</dt><dd>${escapeHtml(state.participants.find(p=>(p.internalId||p.id)===src.participantId)?.id||'Unassigned')}</dd></dl>`:`<p>Select or open research material when you need source-specific details.</p><dl><dt>Sources</dt><dd>${state.importedSources.length}</dd><dt>Participants</dt><dd>${state.participants.length}</dd><dt>Collections</dt><dd>${state.sourceCollections.length}</dd></dl>`}</section></aside>`;
  }
  if(state.activeSection==='Themes')return `<aside class="inspector mode-inspector">${top('Theme context')}<section class="inspect-block"><h4>Interpretive structure</h4><dl><dt>Candidate themes</dt><dd>${state.themes.length}</dd><dt>Codes available</dt><dd>${state.codes.length}</dd><dt>Coded passages</dt><dd>${(state.allCodingRefs||state.codingRefs).length}</dd></dl><p>Inspect supporting evidence before treating a theme as a stable interpretation.</p></section></aside>`;
  if(state.activeSection==='Analyse'){
    const labels={matrix:'Participant × code',cooccurrence:'Code co-occurrence',negative:'Negative cases',groups:'Group comparison',intercoder:'Intercoder comparison'};
    return `<aside class="inspector mode-inspector">${top('Analysis context')}<section class="inspect-block"><h4>${escapeHtml(labels[state.analysisTab]||'Analysis')}</h4><p>Results are derived from saved coding references and remain drillable to evidence.</p><dl><dt>Coded passages</dt><dd>${(state.allCodingRefs||state.codingRefs).length}</dd><dt>Codes</dt><dd>${state.codes.length}</dd><dt>Participants</dt><dd>${state.participants.length}</dd></dl></section></aside>`;
  }
  if(state.activeSection==='Write'){
    const targets=[...state.project.researchQuestionRecords.map((r,i)=>({type:'research_question',id:r.id,title:`Research Question ${i+1}`})),...state.themes.map(t=>({type:'theme',id:t.id,title:t.name}))];
    const target=targets.find(t=>state.writeTarget&&t.type===state.writeTarget.type&&t.id===state.writeTarget.id)||targets[0];
    const section=target&&state.findingsSections.find(x=>x.targetType===target.type&&(x.targetId||null)===(target.id||null));
    const links=section?state.findingsEvidence.filter(x=>x.findingsId===section.id):[];
    return `<aside class="inspector mode-inspector">${top('Writing context')}<section class="inspect-block"><h4>${escapeHtml(target?.title||'Findings')}</h4><p>${section?`Last saved ${relativeTime(section.updatedAt)}.`:'This section has not been saved yet.'}</p><dl><dt>Linked evidence</dt><dd>${links.length}</dd><dt>Saved sections</dt><dd>${state.findingsSections.length}</dd></dl></section></aside>`;
  }
  return '';
}
'''
    app=app.replace(anchor,fn+anchor,1)

old='  return `<div class="mode-shell">${renderModeContext()}<section class="mode-main">${content}</section></div>`;'
new='  return `<div class="mode-shell ${state.inspectorCollapsed?\'right-collapsed\':\'\'}" style="--right-inspector:${Math.max(300,Math.min(520,Number(state.inspectorWidth)||340))}px">${renderModeContext()}<section class="mode-main">${content}</section><div class="pane-resizer right-resizer" id="right-resizer" role="separator" tabindex="0" aria-orientation="vertical" aria-label="Resize inspector" aria-valuemin="300" aria-valuemax="520"></div>${renderModeInspector()}</div>`;'
if old in app:
    app=app.replace(old,new,1)
elif 'renderModeInspector()' not in app:
    raise SystemExit('Could not upgrade mode shell with shared inspector')

old_bind="const root=document.querySelector('.tri-layout');if(!root)return;"
new_bind="const root=document.querySelector('.tri-layout,.mode-shell');if(!root)return;"
if old_bind in app:
    app=app.replace(old_bind,new_bind,1)
elif new_bind not in app:
    raise SystemExit('Could not extend pane resizer to mode shell')

app_path.write_text(app,encoding='utf-8')

css=css_path.read_text(encoding='utf-8')
if '/* UX_V2_SHARED_MODE_INSPECTOR */' not in css:
    css += r'''

/* UX_V2_SHARED_MODE_INSPECTOR */
.mode-shell{grid-template-columns:var(--trace-context) minmax(0,1fr) 7px minmax(300px,var(--right-inspector,340px))!important}.mode-shell>.right-resizer{display:block}.mode-inspector{border-left:1px solid var(--line);border-right:0;min-width:0;background:var(--panel2);overflow:auto}.mode-inspector-top{display:flex;align-items:center;justify-content:space-between;padding:13px 12px;border-bottom:1px solid var(--line)}.mode-inspector-top>div{display:flex;flex-direction:column;gap:2px}.mode-inspector-top small{font-size:12.5px;letter-spacing:.08em;color:var(--muted)}.mode-inspector-top b{font-size:14px;color:var(--ink)}.mode-shell.right-collapsed{grid-template-columns:var(--trace-context) minmax(0,1fr) 0 0!important}.mode-shell.right-collapsed>.mode-inspector,.mode-shell.right-collapsed>.right-resizer{display:none!important}
@media(max-width:1180px){.mode-shell{grid-template-columns:var(--trace-context) minmax(0,1fr)!important}.mode-shell>.mode-inspector,.mode-shell>.right-resizer{display:none!important}}
@media(max-width:840px){.mode-shell{grid-template-columns:1fr!important}}
'''
    css_path.write_text(css,encoding='utf-8')

test=test_path.read_text(encoding='utf-8')
for assertion in [
    "assert 'renderModeInspector' in app\n",
    "assert 'UX_V2_SHARED_MODE_INSPECTOR' in css\n",
]:
    if assertion not in test:
        test+='\n'+assertion
test_path.write_text(test,encoding='utf-8')

check=app_path.read_text(encoding='utf-8')
for required in ('renderModeInspector','Resize inspector','mode-inspector'):
    if required not in check:
        raise SystemExit(f'Shared inspector contract missing: {required}')
print('Shared contextual inspector hotfix applied')
