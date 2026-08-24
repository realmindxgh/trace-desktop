from pathlib import Path

path = Path("setup-shell/src-tauri/src/main.rs")
text = path.read_text(encoding="utf-8")

# Repair the generated setup-state probe syntax.
bad = "let has_exe=existing_exe.exists(),has_uninstaller=uninstaller.is_some();"
good = "let has_exe=existing_exe.exists();let has_uninstaller=uninstaller.is_some();"

if bad in text:
    if text.count(bad) != 1:
        raise SystemExit(f"Expected one generated multi-let syntax defect, found {text.count(bad)}")
    text = text.replace(bad, good, 1)
elif good not in text:
    raise SystemExit("Could not locate generated setup state probe to repair")

# NSIS requires /D=<install-dir> to be the final raw, unquoted command-line tail.
# std::process::Command::arg() correctly quotes Windows arguments containing spaces,
# but those quotes are incompatible with NSIS /D parsing. Use CommandExt::raw_arg on
# Windows while retaining the normal argument path as a non-Windows compile fallback.
windows_import = "#[cfg(windows)]\nuse std::os::windows::process::CommandExt;\n"
if windows_import not in text:
    import_anchor = "use std::{env,fs,io::Write,path::{Path,PathBuf},process::Command,sync::atomic::{AtomicBool,Ordering},thread,time::Duration};\n"
    if text.count(import_anchor) != 1:
        raise SystemExit(f"Expected one std import anchor, found {text.count(import_anchor)}")
    text = text.replace(import_anchor, import_anchor + windows_import, 1)

quoted_nsis = '  cmd.arg(format!("/D={target}"));'
raw_nsis = '''  #[cfg(windows)]
  cmd.raw_arg(format!("/D={target}"));
  #[cfg(not(windows))]
  cmd.arg(format!("/D={target}"));'''

if raw_nsis not in text:
    if text.count(quoted_nsis) != 1:
        raise SystemExit(f"Expected one generated NSIS /D launch, found {text.count(quoted_nsis)}")
    text = text.replace(quoted_nsis, raw_nsis, 1)

path.write_text(text, encoding="utf-8")

check = path.read_text(encoding="utf-8")
if bad in check:
    raise SystemExit("Generated invalid Rust multi-let syntax remains")
if good not in check:
    raise SystemExit("Generated setup state probe repair was not written")
if windows_import not in check:
    raise SystemExit("Windows CommandExt import for raw NSIS /D argument was not written")
if raw_nsis not in check:
    raise SystemExit("Raw Windows NSIS /D launch was not written")
# Exactly one ordinary .arg(/D=...) is expected: the cfg(not(windows)) fallback.
if check.count(quoted_nsis) != 1:
    raise SystemExit(f"Unexpected ordinary NSIS /D launch count after hardening: {check.count(quoted_nsis)}")
print("v0.12.1 generated setup Rust syntax and NSIS custom-path handling repaired")
