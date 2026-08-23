$ErrorActionPreference='Stop'
$control=(Resolve-Path '.').Path
$source=Join-Path $control 'source'
if(Test-Path $source){Remove-Item $source -Recurse -Force}

git clone --quiet https://github.com/realmindxgh/trace-desktop.git $source
if($LASTEXITCODE -ne 0){throw 'Could not clone Trace source repository.'}
git -C $source checkout --quiet eebc47e418003811a0cb27e1b684601a5c77bdcf
if($LASTEXITCODE -ne 0){throw 'Could not checkout proven v0.11 checkpoint.'}

Copy-Item bootstrap/v011transcribe/part00 "$source/bootstrap/v011transcribe/part00" -Force
Copy-Item bootstrap/v011transcribe/part01 "$source/bootstrap/v011transcribe/part01" -Force
$wf=Join-Path $source '.github/workflows/v011-transcription-check.yml'
$text=Get-Content $wf -Raw
$text=$text.Replace('17960','18928')
$text=$text.Replace('8ae71006df954e47040b79fda535b6212bc2949ce4efa7613ab90bbd0204515a','7e8ea74aec6da10154ae9dc7cabe4b252c20ba1432da0ad096496876c02d9b3e')
Set-Content $wf $text

python -m pip install pyyaml
if($LASTEXITCODE -ne 0){throw 'Could not install PyYAML.'}
$replay=Join-Path $source 'replay_ux_layers.py'
@'
import pathlib, subprocess, tempfile, yaml
root=pathlib.Path.cwd()
workflow=yaml.safe_load((root/'.github/workflows/v011-transcription-check.yml').read_text(encoding='utf-8'))
by_name={s.get('name'):s for s in workflow['jobs']['check']['steps']}
wanted=[
  'Reconstruct verified Trace base source',
  'Apply verified v0.10 overlay',
  'Apply verified v0.11 imports and display overlay',
  'Apply verified v0.11 usability overlay',
  'Apply verified v0.11 local transcription overlay',
  'Prepare Windows assets',
]
for name in wanted:
  step=by_name[name]
  cwd=root/step.get('working-directory','.')
  with tempfile.NamedTemporaryFile('w',suffix='.ps1',encoding='utf-8',delete=False) as f:
    f.write("$ErrorActionPreference='Stop'\n")
    f.write(step['run'])
    script=f.name
  print('UX REPLAY STEP:',name,flush=True)
  subprocess.run(['pwsh','-NoProfile','-File',script],cwd=cwd,check=True)
'@ | Set-Content $replay
Push-Location $source
python replay_ux_layers.py
if($LASTEXITCODE -ne 0){Pop-Location;throw 'Could not reconstruct proven v0.11 source layers.'}
Pop-Location

$parts=Get-ChildItem bootstrap/v011pdf/part* | Sort-Object Name
if($parts.Count -ne 1){throw "Expected one corrected PDF part, found $($parts.Count)."}
$b64=($parts|ForEach-Object{Get-Content $_.FullName -Raw}) -join ''
if($b64.Length -ne 8556){throw "PDF overlay base64 length mismatch: $($b64.Length)"}
$pdfXz=Join-Path $env:RUNNER_TEMP 'trace-v011pdf.patch.xz'
[IO.File]::WriteAllBytes($pdfXz,[Convert]::FromBase64String($b64))
if((Get-FileHash $pdfXz -Algorithm SHA256).Hash.ToLowerInvariant() -ne '6e50b81fac3c4822f3ec6e452e5e8bbfd7f0a8628b0f99d7dbb7502c3ccf2128'){throw 'PDF xz hash mismatch.'}
$pdfPatch=Join-Path $env:RUNNER_TEMP 'trace-v011pdf.patch'
python -c "import lzma,pathlib; pathlib.Path(r'$pdfPatch').write_bytes(lzma.decompress(pathlib.Path(r'$pdfXz').read_bytes()))"
if((Get-FileHash $pdfPatch -Algorithm SHA256).Hash.ToLowerInvariant() -ne '8d1ae4be2c70243f36a815a020ff056701944d5ac2e0fe088403fa5d2b94fbb0'){throw 'PDF patch hash mismatch.'}
Push-Location $source
git apply --check --directory=work $pdfPatch
if($LASTEXITCODE -ne 0){Pop-Location;throw 'PDF overlay preflight failed.'}
git apply --directory=work $pdfPatch
if($LASTEXITCODE -ne 0){Pop-Location;throw 'PDF overlay apply failed.'}
Pop-Location

