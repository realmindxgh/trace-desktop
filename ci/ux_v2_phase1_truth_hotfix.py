from pathlib import Path

app_path = Path('src/app.js')
test_path = Path('tests/ux_foundation_v2_contract.py')

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

test = test_path.read_text(encoding='utf-8')
assertion = "assert 'clone(defaults.participants).slice(0,1)' not in app\n"
if assertion not in test:
    anchor = "assert \"||`P${String(ix+1).padStart(2,'0')}`\" not in app\n"
    if anchor not in test:
        raise SystemExit('Could not locate UX participant-truth contract anchor')
    test = test.replace(anchor, anchor + assertion, 1)
test_path.write_text(test, encoding='utf-8')

check = app_path.read_text(encoding='utf-8')
if 'clone(defaults.participants).slice(0,1)' in check:
    raise SystemExit('REFI phantom participant fallback remains')
if new_active not in check:
    raise SystemExit('Imported active participant is not explicitly nullable')
print('Phase 1 participant-state truth hotfix applied')
