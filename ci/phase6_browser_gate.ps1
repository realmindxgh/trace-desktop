$ErrorActionPreference='Stop'
$work=Join-Path (Join-Path (Resolve-Path '.').Path 'source') 'work'
$fixture=Join-Path $work 'phase6-ci.html'
Copy-Item 'ci/phase6-ci.html' $fixture -Force
$server=Start-Process -FilePath python -ArgumentList @('-m','http.server','4184','--directory',$work) -PassThru -WindowStyle Hidden
try{
    $ready=$false
    foreach($i in 1..30){try{$r=Invoke-WebRequest 'http://127.0.0.1:4184/phase6-ci.html' -UseBasicParsing -TimeoutSec 1;if($r.StatusCode -eq 200){$ready=$true;break}}catch{};Start-Sleep -Milliseconds 500}
    if(!$ready){throw 'Phase 6 browser fixture server did not start.'}
    $edge=@("${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe","$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe")|Where-Object{Test-Path $_}|Select-Object -First 1
    if(!$edge){throw 'Microsoft Edge not found for Phase 6 browser gate.'}
    $artifactDir=Join-Path $work 'ux-artifacts'
    New-Item -ItemType Directory -Force -Path $artifactDir|Out-Null
    $views=@(
      @{Name='data-large-1440x900';View='data';Size='1440,900';Need=@('Showing 100 of 250 sources','Show 100 more','ready;overflow=false;sources=100','ariaCurrent=true;skip=true')},
      @{Name='project-settings-1440x900';View='project-settings';Size='1440,900';Need=@('PROJECT SETTINGS','TRACE AI SCOPE','Project database ready','Save project settings')},
      @{Name='project-settings-1024x640';View='project-settings';Size='1024,640';Need=@('PROJECT SETTINGS','Research questions','No project evidence is available to AI features.','overflow=false')},
      @{Name='trace-ai-1440x900';View='ai';Size='1440,900';Need=@('Researcher-led, even when AI is used.','No AI provider is configured in this build.','PROJECT AI SCOPE')},
      @{Name='confirm-delete-1440x900';View='confirm';Size='1440,900';Need=@('Interview 001.txt','12 coding references','3 evidence selections','Delete source')},
      @{Name='recovery-details-1440x900';View='recovery';Size='1440,900';Need=@('SESSION RECOVERY','Trace reopened the last safe project state.','What Trace did not do:')},
      @{Name='recovery-center-1440x900';View='recovery-center';Size='1440,900';Need=@('RECOVERY CENTER','Restore a verified copy without overwriting current research.','Verified backup discovery is available in the installed Windows app.')}
    )
    foreach($v in $views){
      $profile=Join-Path $env:RUNNER_TEMP ('TracePhase6Edge-'+$v.Name)
      $url='http://127.0.0.1:4184/phase6-ci.html?view='+$v.View
      $shot=Join-Path $artifactDir ($v.Name+'.png')
      & $edge '--headless=new' '--disable-gpu' '--no-first-run' '--virtual-time-budget=1600' "--user-data-dir=$profile" "--window-size=$($v.Size)" "--screenshot=$shot" $url
      if($LASTEXITCODE -ne 0 -or !(Test-Path $shot)){throw "Phase 6 screenshot failed: $($v.Name)"}
      $domProfile=$profile+'-dom'
      $dom=& $edge '--headless=new' '--disable-gpu' '--no-first-run' '--virtual-time-budget=1600' "--user-data-dir=$domProfile" "--window-size=$($v.Size)" '--dump-dom' $url 2>$null
      $text=$dom -join "`n"
      if($text.Contains('overflow=true')){throw "Phase 6 horizontal overflow detected: $($v.Name)"}
      foreach($needle in $v.Need){if(!$text.Contains($needle)){throw "Phase 6 browser contract missing '$needle' in $($v.Name)"}}
    }
    Add-Content (Join-Path $artifactDir 'UX-VERIFICATION.txt') "phase6_windows_edge_smoke=true`nphase6_large_project_100_of_250=true`nphase6_project_settings=true`nphase6_project_settings_1024_no_horizontal_overflow=true`nphase6_contextual_ai=true`nphase6_consequence_confirmation=true`nphase6_recovery_details=true`nphase6_recovery_center=true`nphase6_accessibility_markers=true"
} finally {
    if($server -and !$server.HasExited){Stop-Process -Id $server.Id -Force}
    Remove-Item $fixture -Force -ErrorAction SilentlyContinue
}
