from pathlib import Path

app_path = Path('src/app.js')
css_path = Path('src/styles.css')
test_path = Path('tests/ux_foundation_v2_contract.py')

# Phase 1 state truth: REFI-QDA imports with zero participants must remain
# genuinely empty instead of inheriting the demo/default participant.
app = app_path.read_text(encoding='utf-8')
phantom = "  if(!imported.participants.length)imported.participants=clone(defaults.participants).slice(0,1);\n"
if phantom in app:
    if app.count(phantom) != 1:
        raise SystemExit(f'Expected one REFI phantom-participant fallback, found {app.count(phantom)}')
    app = app.replace(phantom, '', 1)

old_active = "imported.activeParticipant=pp?.id||imported.participants[0]?.id;"
new_active = "imported.activeParticipant=pp?.id||imported.participants[0]?.id||null;"
if old_active in app:
    if app.count(old_active) != 1:
        raise SystemExit(f'Expected one imported active-participant fallback, found {app.count(old_active)}')
    app = app.replace(old_active, new_active, 1)
elif new_active not in app:
    raise SystemExit('Could not locate imported active-participant state')

app_path.write_text(app, encoding='utf-8')

# Phase 3 responsive truth: the v0.12.1 hardening layer gave Analyse buttons
# min-width:0 while their container was still flex. That let every primary tab
# collapse to roughly 24 px. Make the navigation a real responsive grid rather
# than weakening the browser/DPI assertion.
marker = '/* UX_V2_ANALYSE_PRIMARY_TABS_FIX */'
css = css_path.read_text(encoding='utf-8')
if marker not in css:
    css += r'''

/* UX_V2_ANALYSE_PRIMARY_TABS_FIX */
.analysis-tabs{
  display:grid!important;
  width:100%!important;
  max-width:100%!important;
  grid-template-columns:repeat(5,minmax(max-content,1fr))!important;
  gap:6px!important;
  overflow:visible!important;
}
.analysis-tabs button{
  width:auto!important;
  min-width:max-content!important;
  overflow:visible!important;
  text-overflow:clip!important;
}
@media(max-width:760px){
  .analysis-tabs{
    grid-template-columns:repeat(2,minmax(0,1fr))!important;
  }
  .analysis-tabs button{
    min-width:0!important;
    white-space:normal!important;
  }
}
'''
    css_path.write_text(css, encoding='utf-8')

# Strengthen the generated static contract for both regressions.
test = test_path.read_text(encoding='utf-8')
participant_assertion = "assert 'clone(defaults.participants).slice(0,1)' not in app\n"
if participant_assertion not in test:
    anchor = "assert \"||`P${String(ix+1).padStart(2,'0')}`\" not in app\n"
    if anchor not in test:
        raise SystemExit('Could not locate UX participant-truth contract anchor')
    test = test.replace(anchor, anchor + participant_assertion, 1)

analysis_assertion = "assert 'UX_V2_ANALYSE_PRIMARY_TABS_FIX' in css\n"
if analysis_assertion not in test:
    # Appending is deliberate: this generated contract already defines `css`,
    # and a focused terminal assertion is less brittle than relying on a
    # particular earlier marker line.
    test += '\n' + analysis_assertion

test_path.write_text(test, encoding='utf-8')

check = app_path.read_text(encoding='utf-8')
if 'clone(defaults.participants).slice(0,1)' in check:
    raise SystemExit('REFI phantom participant fallback remains')
if new_active not in check:
    raise SystemExit('Imported active participant is not explicitly nullable')

css_check = css_path.read_text(encoding='utf-8')
for required in (
    marker,
    'display:grid!important',
    'grid-template-columns:repeat(5,minmax(max-content,1fr))!important',
    'min-width:max-content!important',
):
    if required not in css_check:
        raise SystemExit(f'Analyse primary-tab layout contract missing: {required}')

print('Phase 1 state truth and Analyse primary-tab responsive hotfixes applied')
