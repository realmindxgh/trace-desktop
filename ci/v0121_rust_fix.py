from pathlib import Path

path = Path("setup-shell/src-tauri/src/main.rs")
text = path.read_text(encoding="utf-8")

bad = "let has_exe=existing_exe.exists(),has_uninstaller=uninstaller.is_some();"
good = "let has_exe=existing_exe.exists();let has_uninstaller=uninstaller.is_some();"

if bad in text:
    if text.count(bad) != 1:
        raise SystemExit(f"Expected one generated multi-let syntax defect, found {text.count(bad)}")
    text = text.replace(bad, good, 1)
elif good not in text:
    raise SystemExit("Could not locate generated setup state probe to repair")

path.write_text(text, encoding="utf-8")

check = path.read_text(encoding="utf-8")
if bad in check:
    raise SystemExit("Generated invalid Rust multi-let syntax remains")
if good not in check:
    raise SystemExit("Generated setup state probe repair was not written")
print("v0.12.1 generated setup Rust syntax repaired")
