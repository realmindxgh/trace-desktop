from pathlib import Path

p=Path('tests/ux_foundation_v2.mjs')
s=p.read_text(encoding='utf-8')
if 'async function trustSafetyUx()' not in s:
    terminal='await fresh();await emptyProject();await populated();await contextualData();await keyboardProductivity();await contextualShell();await researcherJourney();await browser.close();'
    if terminal not in s:
        raise SystemExit('Researcher-journey browser terminal sequence changed')
    add=r'''
async function trustSafetyUx(){
  const ctx=await browser.newContext({viewport:{width:1600,height:900}});
  await ctx.addInitScript(()=>localStorage.setItem('trace-v010-state',JSON.stringify({
    project:{id:'p',title:'Trust study',methodology:'RTA',codingMode:'manual',researchQuestions:[],researchQuestionRecords:[]},activeSection:'Data',dataContext:'sources',activeParticipant:'P01',activeSourceId:'s1',openSourceTabs:['s1'],
    participants:[{id:'P01',internalId:'p1',role:'Participant'}],
    transcript:[{speaker:'P01',text:'Access was difficult',sourceId:'s1',segmentId:'seg1',startChar:0,endChar:20}],
    importedSources:[{id:'s1',name:'Interview 01',kind:'text',participantId:'p1',segments:[{id:'seg1',speaker:'P01',text:'Access was difficult'}],codings:[]}],
    codes:[{id:'c1',name:'Access',description:'',color:'#4466aa'}],coders:[{id:'u1',name:'Researcher'}],activeCoderId:'u1',
    codingRefs:[{id:'r1',sourceId:'s1',codeId:'c1',participantId:'p1',segmentId:'seg1',text:'Access was difficult'}],allCodingRefs:[{id:'r1',sourceId:'s1',codeId:'c1',participantId:'p1',segmentId:'seg1',text:'Access was difficult'}],
    annotations:[{id:'a1',sourceId:'s1',startOffset:0,endOffset:6,body:'Important'}],evidenceAnchors:[{id:'e1',sourceId:'s1',startOffset:0,endOffset:6,exactText:'Access'}],
    memos:[{id:'m1',name:'Source memo',targetType:'source',targetId:'s1',text:'Analytical note'}],sourceProperties:[],sourceCollections:[{id:'col1',name:'Interviews',sourceIds:['s1']}],
    importQueue:[{id:'q1',name:'damaged-project.qdpx',status:'error',message:'Trace could not safely import this project file.',technicalDetails:'SQLITE_CORRUPT: database disk image is malformed'}],
    themes:[],findingsSections:[],findingsEvidence:[],backups:[],audit:[],mediaSelections:[{id:'ms1',sourceId:'s1',startTime:2,endTime:6}],mediaCodings:[],mediaPayloads:{},savedAt:Date.now()
  })));
  const page=await ctx.newPage();await page.goto(base,{waitUntil:'networkidle'});

  // Source deletion must disclose all project relationships before any destructive write.
  await page.click('[data-manage-source="s1"]');
  await page.click('#sm-delete');
  const warning=await page.locator('.confirmation-modal .modal-note').innerText().catch(()=> '');
  for(const label of ['coded passage','annotation','evidence anchor','saved media selection','source memo','collection','P01'])if(!warning.includes(label))errors.push(`source delete warning does not disclose ${label}`);
  if(!/original external file remains unchanged/i.test(warning))errors.push('source delete warning does not distinguish project deletion from the original external file');
  await page.click('#confirm-cancel');

  // Failed imports show human copy first and keep implementation details behind disclosure.
  await page.click('[data-data-context="imports"]');
  const result=page.locator('.import-result.error').filter({hasText:'damaged-project.qdpx'});
  const visibleCopy=await result.locator('small').innerText().catch(()=> '');
  if(/SQLITE|database disk image/i.test(visibleCopy))errors.push('database/framework detail leaked into primary import error copy');
  if(!await result.locator('details').count())errors.push('failed import has no Technical details disclosure');
  const technical=await result.locator('details').textContent().catch(()=> '');
  if(!/SQLITE_CORRUPT/.test(technical))errors.push('failed import Technical details lost troubleshooting evidence');
  await ctx.close();
}
'''
    s=s.replace(terminal,add+'\nawait fresh();await emptyProject();await populated();await contextualData();await keyboardProductivity();await contextualShell();await researcherJourney();await trustSafetyUx();await browser.close();',1)
    p.write_text(s,encoding='utf-8')

check=p.read_text(encoding='utf-8')
for required in ('async function trustSafetyUx()','source delete warning','SQLITE_CORRUPT','original external file remains unchanged'):
    if required not in check:
        raise SystemExit(f'Trust browser coverage missing: {required}')
print('Phase 8 browser gate expanded for rendered trust and destructive-action disclosure')
