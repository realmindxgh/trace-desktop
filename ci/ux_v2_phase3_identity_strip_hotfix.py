from pathlib import Path
import runpy

app_path=Path('src/app.js')
css_path=Path('src/styles.css')
contract_path=Path('tests/ux_foundation_v2_contract.py')
visual_path=Path('tests/ux_foundation_visuals.mjs')

app=app_path.read_text(encoding='utf-8')
css=css_path.read_text(encoding='utf-8')
contract=contract_path.read_text(encoding='utf-8')

old_shell='<div class="shell project-shell">${renderTopbar()}${recoveryNotice?'
new_shell='<div class="shell project-shell ${currentSource()&&!recoveryNotice?\'has-workspace-identity\':\'\'}">${renderTopbar()}${recoveryNotice?'
if old_shell in app:
    app=app.replace(old_shell,new_shell,1)
elif 'has-workspace-identity' not in app:
    raise SystemExit('Could not locate project shell class anchor')

old_identity='${src?`<div class="workspace-identity"><span>${escapeHtml(state.activeSection)}</span><b>›</b><strong>${escapeHtml(src.name)}</strong></div>`:\'\'}</header>`;'
new_identity='${src&&!recoveryNotice?`<div class="workspace-identity" aria-label="Open source context"><span>${escapeHtml(state.activeSection)}</span><b>›</b><strong>${escapeHtml(src.name)}</strong></div>`:\'\'}</header>`;'
if old_identity in app:
    app=app.replace(old_identity,new_identity,1)
elif 'aria-label="Open source context"' not in app:
    raise SystemExit('Could not locate workspace identity anchor')

marker='/* UX_V2_PHASE3_SOURCE_IDENTITY_STRIP */'
if marker not in css:
    css += r'''

/* UX_V2_PHASE3_SOURCE_IDENTITY_STRIP */
.project-shell.has-workspace-identity{grid-template-rows:64px 28px minmax(0,1fr)!important}
.project-shell.has-workspace-identity>.project-frame{grid-row:3!important}
.workspace-identity{left:0!important;right:0!important;bottom:-28px!important;height:28px!important;box-sizing:border-box;padding:0 18px 0 calc(var(--trace-rail) + 16px);align-items:center;background:var(--panel2);border-bottom:1px solid var(--line);z-index:15!important;overflow:hidden}
.workspace-identity span,.workspace-identity b,.workspace-identity strong{line-height:28px}
.workspace-identity strong{display:block;min-width:0;max-width:min(520px,50vw)}
'''

app_path.write_text(app,encoding='utf-8')
css_path.write_text(css,encoding='utf-8')

for assertion in (
    "assert 'has-workspace-identity' in app\n",
    "assert 'Open source context' in app\n",
    "assert 'UX_V2_PHASE3_SOURCE_IDENTITY_STRIP' in css\n",
):
    if assertion not in contract:
        contract += '\n'+assertion
contract_path.write_text(contract,encoding='utf-8')

# The visual fixture should describe its two real transcript rows honestly.
if visual_path.exists():
    visual=visual_path.read_text(encoding='utf-8')
    visual=visual.replace("kind:'text',participantId:'p1'", "kind:'text',lines:2,participantId:'p1'", 1)

    # Record and reject any physical collision between the source identity strip and document tabs.
    old="""      codingTitles:[...document.querySelectorAll('.coding-stripes i')].map(i=>i.getAttribute('title')||i.textContent?.trim()||''),
      inspectorVisible:[...document.querySelectorAll('.inspector')].some(visible),"""
    new="""      codingTitles:[...document.querySelectorAll('.coding-stripes i')].map(i=>i.getAttribute('title')||i.textContent?.trim()||''),
      identityTabOverlap:(()=>{const a=document.querySelector('.workspace-identity'),b=document.querySelector('.document-tabs');if(!a||!b||!visible(a)||!visible(b))return 0;const x=a.getBoundingClientRect(),y=b.getBoundingClientRect();return Math.max(0,Math.min(x.bottom,y.bottom)-Math.max(x.top,y.top));})(),
      inspectorVisible:[...document.querySelectorAll('.inspector')].some(visible),"""
    if old in visual:
        visual=visual.replace(old,new,1)
    elif 'identityTabOverlap:' not in visual:
        raise SystemExit('Could not locate visual metadata anchor')

    old_check="""  if(meta.minimumVisibleFontPx>0&&meta.minimumVisibleFontPx<12)failures.push(`${name}: visible UI text fell below 12px (${meta.minimumVisibleFontPx}px)`);"""
    new_check=old_check+"\n  if(meta.identityTabOverlap>1)failures.push(`${name}: source identity overlaps document tabs by ${meta.identityTabOverlap}px`);"
    if old_check in visual and 'source identity overlaps document tabs' not in visual:
        visual=visual.replace(old_check,new_check,1)
    elif 'source identity overlaps document tabs' not in visual:
        raise SystemExit('Could not locate visual geometry assertion anchor')
    visual_path.write_text(visual,encoding='utf-8')

# Keep save timing in contextual details rather than turning the global topbar into a stale-age ticker.
runpy.run_path('../control/ci/ux_v2_phase3_save_status_hotfix.py',run_name='__main__')
# Finish the plain-language error migration after the trust helpers and consequence previews exist.
runpy.run_path('../control/ci/ux_v2_phase7_error_completion_hotfix.py',run_name='__main__')

check=app_path.read_text(encoding='utf-8')
styles=css_path.read_text(encoding='utf-8')
for required in ('has-workspace-identity','Open source context'):
    if required not in check: raise SystemExit(f'Identity strip app contract missing: {required}')
if marker not in styles: raise SystemExit('Identity strip CSS marker missing')
print('Source identity strip, document-tab overlap guard, stable Saved status and human errors applied')
