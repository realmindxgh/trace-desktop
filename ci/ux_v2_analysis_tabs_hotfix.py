from pathlib import Path

css_path = Path('src/styles.css')
test_path = Path('tests/ux_foundation_v2_contract.py')
marker = '/* UX_V2_ANALYSE_PRIMARY_TABS_FIX */'

css = css_path.read_text(encoding='utf-8')
if marker not in css:
    css += r'''

/* UX_V2_ANALYSE_PRIMARY_TABS_FIX */
/* Primary Analyse navigation must remain readable across the supported
   desktop/DPI matrix. The older flex strip allowed its buttons to shrink to
   a few pixels once min-width:0 was introduced by the v0.12.1 hardening
   layer. Use an actual grid on normal desktop widths, and deliberately wrap
   to two columns on very narrow windows instead of crushing labels. */
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

# Make the regression detectable by the static UX contract as well as the
# browser geometry gate.
test = test_path.read_text(encoding='utf-8')
assertion = "assert 'UX_V2_ANALYSE_PRIMARY_TABS_FIX' in css\n"
if assertion not in test:
    anchor = "assert 'UX_FOUNDATION_V2' in css\n"
    if anchor not in test:
        # The exact marker in the generated contract may change; append a
        # focused assertion rather than silently skipping protection.
        test += '\n' + assertion
    else:
        test = test.replace(anchor, anchor + assertion, 1)
    test_path.write_text(test, encoding='utf-8')

check = css_path.read_text(encoding='utf-8')
for required in (
    marker,
    'display:grid!important',
    'grid-template-columns:repeat(5,minmax(max-content,1fr))!important',
    'min-width:max-content!important',
):
    if required not in check:
        raise SystemExit(f'Analyse primary-tab layout contract missing: {required}')
print('Analyse primary-tab responsive layout hotfix applied')