$parts=Get-ChildItem bootstrap/v011ux/part* | Sort-Object Name
if($parts.Count -ne 7){throw "Expected seven UX parts, found $($parts.Count)."}
$b64=($parts|ForEach-Object{Get-Content $_.FullName -Raw}) -join ''
if($b64.Length -ne 36792){throw "UX overlay base64 length mismatch: $($b64.Length)"}
$uxXz=Join-Path $env:RUNNER_TEMP 'trace-ux-foundation.patch.xz'
[IO.File]::WriteAllBytes($uxXz,[Convert]::FromBase64String($b64))
$uxXzHash=(Get-FileHash $uxXz -Algorithm SHA256).Hash.ToLowerInvariant()
if($uxXzHash -ne '0c59b23925e1ad66b8ca4c7e8931f2c0188698ecb0f29deabcf625d5d5967884'){throw "UX xz hash mismatch: $uxXzHash"}
$uxPatch=Join-Path $env:RUNNER_TEMP 'trace-ux-foundation.patch'
python -c "import lzma,pathlib; pathlib.Path(r'$uxPatch').write_bytes(lzma.decompress(pathlib.Path(r'$uxXz').read_bytes()))"
$uxPatchHash=(Get-FileHash $uxPatch -Algorithm SHA256).Hash.ToLowerInvariant()
if($uxPatchHash -ne 'a6223601b26716813b9a4828e3e77b2bbac1496d7b9540e21761231b5909cc2a'){throw "UX patch hash mismatch: $uxPatchHash"}
Push-Location $source
git apply --check --directory=work $uxPatch
if($LASTEXITCODE -ne 0){Pop-Location;throw 'UX overlay preflight failed.'}
git apply --directory=work $uxPatch
if($LASTEXITCODE -ne 0){Pop-Location;throw 'UX overlay apply failed.'}
Pop-Location

$work=Join-Path $source 'work'
Push-Location $work
node --check src/app.js
if($LASTEXITCODE -ne 0){throw 'JavaScript syntax failed.'}
foreach($test in @('v11_imports_display.py','v11_usability.py','v11_transcription.py','v11_pdf_text.py','v12_ux_foundation.py')){
  python "tests/$test"
  if($LASTEXITCODE -ne 0){throw "Contract failed: $test"}
}

npm install --no-save @tauri-apps/cli@2.11.0
if($LASTEXITCODE -ne 0){throw 'Could not install Tauri CLI.'}
npm run build
if($LASTEXITCODE -ne 0){throw 'Frontend build failed.'}
New-Item -ItemType Directory -Force -Path ux-artifacts | Out-Null
$server=Start-Process -FilePath python -ArgumentList @('-m','http.server','4173','--directory','dist') -PassThru -WindowStyle Hidden
try{
  $ready=$false
  foreach($i in 1..30){try{$r=Invoke-WebRequest 'http://127.0.0.1:4173' -UseBasicParsing -TimeoutSec 1;if($r.StatusCode -eq 200){$ready=$true;break}}catch{};Start-Sleep -Milliseconds 500}
  if(!$ready){throw 'Preview server did not start.'}
  $edge=@("${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe","$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe")|Where-Object{Test-Path $_}|Select-Object -First 1
  if(!$edge){throw 'Microsoft Edge not found.'}
  $profile=Join-Path $env:RUNNER_TEMP 'TraceUXEdgeProfile'
  $shot1440=(Join-Path (Resolve-Path '.').Path 'ux-artifacts/home-1440x900.png')
  $shot1024=(Join-Path (Resolve-Path '.').Path 'ux-artifacts/home-1024x640.png')
  $common=@('--headless=new','--disable-gpu','--no-first-run',"--user-data-dir=$profile")
  & $edge @common '--window-size=1440,900' "--screenshot=$shot1440" 'http://127.0.0.1:4173'
  if($LASTEXITCODE -ne 0 -or !(Test-Path $shot1440)){throw '1440 first-launch screenshot failed.'}
  & $edge @common '--window-size=1024,640' "--screenshot=$shot1024" 'http://127.0.0.1:4173'
  if($LASTEXITCODE -ne 0 -or !(Test-Path $shot1024)){throw '1024 first-launch screenshot failed.'}
  $dom=& $edge @common '--window-size=1440,900' '--dump-dom' 'http://127.0.0.1:4173' 2>$null
  $domText=$dom -join "`n"
  $domText|Set-Content ux-artifacts/home-dom.html
  foreach($required in @('Welcome to Trace.','New project','Open .trace project','Recover backup','No local projects yet')){if(!$domText.Contains($required)){throw "First-launch DOM missing: $required"}}
  foreach($forbidden in @('No text source is open.','View profile','Participant • — years exp.')){if($domText.Contains($forbidden)){throw "Stale first-launch workspace leaked: $forbidden"}}
}finally{if($server -and !$server.HasExited){Stop-Process -Id $server.Id -Force}}

