from pathlib import Path

app_path=Path('src/app.js')
test_path=Path('tests/ux_foundation_v2_contract.py')
app=app_path.read_text(encoding='utf-8')
old=r'''function renderDock(){
  const sections = [ ['Data','data'], ['Code','tag'], ['Themes','themes'], ['Analyse','analyse'], ['Write','write'] ];
  return `<nav class="dock">${sections.map(([name,ic])=>`<button class="dock-item ${state.activeSection===name?'active':''}" data-section="${name}">${icon(ic,23)}<span>${name}</span></button>`).join('')}<span class="dock-separator"></span><button class="trace-orb" id="trace-orb" title="Trace Assistant"><span>${icon('spark',20)}</span><b>Assistant</b></button></nav>`;
}

'''
if old in app:
    app=app.replace(old,'',1)
elif 'function renderDock(){' in app:
    raise SystemExit('Old dock renderer changed shape; remove it explicitly rather than guessing')
app_path.write_text(app,encoding='utf-8')

test=test_path.read_text(encoding='utf-8')
assertion="assert 'function renderDock(){' not in app\n"
if assertion not in test:
    test+='\n'+assertion
test_path.write_text(test,encoding='utf-8')

if 'function renderDock(){' in app_path.read_text(encoding='utf-8'):
    raise SystemExit('Legacy bottom-dock renderer remains')
print('Legacy competing bottom-navigation renderer removed')
