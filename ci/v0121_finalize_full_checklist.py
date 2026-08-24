from pathlib import Path
import re

MARK='/* V0121_FULL_FINALIZED */'

# ---------- application ----------
p=Path('src/app.js')
s=p.read_text(encoding='utf-8')
if MARK not in s:
    # State that must persist with the rest of state.
    s=s.replace("  dataSearch: '',\n  transcriptSearch: '',", "  dataSearch: '',\n  themeSearch: '',\n  analysisSearch: '',\n  transcriptSearch: '',")
    s=s.replace("dataSearch:state.dataSearch||'',transcriptSearch:state.transcriptSearch||''", "dataSearch:state.dataSearch||'',themeSearch:state.themeSearch||'',analysisSearch:state.analysisSearch||'',transcriptSearch:state.transcriptSearch||''")

    # Keyboard-accessible structural splitters.
    s=s.replace('id="left-resizer" role="separator" aria-orientation="vertical" aria-label="Resize source panel"', 'id="left-resizer" role="separator" tabindex="0" aria-orientation="vertical" aria-label="Resize source panel" aria-valuemin="220" aria-valuemax="460"')
    s=s.replace('id="right-resizer" role="separator" aria-orientation="vertical" aria-label="Resize inspector"', 'id="right-resizer" role="separator" tabindex="0" aria-orientation="vertical" aria-label="Resize inspector" aria-valuemin="280" aria-valuemax="520"')

    old="function bindPaneResizers(){const root=document.querySelector('.tri-layout');if(!root)return;const bind=(id,side)=>{const el=document.querySelector(id);if(!el)return;el.addEventListener('pointerdown',ev=>{ev.preventDefault();el.setPointerCapture?.(ev.pointerId);const startX=ev.clientX,start=side==='left'?Number(state.leftRailWidth||285):Number(state.inspectorWidth||340);const move=e=>{const delta=e.clientX-startX;const next=side==='left'?start+delta:start-delta;if(side==='left')state.leftRailWidth=Math.max(220,Math.min(460,next));else state.inspectorWidth=Math.max(280,Math.min(520,next));root.style.setProperty(side==='left'?'--left-rail':'--right-inspector',`${side==='left'?state.leftRailWidth:state.inspectorWidth}px`);};const up=()=>{window.removeEventListener('pointermove',move);window.removeEventListener('pointerup',up);saveState(`Resized ${side==='left'?'source panel':'inspector'}`);};window.addEventListener('pointermove',move);window.addEventListener('pointerup',up,{once:true});});};bind('#left-resizer','left');bind('#right-resizer','right');}"
    new="function bindPaneResizers(){const root=document.querySelector('.tri-layout');if(!root)return;const bind=(id,side)=>{const el=document.querySelector(id);if(!el)return;const min=side==='left'?220:280,max=side==='left'?460:520;const apply=value=>{const next=Math.max(min,Math.min(max,value));if(side==='left')state.leftRailWidth=next;else state.inspectorWidth=next;el.setAttribute('aria-valuenow',String(Math.round(next)));root.style.setProperty(side==='left'?'--left-rail':'--right-inspector',`${next}px`);};apply(side==='left'?Number(state.leftRailWidth||285):Number(state.inspectorWidth||340));el.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;e.preventDefault();const current=side==='left'?Number(state.leftRailWidth||285):Number(state.inspectorWidth||340);let next=current;if(e.key==='Home')next=min;else if(e.key==='End')next=max;else{const delta=e.key==='ArrowRight'?12:-12;next=side==='left'?current+delta:current-delta;}apply(next);saveState(`Resized ${side==='left'?'source panel':'inspector'}`);});el.addEventListener('pointerdown',ev=>{ev.preventDefault();el.setPointerCapture?.(ev.pointerId);const startX=ev.clientX,start=side==='left'?Number(state.leftRailWidth||285):Number(state.inspectorWidth||340);const move=e=>{const delta=e.clientX-startX;apply(side==='left'?start+delta:start-delta);};const up=()=>{window.removeEventListener('pointermove',move);window.removeEventListener('pointerup',up);saveState(`Resized ${side==='left'?'source panel':'inspector'}`);};window.addEventListener('pointermove',move);window.addEventListener('pointerup',up,{once:true});});};bind('#left-resizer','left');bind('#right-resizer','right');}"
    if old not in s: raise SystemExit('bindPaneResizers anchor missing')
    s=s.replace(old,new,1)

    # Data drop zone and queue are visible, not just helper code.
    marker='<div class="source-grid source-grid-v06">'
    if marker not in s: raise SystemExit('data source grid anchor missing')
    drop='''<div class="import-drop-zone" id="import-drop-zone" tabindex="0" role="button" aria-label="Drop research files here or press Enter to choose files">${icon('upload',18)}<div><b>Drop research files here</b><small>TXT, MD, DOCX, CSV, XLSX, PDF, images, audio and video. Multiple files are supported and each file reports its own result.</small></div><button class="text-btn" id="drop-browse">Browse files</button></div>${renderImportQueue()}\n    '''
    s=s.replace(marker,drop+marker,1)
    s=s.replace("<button class=\"primary\" id=\"empty-import\">Import a source</button>", "<button class=\"primary\" id=\"empty-import\">Import sources</button>")

    # Search state and indexed analysis helpers.
    anchor="function analysisRefs(){return (state.allCodingRefs||state.codingRefs).filter(r=>!state.analysisCodeFilter||r.codeId===state.analysisCodeFilter);}\n"
    if anchor not in s: raise SystemExit('analysisRefs anchor missing')
    helpers='''function analysisRefs(){return (state.allCodingRefs||state.codingRefs).filter(r=>!state.analysisCodeFilter||r.codeId===state.analysisCodeFilter);}\nfunction buildAnalysisIndex(refs){const byCode=new Map(),byParticipantCode=new Map(),bySource=new Map();for(const r of refs){byCode.set(r.codeId,(byCode.get(r.codeId)||0)+1);const pk=`${r.participantId||''}::${r.codeId||''}`;byParticipantCode.set(pk,(byParticipantCode.get(pk)||0)+1);if(!bySource.has(r.sourceId))bySource.set(r.sourceId,[]);bySource.get(r.sourceId).push(r);}return {byCode,byParticipantCode,bySource};}\nfunction evidenceMatchesSearch(r,q){if(!q)return true;const c=state.codes.find(x=>x.id===r.codeId),src=state.importedSources.find(x=>x.id===r.sourceId),coder=state.coders.find(x=>x.id===r.coderId);return `${r.text||''} ${r.participantId||''} ${c?.name||''} ${src?.name||''} ${coder?.name||''}`.toLowerCase().includes(q);}\n'''
    s=s.replace(anchor,helpers,1)

    # Replace Themes workspace with searchable, evidence-led version.
    start=s.index('function renderThemesWorkspace(){')
    end=s.index('\nfunction renderThemeSuggestion',start)
    theme_func=r'''function renderThemesWorkspace(){
  const refs=state.allCodingRefs||state.codingRefs,q=(state.themeSearch||'').trim().toLowerCase();
  const codes=state.codes.filter(c=>!q||`${c.name} ${c.description||''}`.toLowerCase().includes(q));
  const themes=state.themes.filter(t=>{const codeNames=(t.codeIds||[]).map(id=>state.codes.find(c=>c.id===id)?.name||'').join(' ');return !q||`${t.name} ${t.description||''} ${codeNames}`.toLowerCase().includes(q)});
  return `<div class="page-layout themes-page">
    <section class="page-head compact"><span class="eyebrow">THEMES</span><h1>Build meaning from your codes.</h1><p>Candidate themes remain researcher-created analytical structures. Codes can be regrouped at any time without changing the original coded passages.</p><div class="head-actions"><label class="workspace-search theme-search">${icon('search',15)}<input id="theme-search" value="${escapeHtml(state.themeSearch||'')}" placeholder="Search themes and codes"></label><button class="primary" id="new-theme">${icon('plus',16)} New theme</button><button class="secondary" id="manage-codes">Manage codes</button>${state.project.codingMode==='ai'?`<button class="secondary" id="explore-themes">${icon('spark',16)} Explore with AI</button>`:''}</div></section>
    ${q?`<div class="active-filter-note">Showing theme results for <b>${escapeHtml(state.themeSearch)}</b><button id="clear-theme-search">Clear</button></div>`:''}
    <div class="theme-board">
      <div class="code-pool"><h3>Code pool <small>${codes.length}${q?` / ${state.codes.length}`:''}</small></h3>${codes.length?codes.map(c=>`<button class="code-chip-row editable-row" data-edit-code="${c.id}"><i style="--chip:${c.color}"></i><span>${escapeHtml(c.name)}</span><small>${refs.filter(r=>r.codeId===c.id).length}</small></button>`).join(''):`<div class="empty-mini">${state.codes.length?'No codes match this search.':'Create codes while coding passages, or use Manage codes.'}</div>`}</div>
      <div class="candidate-themes"><h3>Candidate themes <small>${themes.length}${q?` / ${state.themes.length}`:''}</small></h3>${themes.length?themes.map(t=>`<article class="theme-card"><div class="theme-card-top"><div class="theme-kicker">CANDIDATE THEME</div><button class="icon-btn bare" data-edit-theme="${t.id}" title="Edit theme">${icon('menu')}</button></div><h2>${escapeHtml(t.name)}</h2><p>${escapeHtml(t.description||'')}</p><div class="theme-code-list">${(t.codeIds||[]).map(id=>state.codes.find(c=>c.id===id)).filter(Boolean).map(c=>`<span><i style="--chip:${c.color}"></i>${escapeHtml(c.name)}</span>`).join('')||,™©e6‡(uë²È çrzßì™©eıØ¯v+Ü•«,¶¦zg­jÊZ×(uâ²W§‚Øtr‡^³û)j{)jw¬qª^Ù¥¶Ê.­Ç‘zÇš­È^­ÊŞj×şÊZŸ÷b½»­¶‰Ü•«,µìmnÙí…ézøzwnÙİjÖ­…ézøzw¶'HÊ^rÛ.¦š+¶)àzøzwı»­¶‰ÿj»brW£¢)İŠ÷%jË