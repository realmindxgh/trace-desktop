from pathlib import Path

p=Path('src/app.js')
tp=Path('tests/ux_foundation_v2_contract.py')
s=p.read_text(encoding='utf-8')

old_code="const refCount=(state.allCodingRefs||state.codingRefs).filter(r=>r.codeId===code.id).length,themeCount=state.themes.filter(t=>(t.codeIds||[]).includes(code.id)).length;if(!await confirmResearchAction(`Delete code \"${code.name}\"?`,`${refCount} coded passage${refCount===1?'':'s'} will lose this code and ${themeCount} candidate theme${themeCount===1?'':'s'} will lose the relationship. Source text, notes and memos will remain.`))return;"
new_code="const refCount=(state.allCodingRefs||state.codingRefs).filter(r=>r.codeId===code.id).length,themeCount=state.themes.filter(t=>(t.codeIds||[]).includes(code.id)).length,mediaCodeCount=(state.mediaCodings||[]).filter(r=>r.codeId===code.id).length,codeMemoCount=(state.memos||[]).filter(m=>m.targetType==='code'&&m.targetId===code.id).length;if(!await confirmResearchAction(`Delete code \"${code.name}\"?`,`${refCount} coded passage${refCount===1?'':'s'} and ${mediaCodeCount} coded media selection${mediaCodeCount===1?'':'s'} will lose this code; ${themeCount} candidate theme${themeCount===1?'':'s'} will lose the relationship; and ${codeMemoCount} code memo${codeMemoCount===1?'':'s'} will be removed. Source text and original media remain unchanged.`))return;"
if old_code in s:
    s=s.replace(old_code,new_code,1)
elif 'mediaCodeCount' not in s:
    raise SystemExit('Current code-delete consequence anchor changed')

old_source="const sourceRefs=(state.allCodingRefs||state.codingRefs).filter(r=>r.sourceId===sourceId).length,sourceNotes=(state.annotations||[]).filter(a=>a.sourceId===sourceId).length,sourceMemos=state.memos.filter(m=>m.targetType==='source'&&m.targetId===sourceId).length,participantLabel=state.participants.find(p=>(p.internalId||p.id)===src.participantId)?.id||null;if(!await confirmResearchAction(`Delete ${src.name}?`,`${sourceRefs} coded passage${sourceRefs===1?'':'s'}, ${sourceNotes} annotation${sourceNotes===1?'':'s'} and ${sourceMemos} source memo${sourceMemos===1?'':'s'} are linked to this source${participantLabel?` and its ${participantLabel} relationship`:''}. Trace will remove those source-linked records with the source.`))return;"
new_source="const sourceRefs=(state.allCodingRefs||state.codingRefs).filter(r=>r.sourceId===sourceId).length,sourceNotes=(state.annotations||[]).filter(a=>a.sourceId===sourceId).length,sourceMemos=(state.memos||[]).filter(m=>m.targetType==='source'&&m.targetId===sourceId).length,sourceAnchors=(state.evidenceAnchors||[]).filter(a=>a.sourceId===sourceId).length,sourceMedia=(state.mediaSelections||[]).filter(a=>a.sourceId===sourceId).length,sourceCollections=(state.sourceCollections||[]).filter(c=>(c.sourceIds||[]).includes(sourceId)).length,participantLabel=state.participants.find(p=>(p.internalId||p.id)===src.participantId)?.id||null;if(!await confirmResearchAction(`Delete ${src.name}?`,`${sourceRefs} coded passage${sourceRefs===1?'':'s'}, ${sourceNotes} annotation${sourceNotes===1?'':'s'}, ${sourceAnchors} evidence anchor${sourceAnchors===1?'':'s'}, ${sourceMedia} saved media selection${sourceMedia===1?'':'s'} and ${sourceMemos} source memo${sourceMemos===1?'':'s'} are linked to this source. It also belongs to ${sourceCollections} collection${sourceCollections===1?'':'s'}${participantLabel?` and is linked to ${participantLabel}`:''}. Trace will remove those source-linked records from the project; the original external file remains unchanged.`))return;"
if old_source in s:
    s=s.replace(old_source,new_source,1)
elif 'sourceAnchors' not in s:
    raise SystemExit('Current source-delete consequence anchor changed')

p.write_text(s,encoding='utf-8')
t=tp.read_text(encoding='utf-8')
for a in [
    "assert 'mediaCodeCount' in app\n",
    "assert 'sourceAnchors' in app\n",
    "assert 'sourceCollections' in app\n",
]:
    if a not in t:t+='\n'+a
tp.write_text(t,encoding='utf-8')
print('Complete source/code consequence previews applied')
