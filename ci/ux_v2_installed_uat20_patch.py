from pathlib import Path

# This transform strengthens the installed-app acceptance driver without altering
# the promoted Trace source artifact. It addresses two demonstrated acceptance
# gaps: asynchronous Sources hydration after restart and the old sine-wave media
# fixture that never proved preview + transcription through the installed UI.
driver_path = Path('../control/ci/ux_v2_installed_webview_smoke.mjs')
if not driver_path.exists():
    raise SystemExit(f'Installed WebView smoke driver is missing: {driver_path}')
driver = driver_path.read_text(encoding='utf-8')

fixture_anchor = """}
for(const [name,value] of Object.entries({TRACE_INSTALLED_EXE:exe,TRACE_PLAYWRIGHT_ROOT:playwrightRoot,TRACE_WEBVIEW_USER_DATA:userData,TRACE_INSTALLED_IMPORT_FILE:importFile,TRACE_INSTALLED_SURVEY_FILE:surveyFile,TRACE_INSTALLED_PDF_FILE:pdfFile,TRACE_INSTALLED_AUDIO_FILE:audioFile})){"""
fixture_replacement = r''' }
// Physical-UAT regression: use actual spoken audio, not the historical sine-wave fixture.
if(process.platform==='win32'){
  const spokenDir=path.join(evidenceDir,'fixtures');
  fs.mkdirSync(spokenDir,{recursive:true});
  const spokenAudio=path.join(spokenDir,'interview-audio.wav');
  const speechScript=`Add-Type -AssemblyName System.Speech; $voice=New-Object System.Speech.Synthesis.SpeechSynthesizer; $voice.SetOutputToWaveFile($env:TRACE_ACCEPTANCE_SPOKEN_WAV); $voice.Speak('Trace transcription works on this computer. Evidence remains connected to the research source.'); $voice.Dispose()`;
  const spoken=spawnSync('powershell.exe',['-NoProfile','-Command',speechScript],{env:{...process.env,TRACE_ACCEPTANCE_SPOKEN_WAV:spokenAudio},encoding:'utf8',windowsHide:true});
  if(spoken.status!==0||!fs.existsSync(spokenAudio)||fs.statSync(spokenAudio).size<1000)throw new Error(`Could not generate installed spoken-audio fixture: ${spoken.stderr||spoken.stdout}`);
  audioFile=spokenAudio;
  diagnose('spoken-audio-fixture',{audioFile,sizeBytes:fs.statSync(audioFile).size});
}
for(const [name,value] of Object.entries({TRACE_INSTALLED_EXE:exe,TRACE_PLAYWRIGHT_ROOT:playwrightRoot,TRACE_WEBVIEW_USER_DATA:userData,TRACE_INSTALLED_IMPORT_FILE:importFile,TRACE_INSTALLED_SURVEY_FILE:surveyFile,TRACE_INSTALLED_PDF_FILE:pdfFile,TRACE_INSTALLED_AUDIO_FILE:audioFile})){'''.lstrip()
if 'spoken-audio-fixture' not in driver:
    if fixture_anchor not in driver:
        raise SystemExit('Installed driver fixture anchor changed')
    driver = driver.replace(fixture_anchor, fixture_replacement, 1)

