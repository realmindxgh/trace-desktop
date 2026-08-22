from pathlib import Path
import base64
import hashlib
import lzma
import subprocess
import tempfile

ROOT = Path.cwd()
CONTROL = (ROOT / '..' / 'control').resolve()
MAIN_RS = ROOT / 'work/setup-shell/src-tauri/src/main.rs'
APP_JS = ROOT / 'work/setup-shell/src/app.js'


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def decode_overlay(part_dir: Path, expected_parts: int, expected_b64_len: int, expected_xz_sha: str, expected_patch_sha: str) -> bytes:
    parts = sorted(part_dir.glob('part*'))
    if len(parts) != expected_parts:
        raise SystemExit(f'Overlay part count mismatch for {part_dir}: expected {expected_parts}, found {len(parts)}')
    b64 = ''.join(p.read_text(encoding='utf-8') for p in parts)
    if len(b64) != expected_b64_len:
        raise SystemExit(f'Overlay base64 length mismatch for {part_dir}: {len(b64)}')
    compressed = base64.b64decode(b64)
    actual_xz = sha256(compressed)
    if actual_xz != expected_xz_sha:
        raise SystemExit(f'Overlay xz SHA-256 mismatch for {part_dir}: {actual_xz}')
    patch = lzma.decompress(compressed)
    actual_patch = sha256(patch)
    if actual_patch != expected_patch_sha:
        raise SystemExit(f'Overlay patch SHA-256 mismatch for {part_dir}: {actual_patch}')
    return patch


def git_apply_to_work(patch: bytes, label: str) -> None:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.patch') as handle:
        handle.write(patch)
        patch_path = Path(handle.name)
    try:
        subprocess.run(['git', 'apply', '--check', '--directory=work', str(patch_path)], cwd=ROOT, check=True)
        subprocess.run(['git', 'apply', '--directory=work', str(patch_path)], cwd=ROOT, check=True)
    except subprocess.CalledProcessError as exc:
        raise SystemExit(f'Could not apply {label} from reconstructed repository root: {exc.returncode}') from exc
    finally:
        patch_path.unlink(missing_ok=True)


text = MAIN_RS.read_text(encoding='utf-8')
app = APP_JS.read_text(encoding='utf-8')

# A git apply launched from source/work inside a real source checkout can return
# success while ignoring paths outside that Git subdirectory prefix. Detect that
# condition and apply the exact checksum-pinned overlays from the repository root.
if 'fn perform_install(' not in text or "bridge.invoke('setup_version')" not in app:
    print('Installer v2 repair was not present after workflow overlay step; reapplying from reconstructed repository root.')
    main_patch = decode_overlay(
        CONTROL / 'bootstrap/v011installer2',
        4,
        20512,
        '572c0d31f73db60600a1e374e5f821812d2bd417853ce30832e718a061042307',
        '7eaba8d93c223f048a658821e35a8e0cd0634997872237a79e198e9e3d27383b',
    )
    git_apply_to_work(main_patch, 'installer v2 repair overlay')
    text = MAIN_RS.read_text(encoding='utf-8')
    app = APP_JS.read_text(encoding='utf-8')

if "document.querySelector('#next')?.click()" not in app:
    print('Real primary-button GUI gate overlay was not present; reapplying from reconstructed repository root.')
    click_patch = decode_overlay(
        CONTROL / 'bootstrap/v011installer2click',
        1,
        536,
        '3b3da6f386bd33876aab699b09d790b69508a708ce95260d3ec021d6db4d7021',
        '2e24789d17ed519e1184af25e07039434be2c3d4f1cff699730bc7e375b01a5c',
    )
    git_apply_to_work(click_patch, 'real primary-button GUI gate overlay')
    app = APP_JS.read_text(encoding='utf-8')

# Rust Serialize responses normally expose snake_case field names, while Tauri
# command parameter names at the JS invoke boundary are camelCase. Preserve the
# CI-requested directory across both sides of that boundary. The nested
# InstallOptions object is Serde data, so its `install_dir` field remains
# snake_case by design.
old_handoff = "if(ci?.install_dir){state.ciGui=true;state.installDir=ci.install_dir;state.shortcuts=false;state.launch=false}"
new_handoff = "const ciInstallDir=ci?.install_dir||ci?.installDir;if(ciInstallDir){state.ciGui=true;state.installDir=ciInstallDir;state.shortcuts=false;state.launch=false}"
if old_handoff in app:
    app = app.replace(old_handoff, new_handoff, 1)
    print('Normalized installer v2 CI request response install-directory key.')
