from pathlib import Path

p=Path('tests/ux_foundation_v2.mjs')
s=p.read_text(encoding='utf-8')
if 'async function researcherJourney()' not in s:
    terminal="await fresh();await emptyProject();await populated();await contextualData();await keyboardProductivity();await contextualShell();await browser.close();"
    if terminal not in s:
        raise SystemExit('Expanded browser terminal marker not found')
    fn=r'''
async function researcherJourney(){
  const ctx=await browser.newContext({viewport:{width:1600,height:900}});
  const page=await ctx.newPage();
  await page.goto(base,{waitUntil:'networkidle'});
  await page.click('#home-new');
  await page.fill('#p-title','Researcher journey');
  await page.click('#create-project');
  if(!await page.locator('.project-overview').count())errors.push('journey project did not open Project Overview');
  await page.locator('#file-import').setInputFiles({name:'Interview 01.txt',mimeType:'text/plain',buffer:Buffer.from('Access to support was difficult at first, but peer help changed the experience.')});
  await page.waitForTimeout(150);
  if(!await page.locator('.project-health article').filter({hasText:'Sources'}).filter({hasText:'1'}).count())errors.push('journey import did not update project source count');
  await page.click('[data-section="Code"]');
  if(!await page.locator('.transcript-line p').count())errors.push('journey imported transcript is not codable');
  await page.keyboard.press('Control+Shift+C');
  await page.fill('#ce-name','Access barriers');
  await page.fill('#ce-description','Difficulties obtaining needed support');
  await page.click('#ce-save');
  await page.locator('.transcript-line p').first().evaluate(el=>{const node=el.firstChild;if(!node)return;const range=document.createRange();range.setStart(node,0);range.setEnd(node,Math.min(17,node.textContent.length));const sel=window.getSelection();sel.removeAllRanges();sel.addRange(range);el.closest('#transcript-scroll')?.dispatchEvent(new MouseEvent('mouseup',{bubbles:true}));});
  await page.click('#tool-code');
  if(await page.locator('[data-mode="manual"]').count())await page.click('[data-mode="manual"]');
  await page.locator('[data-code]').first().click();
  if(!await page.locator('.coding-stripes i[title="Access barriers"]').count())errors.push('journey coding did not attach the selected code visibly to the transcript');
  await page.keyboard.press('Control+Shift+M');
  await page.fill('#me-name','Access memo');
  await page.fill('#me-body','Access difficulty appears before peer support changes the experience.');
  await page.click('#me-save');
  await page.click('[data-section="Themes"]');
  await page.click('#new-theme');
  await page.fill('#te-name','Support pathways');
  await page.locator('[data-theme-code]').first().check();
  await page.click('#te-save');
  if(!await page.getByText('Support pathways',{exact:true}).count())errors.push('journey theme was not created');
  await page.click('[data-section="Analyse"]');
  if(!await page.locator('[data-analysis-tab="matrix"]').count())errors.push('journey Analyse workspace missing evidence navigation');
  await page.click('[data-section="Write"]');
  if(!await page.locator('[data-write-target^="theme:"]').count())errors.push('journey theme did not become a writing target');
  await page.fill('#findings-body','Participants described initial access barriers, with peer support changing how support was experienced.');
  await page.click('#save-findings');
  if(!await page.locator('#write-save-status').filter({hasText:/Saved/}).count())errors.push('journey findings did not save');
  await page.click('#rail-home');
  if(!await page.locator('#resume-current').count())errors.push('journey current project is not recoverable from Trace Home');
  await page.click('#resume-current');
  await page.click('[data-section="Themes"]');
  if(!await page.getByText('Support pathways',{exact:true}).count())errors.push('journey theme did not survive Home/resume cycle');
  await page.click('[data-section="Write"]');
  if((await page.locator('#findings-body').inputValue().catch(()=>''))!=='Participants described initial access barriers, with peer support changing how support was experienced.')errors.push('journey findings did not survive Home/resume cycle');
  await ctx.close();
}
'''
    s=s.replace(terminal,fn+'\nawait fresh();await emptyProject();await populated();await contextualData();await keyboardProductivity();await contextualShell();await researcherJourney();await browser.close();',1)
    p.write_text(s,encoding='utf-8')

check=p.read_text(encoding='utf-8')
for required in ('async function researcherJourney()','Researcher journey','Access barriers','Support pathways','resume-current','data-mode="manual"','coding-stripes i[title="Access barriers"]'):
    if required not in check:
        raise SystemExit(f'Researcher journey gate missing: {required}')
print('End-to-end researcher journey browser gate injected')
