import { createRequire } from 'node:module';
import { spawn, spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const exe=process.env.TRACE_INSTALLED_EXE;
const playwrightRoot=process.env.TRACE_PLAYWRIGHT_ROOT;
const userData=process.env.TRACE_WEBVIEW_USER_DATA;
const evidenceDir=process.env.TRACE_INSTALLED_EVIDENCE_DIR||path.resolve('installed-ux-evidence');
const importFile=process.env.TRACE_INSTALLED_IMPORT_FILE;
if(!exe||!fs.existsSync(exe))throw new Error(`TRACE_INSTALLED_EXE is missing: ${exe||'<unset>'}`);
if(!playwrightRoot)throw new Error('TRACE_PLAYWRIGHT_ROOT is required.');
if(!userData)throw new Error('TRACE_WEBVIEW_USER_DATA is required.');
if(!importFile||!fs.existsSync(importFile))throw new Error(`TRACE_INSTALLED_IMPORT_FILE is missing: ${importFile||'<unset>'}`);
fs.mkdirSync(userData,{recursive:true});fs.mkdirSync(evidenceDir,{recursive:true});
const requireFromSource=createRequire(path.resolve(playwrightRoot,'package.json'));
const { chromium }=requireFromSource('playwright');

const failures=[];
const check=(ok,msg)=>{if(!ok)failures.push(msg)};
const wait=ms=>new Promise(r=>setTimeout(r,ms));
async function launchInstalled(port){
  const env={...process.env,WEBVIEW2_USER_DATA_FOLDER:userData,WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS:`--remote-debugging-port=${port} --remote-allow-origins=*`};
  const child=spawn(exe,[],{env,windowsHide:false,stdio:'ignore'});
  let browser=null,last=null;
  for(let i=0;i<90;i++){
    if(child.exitCode!==null)throw new Error(`Installed Trace exited before WebView2 became available (exit ${child.exitCode}).`);
    try{browser=await chromium.connectOverCDP(`http://127.0.0.1:${port}`);break}catch(err){last=err;await wait(500)}
  }
  if(!browser){killTree(child.pid);throw new Error(`Could not attach to installed WebView2 on port ${port}: ${String(last)}`)}
  const contexts=browser.contexts();
  const pages=contexts.flatMap(c=>c.pages());
  let page=pages.find(p=>!/^devtools:/i.test(p.url()))||pages[0];
  if(!page){await wait(500);page=browser.contexts().flatMap(c=>c.pages())[0]}
  if(!page){await browser.close().catch(()=>{});killTree(child.pid);throw new Error('Installed Trace exposed no WebView page.')}
  await page.waitForLoadState('domcontentloaded').catch(()=>{});
  await page.waitForSelector('body',{timeout:20000});
  return {child,browser,page};
}
function killTree(pid){if(!pid)return;spawnSync('taskkill',['/PID',String(pid),'/T','/F'],{windowsHide:true,stdio:'ignore'});}
async function closeInstalled(session){try{await session.browser.close()}catch{}killTree(session.child.pid);await wait(1500)}
async function screenshot(page,name){await page.screenshot({path:path.join(evidenceDir,`${name}.png`),fullPage:false});}

let first=await launchInstalled(9331);
let page=first.page;
await page.waitForSelector('.trace-home',{timeout:20000});
const firstText=await page.locator('body').innerText();
check(await page.locator('#home-new').count()===1,'Installed fresh launch has no New Project action');
check(await page.locator('#home-open').count()===1,'Installed fresh launch has no Open Project action');
check(await page.locator('#home-import').count()===1,'Installed fresh launch has no Import Project action');
check(await page.locator('#home-recover').count()===1,'Installed fresh launch has no Recover Project action');
check(!/Downloading Videos/i.test(firstText),'Installed fresh launch leaked the old Downloading Videos project');
check(!/(^|\s)P01(\s|$)/m.test(firstText),'Installed fresh launch fabricated P01');
check(await page.locator('.project-frame').count()===0,'Installed fresh launch opened a project workspace instead of Trace Home');
await screenshot(page,'01-installed-fresh-home');

// Exercise the researcher journey against the real installed Tauri/WebView2 application.
await page.click('#home-new');
await page.fill('#p-title','Installed UX journey');
await page.click('#create-project');
await page.waitForSelector('.project-overview',{timeout:20000});
check(await page.locator('.project-overview').count()===1,'Installed New Project did not open Project Overview');
await page.locator('#file-import').setInputFiles(importFile);
await page.waitForFunction(()=>document.querySelector('.project-health')?.textContent?.includes('1'),null,{timeout:20000}).catch(()=>{});
check(await page.locator('.project-health article').filter({hasText:'Sources'}).filter({hasText:'1'}).count()>0,'Installed import did not update source count');

await page.click('[data-section="Code"]');
await page.waitForSelector('.transcript-line p',{timeout:20000});
await page.keyboard.press('Control+Shift+C');
await page.fill('#ce-name','Access barriers');
await page.fill('#ce-description','Difficulties obtaining needed support');
await page.click('#ce-save');
await page.locator('.transcript-line p').first().evaluate(el=>{const node=el.firstChild;if(!node)return;const range=document.createRange();range.setStart(node,0);range.setEnd(node,Math.min(17,node.textContent.length));const sel=window.getSelection();sel.removeAllRanges();sel.addRange(range);el.closest('#transcript-scroll')?.dispatchEvent(new MouseEvent('mouseup',{bubbles:true}));});
await page.click('#tool-code');
if(await page.locator('[data-mode="manual"]').count())await page.click('[data-mode="manual"]');
await page.locator('[data-code]').filter({hasText:'Access barriers'}).first().click();
check(await page.locator('.coding-stripes i[title="Access barriers"]').count()>0,'Installed journey did not visibly apply Access barriers');

await page.keyboard.press('Control+Shift+M');
await page.fill('#me-name','Access memo');
await page.fill('#me-body','Access difficulty appears before peer support changes the experience.');
await page.click('#me-save');
await page.click('[data-section="Themes"]');
await page.click('#new-theme');
await page.fill('#te-name','Support pathways');
await page.locator('[data-theme-code]').filter({hasText:'Access barriers'}).check();
await page.click('#te-save');
check(await page.getByText('Support pathways',{exact:true}).count()>0,'Installed journey did not create Support pathways');

await page.click('[data-section="Analyse"]');
check(await page.locator('[data-analysis-tab="matrix"]').count()>0,'Installed Analyse workspace is missing');
await page.click('[data-section="Write"]');
check(await page.locator('[data-write-target^="theme:"]').count()>0,'Installed theme did not become a Write target');
const findings='Participants described initial access barriers, with support pathways shaping how help was experienced.';
await page.fill('#findings-body',findings);
await page.click('#save-findings');
await page.waitForTimeout(400);
check(await page.locator('#write-save-status').filter({hasText:/Saved/}).count()>0,'Installed findings did not save');
await screenshot(page,'02-installed-populated-write');

await page.click('#rail-home');
await page.waitForSelector('.trace-home',{timeout:10000});
check(await page.locator('#resume-current').count()>0,'Installed project is not resumable from Trace Home before restart');
await screenshot(page,'03-installed-home-after-work');
await closeInstalled(first);

// Relaunch the real installed process with the same WebView2 profile. Default behavior must still be Home,
// and the researcher must be able to resume the project without losing analytical state.
let second=await launchInstalled(9332);page=second.page;
await page.waitForSelector('.trace-home',{timeout:20000});
check(await page.locator('#resume-current').count()>0,'Installed close/reopen lost the current project launcher');
check(await page.locator('.project-frame').count()===0,'Installed close/reopen bypassed Home without an explicit resume preference');
await page.click('#resume-current');
await page.click('[data-section="Themes"]');
check(await page.getByText('Support pathways',{exact:true}).count()>0,'Installed close/reopen lost the saved theme');
await page.click('[data-section="Write"]');
check((await page.locator('#findings-body').inputValue().catch(()=>''))===findings,'Installed close/reopen lost the saved findings');
await page.click('[data-section="Code"]');
check(await page.locator('.coding-stripes i[title="Access barriers"]').count()>0,'Installed close/reopen lost the applied coding');
await screenshot(page,'04-installed-resumed-code');
await closeInstalled(second);

fs.writeFileSync(path.join(evidenceDir,'installed-smoke.json'),JSON.stringify({freshHome:true,createdProject:true,importedSource:true,coding:true,memo:true,theme:true,analyse:true,findings:true,closedAndReopened:true,failures},null,2));
if(failures.length){console.error(failures.join('\n'));process.exit(1)}
console.log('Installed Trace WebView2 researcher journey: green');
