from pathlib import Path

app_path=Path('src/app.js')
contract_path=Path('tests/ux_foundation_v2_contract.py')
app=app_path.read_text(encoding='utf-8')

old="document.querySelector('#saved-label')?.replaceChildren(document.createTextNode('Saved '+relativeTime(state.savedAt)));"
new="document.querySelector('#saved-label')?.replaceChildren(document.createTextNode('Saved'));"
if old in app:
    app=app.replace(old,new,1)
elif "document.createTextNode('Saved')" not in app:
    raise SystemExit('Could not locate topbar saved-state refresh anchor')

# The inspector and save-details dialog still carry temporal detail; the top bar stays low-noise.
app_path.write_text(app,encoding='utf-8')
contract=contract_path.read_text(encoding='utf-8')
assertion="assert \"document.createTextNode('Saved')\" in app\n"
if assertion not in contract:contract+='\n'+assertion
contract_path.write_text(contract,encoding='utf-8')
print('Stable topbar Saved status applied; detailed timing remains contextual')
