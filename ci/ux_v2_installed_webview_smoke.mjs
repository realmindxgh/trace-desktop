import { createRequire } from 'node:module';
import { spawn, spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const exe=process.env.TRACE_INSTALLED_EXE;
const playwrightRoot=process.env.TRACE_PLAYWRIGHT_ROOT;
const userData=process.env.TRACE_WEBVIEW_USER_DATA;
const evidenceDir=process.env.TRACE_INSTALLED_EVIDENCE_DIR||path.resolve('installed-ux-evidence');
let importFile=process.env.TRACE_INSTALLED_IMPORT_FILE;
let surveyFile=process.env.TRACE_INSTALLED_SURVEY_FILE;
let pdfFile=process.env.TRACE_INSTALLED_PDF_FILE;
let audioFile=process.env.TRACE_INSTALLED_AUDIO_FILE;
fs.mkdirSync(evidenceDir,{recursive:true});
const diagnosticPath=path.join(evidenceDir,'installed-smoke-diagnostic.jsonl');
const diagnose=(event,data={})=>{
  try{fs.appendFileSync(diagnosticPath,JSON.stringify({at:new Date().toISOString(),event,...data})+'\n')}catch{}
};
let activePage=null;
async function captureFatal(reason){
  const err=reason instanceof Error?reason:new Error(String(reason));
  diagnose('fatal',{message:err.message,stack:err.stack||''});
  if(activePage){
    try{fs.writeFileSync(path.join(evidenceDir,'fatal-page.html'),await activePage.content())}catch{}
    try{fs.writeFileSync(path.join(evidenceDir,'fatal-page.txt'),await activePage.locator('body').innerText())}catch{}
    try{await activePage.screenshot({path:path.join(evidenceDir,'fatal-page.png'),fullPage:false})}catch{}
  }
  console.error(err.stack||err.message);
}
process.on('uncaughtException',err=>{captureFatal(err).finally(()=>process.exit(1))});
process.on('unhandledRejection',err=>{captureFatal(err).finally(()=>process.exit(1))});

// Generate the additional acceptance files on the runner itself so the exact installed-app gate
// always exercises a spreadsheet, searchable PDF and decodable media without network fixtures.
if(!surveyFile||!pdfFile||!audioFile){
  const fixtureDir=path.join(evidenceDir,'fixtures');
  const generator=path.resolve(process.cwd(),'control','ci','ux_v2_make_acceptance_fixtures.py');
  if(!fs.existsSync(generator))throw new Error(`Acceptance fixture generator is missing: ${generator}`);
  const generated=spawnSync('python',[generator],{env:{...process.env,TRACE_ACCEPTANCE_FIXTURE_DIR:fixtureDir},encoding:'utf8'});
  if(generated.status!==0)throw new Error(`Acceptance fixture generation failed: ${generated.stderr||generated.stdout}`);
  importFile=importFile||path.join(fixtureDir,'interview.txt');
  surveyFile=surveyFile||path.join(fixtureDir,'participants.xlsx');
  pdfFile=pdfFile||path.join(fixtureDir,'evidence.pdf');
  audioFile=audioFile||path.join(fixtureDir,'interview-audio.wav');
}
for(const [name,value] of Object.entries({TRACE_INSTALLED_EXE:exe,TRACE_PLAYWRIGHT_ROOT:playwrightRoot,TRACE_WEBVIEW_USER_DATA:userData,TRACE_INSTALLED_IMPORT_FILE:importFile,TRACE_INSTALLED_SURVEY_FILE:surveyFile,TRACE_INSTALLED_PDF_FILE:pdfFile,TRACE_INSTALLED_AUDIO_FILE:audioFile})){
  if(!value)throw new Error(`${name} is required.`);
  if(name!=='TRACE_PLAYWRIGHT_ROOT'&&name!=='TRACE_WEBVIEW_USER_DATA'&&!fs.existsSync(value))throw new Error(`${name} is missing: ${value}`);
}
fs.mkdirSync(userData,{recursive:true});
const requireFromSource=createRequire(path.resolve(playwrightRoot,'package.json'));
const { chromium }=requireFromSource('playwright');

diagnose('smoke-start',{exe,playwrightRoot,userData,importFile,surveyFile,pdfFile,audioFile});
const failures=[];
const check=(ok,msg)=>{if(!ok)failures.push(msg)};
const wait=ms=>new Promise(r=>setTimeout(r,ms));
const webViewPolicyRoot=String.raw`HKCU\Software\Policies\Microsoft\Edge\WebView2`+'\\';
const webViewPolicyValue=path.basename(exe);
function reg(args,label,required=true){
  const result=spawnSync('reg.exe',args,{windowsHide:true,encoding:'utf8'});
  if(required&&result.status!==0)throw new Error(`${label} failed (${result.status}): ${result.stderr||result.stdout}`);
  return result;
}
function clearWebViewPolicy(){
  reg(['delete',`${webViewPolicyRoot}\AdditionalBrowserArguments`,'/v',webViewPolicyValue,'/f'],'WebView2 browser-argument policy cleanup',false);
  reg(['delete',`${webViewPolicyRoot}\UserDataFolder`,'/v',webViewPolicyValue,'/f'],'WebView2 user-data policy cleanup',false);
}
function configureWebViewPolicy(port){
  clearWebViewPolicy();
  reg(['add',`${webViewPolicyRoot}\AdditionalBrowserArguments`,'/v',webViewPolicyValue,'/t','REG_SZ','/d',`--remote-debugging-port=${port} --remote-allow-origins=*`,'/f'],'WebView2 browser-argument policy setup');
  reg(['add',`${webViewPolicyRoot}\UserDataFolder`,'/v',webViewPolicyValue,'/t','REG_SZ','/d',userData,'/f'],'WebView2 user-data policy setup');
  const browserPolicy=reg(['query',`${webViewPolicyRoot}\AdditionalBrowserArguments`,'/v',webViewPolicyValue],'WebView2 browser-argument policy verification');
  const dataPolicy=reg(['query',`${webViewPolicyRoot}\UserDataFolder`,'/v',webViewPolicyValue],'WebView2 user-data policy verification');
  diagnose('webview-policy-configured',{port,appId:webViewPolicyValue,browserPolicy:(browserPolicy.stdout||'').trim(),dataPolicy:(dataPolicy.stdout||'').trim()});
}
process.on('exit',clearWebViewPolicy);
async function launchInstalled(port){
  configureWebViewPolicy(port);
  const env={...process.env};
  delete env.WEBVIEW2_USER_DATA_FOLDER;
  delete env.WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS;
  const stdout=fs.openSync(path.join(evidenceDir,`trace-${port}-stdout.log`),'a');
  const stderr=fs.openSync(path.join(evidenceDir,`trace-${port}-stderr.log`),'a');
  const child=spawn(exe,[],{env,windowsHide:false,stdio:['ignore',stdout,stderr]});
  diagnose('process-spawned',{port,pid:child.pid});
  let browser=null,last=null,endpoint=null;
  const endpoints=[`http://127.0.0.1:${port}`,`http://localhost:${port}`];
  for(let i=0;i<120&&!browser;i++){
    if(child.exitCode!==null){clearWebViewPolicy();throw new Error(`Installed Trace exited before WebView2 became available (exit ${child.exitCode}).`)}
    for(const candidate of endpoints){
      try{
        browser=await chromium.connectOverCDP(candidate);
        endpoint=candidate;
        break;
      }catch(err){last=err}
    }
    if(!browser){
      if(i%10===0){
        let version='unavailable';
        try{const response=await fetch(`${endpoints[0]}/json/version`);version=`${response.status} ${await response.text()}`.slice(0,1200)}catch(err){version=String(err)}
        diagnose('cdp-poll',{port,attempt:i+1,processAlive:child.exitCode===null,version,lastError:String(last)});
      }
      await wait(500);
    }
  }
  if(!browser){killTree(child.pid);clearWebViewPolicy();throw new Error(`Could not attach to installed WebView2 on port ${port}: ${String(last)}`)}
  diagnose('cdp-connected',{port,endpoint});

  let page=null,fallback=null,lastTargets=[];
  const deadline=Date.now()+25000;
  while(Date.now()<deadline&&!page){
    const pages=browser.contexts().flatMap(c=>c.pages());
    lastTargets=[];
    for(const candidate of pages){
      const url=candidate.url();
      let title='';
      try{title=await candidate.title()}catch{}
      lastTargets.push({url,title});
      if(/^devtools:/i.test(url)||/^about:blank$/i.test(url))continue;
      fallback=fallback||candidate;
      try{
        if(await candidate.locator('.trace-home, .project-frame').count()){page=candidate;break}
      }catch{}
    }
    if(!page){
      const pagesNow=browser.contexts().flatMap(c=>c.pages());
      fallback=fallback||pagesNow.find(p=>!/^devtools:/i.test(p.url())&&!/^about:blank$/i.test(p.url()))||null;
      await wait(250);
    }
  }
  page=page||fallback;
  diagnose('targets-discovered',{port,targets:lastTargets,selectedUrl:page?.url?.()||null});
  if(!page){await browser.close().catch(()=>{});killTree(child.pid);clearWebViewPolicy();throw new Error(`Installed Trace exposed no usable WebView page. Targets: ${JSON.stringify(lastTargets)}`)}
  activePage=page;
  await page.waitForLoadState('domcontentloaded').catch(()=>{});
  await page.waitForSelector('body',{timeout:20000});
  diagnose('page-ready',{port,url:page.url(),title:await page.title().catch(()=>''),home:await page.locator('.trace-home').count(),project:await page.locator('.project-frame').count()});
  return {child,browser,page};
}
function killTree(pid){if(!pid)return;spawnSync('taskkill',['/PID',String(pid),'/T','/F'],{windowsHide:true,stdio:'ignore'});}
async function closeInstalled(session){try{await session.browser.close()}catch{}killTree(session.child.pid);clearWebViewPolicy();await wait(1500);activePage=null}
async function screenshot(page,name){await page.screenshot({path:path.join(evidenceDir,`${name}.png`),fullPage:false});diagnose('screenshot',{name,url:page.url()})}
async function importBinary(page,file,name){
  await page.locator('#file-import').setInputFiles(file);
  await page.waitForFunction(expected=>[...document.querySelectorAll('.import-result')].some(x=>x.textContent?.includes(expected)&&x.classList.contains('ok')),name,{timeout:30000});
}

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
const themeCodes=page.locator('[data-theme-code]');
check(await themeCodes.count()>0,'Installed theme editor exposed no code choices');
if(await themeCodes.count())await themeCodes.first().check();
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

// Exercise the other research file classes required by final acceptance: spreadsheet cases, PDF and media.
await page.click('[data-section="Data"]');
await page.locator('#file-import').setInputFiles(surveyFile);
await page.waitForSelector('#survey-import-go',{timeout:20000});
const surveyText=await page.locator('.survey-import-modal').innerText();
check(/2\s+response rows/i.test(surveyText),'Installed XLSX preview did not find two participant rows');
await page.click('#survey-import-go');
await page.waitForSelector('.survey-import-modal',{state:'detached',timeout:30000});
await page.click('[data-data-context="participants"]');
await page.waitForTimeout(300);
const participantText=await page.locator('main.workspace').innerText();
check(participantText.includes('P01')&&participantText.includes('P02'),'Installed XLSX import did not create the expected participant cases');
check(participantText.includes('Role')&&participantText.includes('Region'),'Installed XLSX import did not expose participant attributes');

await page.click('[data-data-context="sources"]');
await importBinary(page,pdfFile,'evidence.pdf');
await page.click('[data-section="Data"]');
await page.click('[data-data-context="sources"]');
await importBinary(page,audioFile,'interview-audio.wav');
await page.click('[data-section="Data"]');
await page.click('[data-data-context="sources"]');
await page.waitForTimeout(400);
const sourceText=await page.locator('main.workspace').innerText();
check(sourceText.includes('evidence.pdf'),'Installed PDF import is not visible in Data');
check(sourceText.includes('interview-audio.wav'),'Installed WAV import is not visible in Data');
check(sourceText.includes('interview.txt'),'Installed transcript disappeared after multi-format imports');
await screenshot(page,'03-installed-multiformat-data');

await page.click('#rail-home');
await page.waitForSelector('.trace-home',{timeout:10000});
check(await page.locator('#resume-current').count()>0,'Installed project is not resumable from Trace Home before restart');
await screenshot(page,'04-installed-home-after-work');
await closeInstalled(first);

// Relaunch the real installed process with the same WebView2 profile. Default behavior must still be Home,
// and the researcher must be able to resume the project without losing analytical or imported research state.
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
await page.click('[data-section="Data"]');
await page.click('[data-data-context="participants"]');
const reopenedParticipants=await page.locator('main.workspace').innerText();
check(reopenedParticipants.includes('P01')&&reopenedParticipants.includes('P02'),'Installed close/reopen lost spreadsheet participant cases');
await page.click('[data-data-context="sources"]');
const reopenedSources=await page.locator('main.workspace').innerText();
check(reopenedSources.includes('evidence.pdf')&&reopenedSources.includes('interview-audio.wav'),'Installed close/reopen lost PDF or media sources');
await page.click('[data-section="Code"]');
await screenshot(page,'05-installed-resumed-code');
await closeInstalled(second);

fs.writeFileSync(path.join(evidenceDir,'installed-smoke.json'),JSON.stringify({freshHome:true,createdProject:true,importedTranscript:true,importedSpreadsheet:true,importedPdf:true,importedAudio:true,coding:true,memo:true,theme:true,analyse:true,findings:true,closedAndReopened:true,failures},null,2));
diagnose('smoke-complete',{failures});
if(failures.length){console.error(failures.join('\n'));process.exit(1)}
console.log('Installed Trace WebView2 multi-format researcher journey: green');