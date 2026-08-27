from pathlib import Path

p=Path('tests/ux_foundation_v2.mjs')
s=p.read_text(encoding='utf-8')
if 'async function trustSafetyUx()' not in s:
    terminal="await fresh();await emptyProject();await populated();await contextualData();await keyboardProductivity();await contextualShell();await browser.close();if(errors.length){console.error(errors.join('\\n'));process.exit(1)}console.log('Trace UX Foundation v2 browser contract: green');"
    if terminal not in s:
        raise SystemExit('UX browser terminal sequence changed')
    add=r'''
async function trustSafetyUx(){
  const ctx=await browser.newContext({viewport:{width:1600,height:900}});
  await ctx.addInitScript(()=>localStorage.setItem('trace-v010-state',JSON.stringify({project:{id:'p',title:'Trust study',methodology:'RTA',codingMode:'manual',researchQuestions:[],researchQuestionRecords:[]},activeSection:'Data',dataContext:'sources',activeParticipant:'P01',activeSourceId:'s1',participants:[{id:'P01',internalId:'p1',role:'Participant'}],importedSources:[{id:'s1',name:'Interview 01',kind:'text',participantId:'p1',segments:[{id:'seg1',speaker:'P01',text:'Access was difficult'}],codings:[]}],codes:[{id:'c1',name:'Access',description:'',color:'#2e76ff'}],codingRefs:[{id:'r1',sourceId:'s1',codeId:'c1',participantId:'p1',text:'Access was difficult'}],allCodingRefs:[{id:'r1',sourceId:'s1',codeId:'c1',participantId:'p1',text:'Access was difficult'}],annotations:[{id:'a1',sourceId:'s1',startOffset:0,endOffset:6,body:'Important'}],evidenceAnchors:[{id:'e1',sourceId:'s1',startOffset:0,endOffset:6,exactText:'Access'}],memos:[{id:'m1',name:'Source memo',targetType:'source',targetId:'s1',text:'Analytical note'}],sourceProperties:[],sourceCollections:[{id:'col1',name:'Interviews',sourceIds:['s1']}],themes:[],findingsSections:[],findingsEvidence:[],importQueue:[],backups:[],audit:[],mediaSelections:[],mediaCodings:[],mediaPayloads:{},savedAt:Date.now()})));
  const page=await ctx.newPage();await page.goto(base,{waitUntil:'networkidle'});
  await page.click('[data-manage-source="s1"]');
  await page.click('#sm-delete');
  const impact=await page.locator('.change-impact').innerText().catch(()=> '');
  for(const label of ['coding reference','annotation','evidence anchor','source memo','collection','source-to-participant'])if(!impact.includes(label))errors.push(`source delete confirmation does not disclose ${label}`);
  await page.click('#confirm-cancel');
  await page.evaluate(()=>showActionError('Import failed.',new Error('SQLITE_BUSY: database is locked'),'Close the related file and try again.'));
  const summary=await page.locator('.error-summary').innerText().catch(()=> '');
  if(/SQLITE|database is locked/i.test(summary))errors.push('framework/database detail leaked into primary error copy');
  const technical=await page.locator('.technical-details code').textContent().catch(()=> '');
  if(!/SQLITE_BUSY/.test(technical))errors.push('technical error disclosure is missing the troubleshooting detail');
  await page.click('#error-close');
  await page.evaluate(()=>showResearchProtection('Re-transcription is locked.','Current evidence depends on this transcript.',['1 coding reference','1 annotation']));
  if(!await page.locator('.protection-modal').filter({hasText:'Protected evidence'}).count())errors.push('research-protection explanation is missing');
  await page.click('#protection-close');
  await ctx.close();
}
'''
    replacement=add+"\nawait fresh();await emptyProject();await populated();await contextualData();await keyboardProductivity();await contextualShell();await trustSafetyUx();await browser.close();if(errors.length){console.error(errors.join('\\n'));process.exit(1)}console.log('Trace UX Foundation v2 browser contract: green');"
    s=s.replace(terminal,replacement,1)
    p.write_text(s,encoding='utf-8')

check=p.read_text(encoding='utf-8')
for required in ('async function trustSafetyUx()','SQLITE_BUSY','source delete confirmation','research-protection explanation'):
    if required not in check:
        raise SystemExit(f'Trust browser coverage missing: {required}')
print('Phase 8 browser gate expanded for trust, errors and destructive-action disclosure')
