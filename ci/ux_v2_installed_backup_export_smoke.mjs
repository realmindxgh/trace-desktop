import { createRequire } from 'node:module';
import { spawn, spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const exe=process.env.TRACE_INSTALLED_EXE;
const playwrightRoot=process.env.TRACE_PLAYWRIGHT_ROOT;
const userData=process.env.TRACE_WEBVIEW_USER_DATA;
const evidenceDir=process.env.TRACE_INSTALLED_EVIDENCE_DIR||path.resolve('installed-ux-evidence');
if(!exe||!fs.existsSync(exe))throw new Error(`TRACE_INSTALLED_EXE is missing: ${exe||'<unset>'}`);
if(!playwrightRoot)throw new Error('TRACE_PLAYWRIGHT_ROOT is required.');
if(!userData)throw new Error('TRACE_WEBVIEW_USER_DATA is required.');
fs.mkdirSync(evidenceDir,{recursive:true});
const requireFromSource=createRequire(path.resolve(playwrightRoot,'package.json'));
const { chromium }=requireFromSource('playwright');
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
}
process.on('exit',clearWebViewPolicy);
function killTree(pid){if(!pid)return;spawnSync('taskkill',['/PID',String(pid),'/T','/F'],{windowsHide:true,stdio:'ignore'});}
async function launchInstalled(port){
  configureWebViewPolicy(port);
  const env={...process.env};
  env.WEBVIEW2_USER_DATA_FOLDER=userData;
  env.WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS=`--remote-debugging-port=${port} --remote-allow-origins=*`;
  const child=spawn(exe,[],{env,windowsHide:false,stdio:'ignore'});
  let browser=null,last=null;
  for(let i=0;i<90;i++){
    if(child.exitCode!==null){clearWebViewPolicy();throw new Error(`Installed Trace exited before WebView2 became available (exit ${child.exitCode}).`)}
    try{browser=await chromium.connectOverCDP(`http://127.0.0.1:${port}`);break}catch(err){last=err;await wait(500)}
  }
  if(!browser){killTree(child.pid);clearWebViewPolicy();throw new Error(`Could not attach to installed WebView2: ${String(last)}`)}
  let page=browser.contexts().flatMap(c=>c.pages()).find(p=>!/^devtools:/i.test(p.url()));
  if(!page){await wait(500);page=browser.contexts().flatMap(c=>c.pages())[0]}
  if(!page){await browser.close().catch(()=>{});killTree(child.pid);clearWebViewPolicy();throw new Error('Installed Trace exposed no WebView page.')}
  await page.waitForSelector('body',{timeout:20000});
  return {child,browser,page};
}
async function closeInstalled(session){try{await session.browser.close()}catch{}killTree(session.child.pid);clearWebViewPolicy();await wait(1200)}

const session=await launchInstalled(9333);
const page=session.page;
await page.waitForSelector('.trace-home',{timeout:20000});
const resumeCurrent=page.locator('#resume-current');
const recentProject=page.locator('[data-home-project]').filter({hasText:'Installed UX journey'}).first();
const hasResume=await resumeCurrent.count()>0;
check(hasResume||await recentProject.count()>0,'Export/recovery acceptance could not find the persisted installed project');
if(hasResume)await resumeCurrent.click();
else await recentProject.click();
await page.waitForSelector('.project-frame',{timeout:20000});

// Export the saved findings from the actual installed WebView and verify the downloaded file contents.
await page.click('[data-section="Write"]');
await page.waitForSelector('#findings-body',{timeout:10000});
const findings=await page.locator('#findings-body').inputValue();
check(findings.includes('Participants described initial access barriers'),'Installed export/recovery project has no expected findings text');
let downloaded=null;
try{
  const downloadPromise=page.waitForEvent('download',{timeout:15000});
  await page.locator('#export-findings').first().click();
  const download=await downloadPromise;
  downloaded=path.join(evidenceDir,'installed-findings-export.md');
  await download.saveAs(downloaded);
  const exported=fs.readFileSync(downloaded,'utf8');
  check(exported.includes('# Installed UX journey'),'Exported findings Markdown does not identify the installed project');
  check(exported.includes('Participants described initial access barriers'),'Exported findings Markdown lost the saved findings text');
}catch(err){
  failures.push(`Installed findings export did not produce a verifiable download: ${String(err)}`);
}

