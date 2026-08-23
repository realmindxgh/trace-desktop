$ErrorActionPreference='Stop'
$work=Join-Path (Join-Path (Resolve-Path '.').Path 'source') 'work'
$fixture=Join-Path $work 'phase5-ci.html'
Copy-Item 'ci/phase5-ci.html' $fixture -Force
$server=Start-Process -FilePath python -ArgumentList @('-m','http.server','4183','--directory',$work) -PassThru -WindowStyle Hidden
try{
  $ready=$false
  foreach($i in 1..30){try{$r=Invoke-WebRequest 'http://127.0.0.1:4183/phase5-ci.html' -UseBasicParsing -TimeoutSec 1;if($r.StatusCode -eq 200){$ready=$true;break}}catch{};Start-Sleep -Milliseconds 500}
  if(!$ready){throw 'Phase 5 browser fixture server did not start.'}
  $edge=@("${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe","$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe")|Where-Object{Test-Path $_}|Select-Object -First 1
  if(!$edge){throw 'Microsoft Edge not found for Phase 5 browser gate.'}
  $artifactDir=Join-Path $work 'ux-artifacts'
  $views=@(
    @{Name='import-1440x900';View='import';Size='1440,900';Need=@('IMPORT RESEARCH DATA','Documents & transcripts','Survey data','Audio & video','REFI-QDA exchange','view=import;overflow=false;fileInput=true;modal=true')},
    @{Name='import-1024x640';View='import';Size='1024,640';Need=@('What are you bringing into Trace?','Images','Portable .trace project','view=import;overflow=false;fileInput=true;modal=true')},
    @{Name='settings-1440x900';View='settings';Size='1440,900';Need=@('Set up the application around your research.','Appearance & readability','Keyboard productivity','Version information unavailable','view=settings;overflow=false;fileInput=true;modal=true')},
    @{Name='settings-1024x640';View='settings';Size='1024,640';Need=@('Reduce interface motion','Resume last project','Privacy-safe diagnostics','view=settings;overflow=false;fileInput=true;modal=true')},
    @{Name='commands-1440x900';View='commands';Size='1440,900';Need=@('Import research data','New code','New memo','Alt+4','Ctrl+I','view=commands;overflow=false;fileInput=true;modal=true')},
    @{Name='error-1024x640';View='error';Size='1024,640';Need=@('TRACE COULD NOT FINISH THAT','Trace did not change your research project.','Technical details','view=error;overflow=false;fileInput=true;modal=true')}
  )
  foreach($v in $views){
    $profile=Join-Path $env:RUNNER_TEMP ('TracePhase5Edge-'+$v.Name);$url='http://127.0.0.1:4183/phase5-ci.html?view='+$v.View;$shot=Join-Path $artifactDir ($v.Name+'.png')
    & $edge '--headless=new' '--disable-gpu' '--no-first-run' '--virtual-time-budget=1500' "--user-data-dir=$profile" "--window-size=$($v.Size)" "--screenshot=$shot" $url
    if($LASTEXITCODE -ne 0 -or !(Test-Path $shot)){throw "Phase 5 screenshot failed: $($v.Name)"}
    $dom=& $edge '--headless=new' '--disable-gpu' '--no-first-run' '--virtual-time-budget=1500' "--user-data-dir=$profile-dom" "--window-size=$($v.Size)" '--dump-dom' $url 2>$null;$text=$dom -join "`n"
    foreach($needle in $v.Need){if(!$text.Contains($needle)){throw "Phase 5 browser contract missing '$needle' in $($v.Name)"}}
    if($text.Contains('Version 0.10.0')){throw "Stale version leaked into Phase 5 settings: $($v.Name)"}
  }
  Add-Content (Join-Path $artifactDir 'UX-VERIFICATION.txt') "phase5_windows_edge_smoke=true`nphase5_import_1440=true`nphase5_import_1024_no_horizontal_overflow=true`nphase5_settings_1440=true`nphase5_settings_1024_no_horizontal_overflow=true`nphase5_command_palette=true`nphase5_human_error_dialog=true`nphase5_real_file_input=true"
} finally {if($server -and !$server.HasExited){Stop-Process -Id $server.Id -Force};Remove-Item $fixture -Force -ErrorAction SilentlyContinue}
