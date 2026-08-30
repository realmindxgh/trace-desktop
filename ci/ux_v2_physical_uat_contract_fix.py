from pathlib import Path

styles_path=Path('src/styles.css')
transcription_path=Path('src-tauri/src/transcription.rs')

styles=styles_path.read_text(encoding='utf-8')
old='.default-model-actions .model-status{display:block;max-width:100%;font-size:11px;line-height:1.4;color:var(--muted);overflow-wrap:anywhere}'
new='.default-model-actions .model-status{display:block;max-width:100%;font-size:12px;line-height:1.4;color:var(--muted);overflow-wrap:anywhere}'
if old in styles:
    styles=styles.replace(old,new,1)
elif new not in styles:
    raise SystemExit('Physical-UAT model-status typography anchor changed')
styles_path.write_text(styles,encoding='utf-8')

# Normalize the generated CI-only Rust assertion if an escaped-space spelling survived generation.
transcription=transcription_path.read_text(encoding='utf-8')
transcription=transcription.replace('.join(" \\ ")','.join(" ")')
transcription_path.write_text(transcription,encoding='utf-8')

print('Applied physical-UAT carried-contract fix.')
