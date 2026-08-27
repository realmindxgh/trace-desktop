from pathlib import Path

app_path=Path('src/app.js')
contract_path=Path('tests/ux_foundation_v2_contract.py')
app=app_path.read_text(encoding='utf-8')
contract=contract_path.read_text(encoding='utf-8')

old="function relativeTime(ts){ const s=Math.max(0,Math.floor((Date.now()-ts)/1000)); if(s<8)return 'just now'; if(s<60)return `${s}s ago`; const m=Math.floor(s/60); if(m<60)return `${m}m ago`; const h=Math.floor(m/60); return `${h}h ago`; }"
new="function relativeTime(ts){const value=Number(ts);if(!Number.isFinite(value)||value<=0)return 'unknown';const s=Math.max(0,Math.floor((Date.now()-value)/1000));if(s<8)return 'just now';if(s<60)return `${s}s ago`;const m=Math.floor(s/60);if(m<60)return `${m}m ago`;const h=Math.floor(m/60);if(h<24)return `${h}h ago`;const d=Math.floor(h/24);if(d<7)return `${d}d ago`;return new Date(value).toLocaleDateString(undefined,{year:'numeric',month:'short',day:'numeric'});}"
if old in app:
    app=app.replace(old,new,1)
elif "if(h<24)return `${h}h ago`" not in app:
    raise SystemExit('relativeTime formatter anchor changed')

app_path.write_text(app,encoding='utf-8')
for assertion in (
    "assert \"if(h<24)return `${h}h ago`\" in app\n",
    "assert \"toLocaleDateString\" in app\n",
    "assert \"return `${h}h ago`; }\" not in app\n",
):
    if assertion not in contract: contract+='\n'+assertion
contract_path.write_text(contract,encoding='utf-8')
print('Contextual timestamp formatter capped relative hours and uses readable dates for older activity')
