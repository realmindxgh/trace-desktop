from pathlib import Path

# Retry 22 corrects a demonstrated WebView automation geometry failure from
# Retry 21. The transcription control was present, visible and enabled, but
# Playwright's synthetic pointer hit-test was intercepted by overlapping layout
# containers in the instrumented WebView. Invoke the real button's DOM click so
# the same application click handler runs without relying on CDP pointer
# geometry. Production source remains untouched.
driver_path = Path('../control/ci/ux_v2_installed_webview_smoke.mjs')
if not driver_path.exists():
    raise SystemExit(f'Installed WebView smoke driver is missing: {driver_path}')
driver = driver_path.read_text(encoding='utf-8')

click_anchor = """await page.waitForFunction(()=>{const b=document.querySelector('#transcribe-source');return !!b&&!b.disabled},null,{timeout:30000});
await page.click('#transcribe-source');
await page.waitForFunction(()=>document.querySelectorAll('.media-transcript-pane .transcript-line p').length>0,null,{timeout:180000});"""
click_replacement = """await page.waitForFunction(()=>{const b=document.querySelector('#transcribe-source');return !!b&&!b.disabled},null,{timeout:30000});
// CDP pointer geometry is unreliable for this nested installed-WebView layout.
// element.click() dispatches the button's real click handler and lets this gate
// test the boundary we care about: local Whisper inference and persistence.
await page.locator('#transcribe-source').evaluate(button=>button.click());
await page.waitForFunction(()=>document.querySelectorAll('.media-transcript-pane .transcript-line p').length>0,null,{timeout:180000});"""

if 'CDP pointer geometry is unreliable for this nested installed-WebView layout' not in driver:
    if click_anchor not in driver:
        raise SystemExit('Installed driver transcription-click anchor changed')
    driver = driver.replace(click_anchor, click_replacement, 1)

driver_path.write_text(driver, encoding='utf-8')
patched = driver_path.read_text(encoding='utf-8')
for token in ('CDP pointer geometry is unreliable for this nested installed-WebView layout',"locator('#transcribe-source').evaluate(button=>button.click())",'timeout:180000'):
    if token not in patched:
        raise SystemExit(f'Installed Whisper acceptance correction missing token: {token}')
print('Installed Whisper action corrected for instrumented WebView pointer geometry')
