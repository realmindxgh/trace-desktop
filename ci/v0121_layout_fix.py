from pathlib import Path

APP_MARKER = "/* V0121_BROWSER_GEOMETRY_FIX */"
SETUP_MARKER = "/* V0121_SETUP_DOCK_GEOMETRY_FIX */"

app_css = Path("src/styles.css")
setup_css = Path("setup-shell/src/styles.css")
layout_test = Path("tests/v0121_layout.mjs")

app = app_css.read_text(encoding="utf-8")
if APP_MARKER not in app:
    app += r'''

/* V0121_BROWSER_GEOMETRY_FIX */
/* Give primary Inspector navigation its own full-width row. The collapse
   control no longer steals width from INFO / CODES / NOTES / MEMOS. */
.inspector-top{
  display:grid!important;
  grid-template-columns:minmax(0,1fr) auto;
  grid-template-rows:34px 40px;
  gap:4px 8px!important;
  align-items:center;
}
.inspector-top::before{
  content:"INSPECTOR";
  grid-column:1;
  grid-row:1;
  align-self:center;
  font-size:12px;
  font-weight:800;
  letter-spacing:.08em;
  color:var(--muted);
}
.inspector-top .inspector-collapse{
  grid-column:2;
  grid-row:1;
  justify-self:end;
}
.inspector-top .inspector-tabs{
  grid-column:1 / -1;
  grid-row:2;
  display:grid!important;
  grid-template-columns:none!important;
  grid-auto-flow:column;
  grid-auto-columns:max-content;
  justify-content:space-between;
  align-items:center;
  width:100%;
  min-width:0;
  gap:6px!important;
  overflow:visible!important;
}
.inspector-top .inspector-tabs button{
  width:auto!important;
  min-width:max-content!important;
  padding-inline:2px!important;
  overflow:visible!important;
  text-overflow:clip!important;
}
'''
    app_css.write_text(app, encoding="utf-8")

setup = setup_css.read_text(encoding="utf-8")
if SETUP_MARKER not in setup:
    setup += r'''

/* V0121_SETUP_DOCK_GEOMETRY_FIX */
/* The setup stage and bottom controls are separate grid regions with a real
   spacer row. The inner body row is explicitly shrinkable so long setup
   content scrolls instead of expanding through the dock. */
.setup-window{
  grid-template-rows:72px minmax(0,1fr) 12px 86px!important;
}
.setup-topbar{grid-row:1!important}
.setup-body{
  grid-row:2!important;
  grid-template-rows:minmax(0,1fr)!important;
  min-height:0!important;
  height:auto!important;
  max-height:none!important;
  overflow:hidden!important;
}
.setup-rail,
.setup-stage{
  min-height:0!important;
  height:auto!important;
  max-height:none!important;
  align-self:stretch!important;
}
.setup-stage{
  overflow:auto!important;
  padding-bottom:24px!important;
}
.setup-dock{
  grid-row:4!important;
  align-self:center!important;
  justify-self:center!important;
  position:relative!important;
  left:auto!important;
  right:auto!important;
  bottom:auto!important;
  transform:none!important;
}
@media(max-height:760px){
  .setup-window{grid-template-rows:72px minmax(0,1fr) 8px 82px!important}
}
@media(max-width:760px){
  .setup-window{grid-template-rows:72px minmax(0,1fr) 8px 82px!important}
}
'''
    setup_css.write_text(setup, encoding="utf-8")

# Keep the browser gate strict, but make any future geometry failure identify
# the exact tab and measured dimensions instead of a generic message.
test = layout_test.read_text(encoding="utf-8")
old_tabs = "if(info.tabs.some(t=>t.sw>t.cw+2))errors.push(`${w}x${h}@${scale} ${section}: clipped primary tab`);"
new_tabs = "for(const t of info.tabs.filter(t=>t.sw>t.cw+2))errors.push(`${w}x${h}@${scale} ${section}: clipped primary tab ${t.t} (${t.sw}/${t.cw})`);"
if old_tabs in test:
    test = test.replace(old_tabs, new_tabs, 1)
old_setup = "if(info.dock&&info.stage&&info.stage.bottom>info.dock.top+2)errors.push(`setup ${fixtureName}: stage overlaps dock`);"
new_setup = "if(info.dock&&info.stage&&info.stage.bottom>info.dock.top+2)errors.push(`setup ${fixtureName}: stage overlaps dock (${Math.round(info.stage.bottom)}/${Math.round(info.dock.top)})`);"
if old_setup in test:
    test = test.replace(old_setup, new_setup, 1)
layout_test.write_text(test, encoding="utf-8")

print("v0.12.1 browser geometry fixes applied")
