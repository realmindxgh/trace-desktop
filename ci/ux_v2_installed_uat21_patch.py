from pathlib import Path

# Retry 21 corrects a demonstrated acceptance-driver mistake from Retry 20.
# Trace intentionally keeps the raw HTML audio element hidden behind its
# evidence workspace, so media-preview acceptance must verify that the element
# is attached and contains the decoded WAV payload rather than requiring CSS
# visibility. Production source remains untouched.
driver_path = Path('../control/ci/ux_v2_installed_webview_smoke.mjs')
if not driver_path.exists():
    raise SystemExit(f'Installed WebView smoke driver is missing: {driver_path}')
driver = driver_path.read_text(encoding='utf-8')

preview_anchor = """await page.waitForSelector('#media-player',{timeout:30000});
check(await page.locator('#media-player').count()>0,'Installed media preview did not open the spoken audio source');"""
preview_replacement = """await page.waitForSelector('#media-player',{state:'attached',timeout:30000});
const installedMediaSrc=await page.locator('#media-player').getAttribute('src').catch(()=>null);
check(/^data:audio\\/wav;base64,/i.test(installedMediaSrc||''),'Installed media preview did not expose decoded WAV data');
check((installedMediaSrc||'').length>10000,'Installed media preview returned implausibly little WAV data');"""
if 'installedMediaSrc' not in driver:
    if preview_anchor not in driver:
        raise SystemExit('Installed driver preview assertion anchor changed')
    driver = driver.replace(preview_anchor, preview_replacement, 1)

reopen_anchor = """const reopenedAudio=page.locator('.source-card').filter({hasText:'interview-audio.wav'}).first();
if(await reopenedAudio.count())await reopenedAudio.click();
await page.waitForSelector('.media-transcript-pane .transcript-line p',{timeout:30000});"""
reopen_replacement = """const reopenedAudio=page.locator('.source-card').filter({hasText:'interview-audio.wav'}).first();
if(await reopenedAudio.count())await reopenedAudio.click();
await page.waitForSelector('#media-player',{state:'attached',timeout:30000});
const reopenedMediaSrc=await page.locator('#media-player').getAttribute('src').catch(()=>null);
check(/^data:audio\\/wav;base64,/i.test(reopenedMediaSrc||''),'Installed close/reopen lost decoded WAV preview data');
await page.waitForSelector('.media-transcript-pane .transcript-line p',{timeout:30000});"""
if 'reopenedMediaSrc' not in driver:
    if reopen_anchor not in driver:
        raise SystemExit('Installed driver reopened-media assertion anchor changed')
    driver = driver.replace(reopen_anchor, reopen_replacement, 1)

driver_path.write_text(driver, encoding='utf-8')
patched = driver_path.read_text(encoding='utf-8')
for token in ("state:'attached'",'installedMediaSrc','reopenedMediaSrc','decoded WAV data'):
    if token not in patched:
        raise SystemExit(f'Installed media acceptance correction missing token: {token}')
print('Installed media acceptance corrected for hidden raw audio element')