// Create a verified native backup from the populated real project.
await page.click('[data-section="Data"]');
if(await page.locator('[data-data-context="sources"]').count())await page.click('[data-data-context="sources"]');
await page.waitForSelector('#create-backup',{timeout:10000});
await page.click('#create-backup');
await page.waitForSelector('[data-restore-backup]',{timeout:30000});
check(await page.locator('[data-restore-backup]').count()>0,'Installed Back up now did not expose a verified recovery point');
await page.screenshot({path:path.join(evidenceDir,'06-installed-verified-backup.png'),fullPage:false});

// Restore that backup as a new Trace project. The current project must remain safe while the restored
// copy carries forward all research relationships and imported material.
await page.locator('[data-restore-backup]').first().click();
await page.waitForSelector('#confirm-go',{timeout:10000});
const confirmCopy=await page.locator('.confirmation-modal').innerText();
check(/current project will stay unchanged/i.test(confirmCopy),'Backup restore confirmation does not explain that the current project stays unchanged');
await page.click('#confirm-go');
await page.waitForSelector('.project-frame',{timeout:30000});
await page.waitForTimeout(600);

await page.click('[data-section="Themes"]');
check(await page.getByText('Support pathways',{exact:true}).count()>0,'Restored backup lost the saved theme');
await page.click('[data-section="Write"]');
check((await page.locator('#findings-body').inputValue().catch(()=>''))===findings,'Restored backup lost the saved findings');
// Restores can reopen on the last PDF/audio source. Reopen the transcript before verifying text coding stripes.
await page.click('[data-section="Data"]');
if(await page.locator('[data-data-context="sources"]').count())await page.click('[data-data-context="sources"]');
const restoredTranscript=page.locator('.source-card').filter({hasText:/interview\.txt/i}).first();
check(await restoredTranscript.count()>0,'Restored backup lost the transcript source needed to verify coding');
if(await restoredTranscript.count())await restoredTranscript.click();
await page.waitForSelector('.coding-stripes i[title="Access barriers"]',{timeout:20000});
check(await page.locator('.coding-stripes i[title="Access barriers"]').count()>0,'Restored backup lost the applied coding');
await page.click('[data-section="Data"]');
await page.click('[data-data-context="participants"]');
const participants=await page.locator('main.workspace').innerText();
check(participants.includes('P01')&&participants.includes('P02'),'Restored backup lost spreadsheet participant cases');
check(participants.includes('Role')&&participants.includes('Region'),'Restored backup lost participant attributes');
await page.click('[data-data-context="sources"]');
const sources=await page.locator('main.workspace').innerText();
check(sources.includes('interview.txt'),'Restored backup lost the transcript source');
check(sources.includes('evidence.pdf'),'Restored backup lost the PDF source');
check(sources.includes('interview-audio.wav'),'Restored backup lost the audio source');
await page.screenshot({path:path.join(evidenceDir,'07-installed-restored-backup.png'),fullPage:false});

fs.writeFileSync(path.join(evidenceDir,'installed-export-recovery.json'),JSON.stringify({findingsExported:!!downloaded,verifiedBackupCreated:true,backupRestoredAsNewProject:true,restoredCoding:true,restoredTheme:true,restoredFindings:true,restoredParticipants:true,restoredPdf:true,restoredAudio:true,failures},null,2));
await closeInstalled(session);
if(failures.length){console.error(failures.join('\n'));process.exit(1)}
console.log('Installed Trace findings export + verified backup recovery journey: green');