media_anchor = """await importBinary(page,audioFile,'interview-audio.wav');
await page.click('[data-section=\"Data\"]');
await page.click('[data-data-context=\"sources\"]');
await page.waitForTimeout(400);"""
media_replacement = """await importBinary(page,audioFile,'interview-audio.wav');
// Opening the real installed audio source must exercise the repaired load_source_media boundary.
const installedAudioCard=page.locator('.source-card').filter({hasText:'interview-audio.wav'}).first();
check(await installedAudioCard.count()>0,'Installed spoken audio source is missing before preview verification');
if(await installedAudioCard.count())await installedAudioCard.click();
await page.waitForSelector('#media-player',{timeout:30000});
check(await page.locator('#media-player').count()>0,'Installed media preview did not open the spoken audio source');
await page.waitForSelector('#transcribe-source',{timeout:30000});
await page.waitForFunction(()=>{const b=document.querySelector('#transcribe-source');return !!b&&!b.disabled},null,{timeout:30000});
await page.click('#transcribe-source');
await page.waitForFunction(()=>document.querySelectorAll('.media-transcript-pane .transcript-line p').length>0,null,{timeout:180000});
const installedAudioTranscript=await page.locator('.media-transcript-pane').innerText();
check(installedAudioTranscript.trim().split(/\\s+/).length>=4,'Installed Whisper transcription returned implausibly little text');
check(/trace|transcription|research/i.test(installedAudioTranscript),'Installed Whisper transcription did not resemble the spoken research fixture');
await screenshot(page,'03a-installed-audio-transcribed');
await page.click('[data-section=\"Data\"]');
await page.click('[data-data-context=\"sources\"]');
await page.waitForTimeout(400);"""
if '03a-installed-audio-transcribed' not in driver:
    if media_anchor not in driver:
        raise SystemExit('Installed driver media-import anchor changed')
    driver = driver.replace(media_anchor, media_replacement, 1)

reopen_anchor = """await page.click('[data-data-context=\"sources\"]');
const reopenedSources=await page.locator('main.workspace').innerText();
check(reopenedSources.includes('evidence.pdf')&&reopenedSources.includes('interview-audio.wav'),'Installed close/reopen lost PDF or media sources');
await page.click('[data-section=\"Code\"]');"""
reopen_replacement = """await page.click('[data-data-context=\"sources\"]');
// Source hydration is asynchronous after switching from Participants. Wait for the durable cards
// rather than sampling main.workspace during the render boundary.
await waitForImportedSource(page,'evidence.pdf');
await waitForImportedSource(page,'interview-audio.wav');
const reopenedSources=await page.locator('main.workspace').innerText();
check(reopenedSources.includes('evidence.pdf')&&reopenedSources.includes('interview-audio.wav'),'Installed close/reopen lost PDF or media sources');
const reopenedAudio=page.locator('.source-card').filter({hasText:'interview-audio.wav'}).first();
if(await reopenedAudio.count())await reopenedAudio.click();
await page.waitForSelector('.media-transcript-pane .transcript-line p',{timeout:30000});
const reopenedAudioTranscript=await page.locator('.media-transcript-pane').innerText();
check(reopenedAudioTranscript.trim().split(/\\s+/).length>=4,'Installed close/reopen lost the generated audio transcript');
await page.click('[data-section=\"Code\"]');"""
if 'Source hydration is asynchronous after switching from Participants' not in driver:
    if reopen_anchor not in driver:
        raise SystemExit('Installed driver reopen-source anchor changed')
    driver = driver.replace(reopen_anchor, reopen_replacement, 1)

json_anchor = """JSON.stringify({freshHome:true,createdProject:true,importedTranscript:true,importedSpreadsheet:true,importedPdf:true,importedAudio:true,coding:true,memo:true,theme:true,analyse:true,findings:true,closedAndReopened:true,failures},null,2)"""
json_replacement = """JSON.stringify({freshHome:true,createdProject:true,importedTranscript:true,importedSpreadsheet:true,importedPdf:true,importedAudio:true,mediaPreview:true,transcription:true,transcriptionPersisted:true,coding:true,memo:true,theme:true,analyse:true,findings:true,closedAndReopened:true,failures},null,2)"""
if 'transcriptionPersisted:true' not in driver:
    if json_anchor not in driver:
        raise SystemExit('Installed driver result-record anchor changed')
    driver = driver.replace(json_anchor, json_replacement, 1)

driver_path.write_text(driver, encoding='utf-8')
patched = driver_path.read_text(encoding='utf-8')
for token in ('spoken-audio-fixture','#media-player','#transcribe-source','03a-installed-audio-transcribed','Source hydration is asynchronous after switching from Participants','transcriptionPersisted:true'):
    if token not in patched:
        raise SystemExit(f'Installed physical-UAT driver patch missing token: {token}')
print('Installed WebView physical-UAT media/transcription regression injected successfully')