cargo check --manifest-path src-tauri/Cargo.toml
if($LASTEXITCODE -ne 0){throw 'Cargo check failed.'}
cargo test --manifest-path src-tauri/Cargo.toml
if($LASTEXITCODE -ne 0){throw 'Cargo tests failed.'}
npx tauri build
if($LASTEXITCODE -ne 0){throw 'Windows Tauri bundle failed.'}

$nativeSetup=(Get-ChildItem src-tauri/target/release/bundle/nsis/*-setup.exe|Select-Object -First 1).FullName
if(!(Test-Path $nativeSetup)){throw 'NSIS candidate missing.'}
$installDir=Join-Path $env:RUNNER_TEMP 'TraceUXFoundationInstall'
if(Test-Path $installDir){Remove-Item $installDir -Recurse -Force}
$researchDir=Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'Trace UX CI Research Data'
New-Item -ItemType Directory -Force -Path $researchDir|Out-Null
$sentinel=Join-Path $researchDir 'research-data-must-survive.txt'
'Trace UX research data preservation sentinel'|Set-Content $sentinel
$p=Start-Process -FilePath $nativeSetup -ArgumentList @('/S',"/D=$installDir") -Wait -PassThru
if($p.ExitCode -ne 0){throw "Candidate install failed: $($p.ExitCode)"}
$exe=Join-Path $installDir 'Trace.exe'
if(!(Test-Path $exe)){throw 'Installed Trace.exe missing.'}
$trace=Start-Process -FilePath $exe -WorkingDirectory $installDir -PassThru
Start-Sleep -Seconds 10
if($trace.HasExited){throw "Installed UX candidate exited: $($trace.ExitCode)"}
Stop-Process -Id $trace.Id -Force
Start-Sleep -Seconds 2
$uninstaller=Get-ChildItem $installDir -Filter '*uninstall*.exe' -File|Select-Object -First 1
if(!$uninstaller){throw 'Candidate uninstaller missing.'}
$u=Start-Process -FilePath $uninstaller.FullName -ArgumentList '/S' -Wait -PassThru
if($u.ExitCode -ne 0){throw "Candidate uninstall failed: $($u.ExitCode)"}
Start-Sleep -Seconds 2
if(Test-Path $exe){throw 'Trace.exe remains after uninstall.'}
if(!(Test-Path $sentinel)){throw 'Research-data sentinel removed.'}
$nsisHash=(Get-FileHash $nativeSetup -Algorithm SHA256).Hash.ToLowerInvariant()
@"
Trace UX Foundation Windows verification
run_id=$env:GITHUB_RUN_ID
trigger_sha=$env:GITHUB_SHA
ux_overlay_patch_sha256=a6223601b26716813b9a4828e3e77b2bbac1496d7b9540e21761231b5909cc2a
first_launch_home=true
first_launch_1440_screenshot=true
first_launch_1024_screenshot=true
no_phantom_workspace_state=true
v011_regressions_green=true
rust_check_green=true
rust_tests_green=true
windows_bundle_green=true
installed_copy_launched=true
installed_copy_survived_10_seconds=true
native_uninstall_green=true
research_data_preserved=true
candidate_nsis_sha256=$nsisHash
"@|Set-Content ux-artifacts/UX-VERIFICATION.txt
Pop-Location
