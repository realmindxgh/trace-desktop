from pathlib import Path

p=Path('tests/ux_foundation_v2.mjs')
s=p.read_text(encoding='utf-8')
if 'async function contextualData()' not in s:
    marker='await fresh();await emptyProject();await populated();await browser.close();'
    add=r'''
async function contextualData(){
  const ctx=await browser.newContext({viewport:{width:1366,height:768}});
  await ctx.addInitScript(()=>localStorage.setItem('trace-v010-state',JSON.stringify({project:{id:'p',title:'Context study',methodology:'',codingMode:'manual',researchQuestions:[],researchQuestionRecords:[]},activeSection:'Data',dataContext:'sources',participants:[],importedSources:[],codes:[],themes:[],allCodingRefs:[],codingRefs:[],memos:[],annotations:[],sourceProperties:[],sourceCollections:[],importQueue:[],backups:[],audit:[],mediaSelections:[],mediaCodings:[],mediaPayloads:{},savedAt:Date.now()})));
  const page=await ctx.newPage();await page.goto(base,{waitUntil:'networkidle'});
  if(!await page.locator('[data-data-context="sources"]').count())errors.push('Data context pane is not functional');
  await page.click('[data-data-context="participants"]');
  if(!await page.locator('.data-truth-empty').filter({hasText:'No participants yet'}).count())errors.push('zero-participant Data workspace is not truthful');
  if(await page.getByText('P01',{exact:true}).count())errors.push('participant sub-workspace fabricated P01');
  await page.click('[data-data-context="collections"]');
  if(!await page.locator('.data-truth-empty').filter({hasText:'No collections yet'}).count())errors.push('Collections contextual workspace missing');
  await page.click('[data-data-context="imports"]');
  if(!await page.locator('.import-workspace-drop').count())errors.push('Imports contextual workspace missing');
  await ctx.close();
}
async function keyboardProductivity(){
  const ctx=await browser.newContext({viewport:{width:1600,height:900}});
  await ctx.addInitScript(()=>localStorage.setItem('trace-v010-state',JSON.stringify({project:{id:'p',title:'Keyboard study',methodology:'RTA',codingMode:'manual',researchQuestions:[],researchQuestionRecords:[]},activeSection:'Code',activeParticipant:'P01',activeSourceId:'s1',openSourceTabs:['s1','s2'],participants:[{id:'P01',internalId:'p1',role:'Participant'}],transcript:[{speaker:'P01',text:'First passage',sourceId:'s1',startChar:0,endChar:13}],importedSources:[{id:'s1',name:'Interview 01',kind:'text',participantId:'p1',segments:[{id:'a',speaker:'P01',text:'First passage'}],codings:[]},{id:'s2',name:'Interview 02',kind:'text',participantId:'p1',segments:[{id:'b',speaker:'P01',text:'Second passage'}],codings:[]}],codes:[{id:'c1',name:'Access',description:'',color:'#2e76ff'}],coders:[{id:'u1',name:'Researcher'}],activeCoderId:'u1',codingRefs:[],allCodingRefs:[],memos:[],annotations:[],themes:[],findingsSections:[],findingsEvidence:[],sourceProperties:[],sourceCollections:[],backups:[],audit:[],mediaSelections:[],mediaCodings:[],mediaPayloads:{},savedAt:Date.now()})));
  const page=await ctx.newPage();await page.goto(base,{waitUntil:'networkidle'});
  if(!await page.locator('.code-system-pane').count())errors.push('Code workspace does not use the code-system contextual pane');
  if(!await page.locator('[data-code-context="c1"]').count())errors.push('real code missing from Code contextual pane');
  await page.keyboard.press('Control+Shift+C');
  if(!await page.locator('#ce-name').count())errors.push('Ctrl+Shift+C did not open New Code');
  await page.locator('#ce-close').click();
  await page.keyboard.press('Control+Shift+M');
  if(!await page.locator('#me-name').count())errors.push('Ctrl+Shift+M did not open New Memo');
  await page.locator('#me-close').click();
  await page.keyboard.press('Control+K');
  if(!await page.locator('.command-palette kbd').filter({hasText:'Ctrl+Shift+C'}).count())errors.push('command palette does not teach productivity shortcuts');
  await page.keyboard.press('Escape');
  await page.keyboard.press('Alt+ArrowRight');
  const active=await page.locator('.document-tabs [aria-selected="true"] span').innerText().catch(()=> '');
  if(active!=='Interview 02')errors.push('Alt+Right did not move to the next source tab');
  await page.click('#trace-orb');
  if(!await page.locator('.trace-ai-modal').filter({hasText:'Interview 02'}).count())errors.push('Trace AI is not contextual to the active source');
  await ctx.close();
}
async function contextualShell(){
  const ctx=await browser.newContext({viewport:{width:1600,height:900}});
  await ctx.addInitScript(()=>localStorage.setItem('trace-v010-state',JSON.stringify({project:{id:'p',title:'Inspector study',methodology:'RTA',codingMode:'manual',researchQuestions:['How do participants describe access?'],researchQuestionRecords:[{id:'rq1',text:'How do participants describe access?'}]},activeSection:'Data',dataContext:'sources',analysisTab:'matrix',writeTarget:{type:'research_question',id:'rq1'},participants:[{id:'P01',internalId:'p1',role:'Participant'}],importedSources:[{id:'s1',name:'Interview 01',kind:'text',participantId:'p1',segments:[{id:'a',speaker:'P01',text:'Access was difficult'}],codings:[]}],activeSourceId:'s1',openSourceTabs:['s1'],codes:[{id:'c1',name:'Access barriers',description:'',color:'#2e76ff'}],themes:[{id:'t1',name:'Uneven access',codeIds:['c1']}],codingRefs:[{id:'r1',sourceId:'s1',codeId:'c1',participantId:'p1',text:'Access was difficult'}],allCodingRefs:[{id:'r1',sourceId:'s1',codeId:'c1',participantId:'p1',text:'Access was difficult'}],memos:[],annotations:[],findingsSections:[],findingsEvidence:[],sourceProperties:[],sourceCollections:[],importQueue:[],backups:[],audit:[],mediaSelections:[],mediaCodings:[],mediaPayloads:{},savedAt:Date.now()})));
  const page=await ctx.newPage();await page.goto(base,{waitUntil:'networkidle'});
  if(!await page.locator('.mode-shell .mode-inspector').count())errors.push('Data workspace shared inspector missing');
  if(!await page.locator('#right-resizer[aria-label="Resize inspector"]').count())errors.push('shared inspector resizer missing');
  await page.click('[data-section="Themes"]');
  if(!await page.locator('.themes-context-pane').count())errors.push('Themes contextual pane missing');
  if(!await page.locator('.mode-inspector').filter({hasText:'Theme context'}).count())errors.push('Themes inspector context missing');
  await page.click('[data-section="Analyse"]');
  if(!await page.locator('.mode-inspector').filter({hasText:'Analysis context'}).count())errors.push('Analyse inspector context missing');
  if(!await page.locator('[data-analysis-tab="matrix"]').count())errors.push('Analyse contextual navigation missing');
  await page.click('[data-section="Write"]');
  if(!await page.locator('.write-context-pane').count())errors.push('Write contextual outline missing');
  if(!await page.locator('[data-write-target="research_question:rq1"]').count())errors.push('Write contextual research-question target missing');
  if(!await page.locator('.mode-inspector').filter({hasText:'Writing context'}).count())errors.push('Write inspector context missing');
  await page.click('#toggle-inspector');
  if(!await page.locator('.mode-shell.right-collapsed').count())errors.push('shared inspector does not collapse');
  await ctx.close();
}
'''
    if marker not in s:
        raise SystemExit('Browser test terminal marker not found')
    s=s.replace(marker,add+'\nawait fresh();await emptyProject();await populated();await contextualData();await keyboardProductivity();await contextualShell();await browser.close();',1)
    p.write_text(s,encoding='utf-8')

check=p.read_text(encoding='utf-8')
for required in ('async function contextualData()','async function keyboardProductivity()','async function contextualShell()','Ctrl+Shift+C','Alt+ArrowRight','Writing context','Resize inspector'):
    if required not in check:
        raise SystemExit(f'Expanded browser gate missing: {required}')
print('Phase 8 browser gate expanded for contextual Data, Code, Themes, Analyse, Write, inspector and keyboard productivity')