elif new_handoff not in app:
    raise SystemExit('Could not locate installer v2 CI GUI request install-directory handoff.')

boundary_replacements = {
    "bridge.invoke('setup_preflight',{install_dir:state.installDir||null})": "bridge.invoke('setup_preflight',{installDir:state.installDir||null})",
    "bridge.invoke('uninstall_trace',{install_dir:state.installDir||null})": "bridge.invoke('uninstall_trace',{installDir:state.installDir||null})",
    "bridge.invoke('launch_trace',{install_dir:state.installDir||null})": "bridge.invoke('launch_trace',{installDir:state.installDir||null})",
}
for old, new in boundary_replacements.items():
    if old in app:
        app = app.replace(old, new)
        print(f'Normalized Tauri invoke parameter: {old.split("(")[0]}')
    elif new not in app:
        raise SystemExit(f'Could not locate expected Tauri invoke boundary: {old}')
APP_JS.write_text(app, encoding='utf-8')

text = MAIN_RS.read_text(encoding='utf-8')

if '--silent-install' in text and 'fn silent_install(' in text:
    print('Trace setup v2 silent CLI already present')
    raise SystemExit(0)

for token in ('fn perform_install(', 'fn perform_uninstall(', 'fn setup_version()', 'fn ci_gui_request()'):
    if token not in text:
        raise SystemExit(f'Installer v2 shared implementation missing before CLI injection: {token}')

# The shared Rust install core must itself verify the selected target, so neither
# the GUI nor the silent verification path can report success merely because the
# embedded NSIS process returned exit code zero.
for token in ('Command::new(&payload).arg("/S").arg(format!("/D={target}"))', 'PathBuf::from(&target).join("Trace.exe")', 'if !exe.exists(){return Err('):
    if token not in text:
        raise SystemExit(f'Installer v2 target-verification invariant missing: {token}')

marker = '\nfn main(){\n'
if marker not in text:
    raise SystemExit('Could not locate Trace setup main() marker')

helpers = r'''
fn arg_value(args:&[String],name:&str)->Option<String>{
  args.iter().position(|a|a==name).and_then(|i|args.get(i+1)).cloned()
}

fn silent_install(options:InstallOptions)->Result<InstallResult,String>{
  let launch_after=options.launch_after;
  let result=perform_install(None,options)?;
  if launch_after{
    let exe=PathBuf::from(&result.install_dir).join("Trace.exe");
    Command::new(&exe).spawn().map_err(|e|format!("Trace installed but could not be launched: {e}"))?;
  }
  Ok(result)
}

fn silent_uninstall(install_dir:Option<String>)->Result<UninstallResult,String>{
  perform_uninstall(None,install_dir)
}
'''

main_prefix = r'''fn main(){
  let args:Vec<String>=env::args().skip(1).collect();
  if args.iter().any(|a|a=="--silent-install"){
    let options=InstallOptions{
      install_dir:arg_value(&args,"--install-dir"),
      create_shortcuts:args.iter().any(|a|a=="--create-shortcut"),
      launch_after:args.iter().any(|a|a=="--launch-after"),
    };
    match silent_install(options){
      Ok(result)=>{println!("TRACE_SETUP_SILENT_INSTALL_OK={}",result.install_dir);return;},
      Err(error)=>{eprintln!("TRACE_SETUP_SILENT_INSTALL_ERROR={error}");std::process::exit(1);}
    }
  }
  if args.iter().any(|a|a=="--silent-uninstall"){
    match silent_uninstall(arg_value(&args,"--install-dir")){
      Ok(result)=>{println!("TRACE_SETUP_SILENT_UNINSTALL_OK={}",result.install_dir);return;},
      Err(error)=>{eprintln!("TRACE_SETUP_SILENT_UNINSTALL_ERROR={error}");std::process::exit(1);}
    }
  }
'''

text = text.replace(marker, '\n' + helpers + '\n' + main_prefix, 1)
MAIN_RS.write_text(text, encoding='utf-8')

check = MAIN_RS.read_text(encoding='utf-8')
for token in ('--silent-install','--silent-uninstall','TRACE_SETUP_SILENT_INSTALL_OK','fn silent_install(','perform_install(None','perform_uninstall(None'):
    if token not in check:
        raise SystemExit(f'Missing injected v2 token: {token}')
print('Trace setup v2 silent CLI injected successfully')
