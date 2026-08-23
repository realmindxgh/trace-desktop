from pathlib import Path

path = Path('work/setup-shell/src-tauri/src/main.rs')
text = path.read_text(encoding='utf-8')

if '--silent-install' in text and 'fn silent_install(' in text:
    print('Trace setup silent CLI already present')
    raise SystemExit(0)

marker = '\nfn main(){\n'
if marker not in text:
    raise SystemExit('Could not locate Trace setup main() marker')

helpers = r'''
fn arg_value(args:&[String],name:&str)->Option<String>{
  args.iter().position(|a|a==name).and_then(|i|args.get(i+1)).cloned()
}

// Release verification deliberately calls the same core routines used by the
// interactive branded installer. This prevents CI from proving a parallel,
// slightly different installation path.
fn silent_install(options:InstallOptions)->Result<InstallResult,String>{
  perform_install(None,options)
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
path.write_text(text, encoding='utf-8')

check = path.read_text(encoding='utf-8')
for token in ('--silent-install','--silent-uninstall','TRACE_SETUP_SILENT_INSTALL_OK','fn silent_install(','perform_install(None','perform_uninstall(None'):
    if token not in check:
        raise SystemExit(f'Missing injected token: {token}')
print('Trace setup silent CLI injected successfully')
