$ErrorActionPreference='Stop'
$work=Join-Path (Join-Path (Resolve-Path '.').Path 'source') 'work'
$fixture=Join-Path $work 'phase4-ci.html'
Copy-Item 'ci/phase4-ci.html' $fixture -Force
$server=Start-Process -FilePath python -ArgumentList @('-m','http.server','4182','--directory',$work) -PassThru -WindowStyle Hidden
try{
    $ready=$false
    foreach($i in 1..30){try{$r=Invoke-WebRequest 'http://127.0.0.1:4182/phase4-ci.html' -UseBasicParsing -TimeoutSec 1;if($r.StatusCode -eq 200){$ready=$true;break}}catch{};Start-Sleep -Milliseconds 500}
    if(!$ready){ throw 'Phase 4 browser fixture server did not start.' }
    $edge=@("${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe","$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe")|Where-Object{Test-Path $_}|Select-Object -First 1
    if(!$edge){ throw 'Microsoft Edge not found for Phase 4 browser gate.' }
    $artifactDir=Join-Path $work 'ux-artifacts'
    $views=@(
      @{Name='analyse-1440x900';View='analyse';Size='1440,900';Need=@('Look for patterns, then return to the evidence.','Where coding is concentrated','Participant × code matrix','view=analyse;overflow=false')},
      @{Name='analyse-1024x640';View='analyse';Size='1024,640';Need=@('EVIDENCE IN VIEW','Participant × code matrix','view=analyse;overflow=false')},
      @{Name='analyse-filtered-1440x900';View='analyse-filtered';Size='1440,900';Need=@('Emotional exhaustion','Clear filters','Passages in view','view=analyse-filtered;overflow=false')},
      @{Name='write-1440x900';View='write';Size='1440,900';Need=@('Build the finding beside its evidence.','Pressure without recovery','Linked to this finding','Available evidence','view=write;overflow=false')},
      @{Name='write-1024x640';View='write';Size='1024,640';Need=@('Build the finding beside its evidence.','EVIDENCE','Pressure without recovery','view=write;overflow=false')}
    )
    foreach($v in $views){
      $profile=Join-Path $env:RUNNER_TEMP ("TracePhase4Edge-"+$v.Name)
      $url='http://127.0.0.1:4182/phase4-ci.html?view='+$v.View
      $shot=Join-Path $artifactDir ($v.Name+'.png')
      & $edge '--headless=new' '--disable-gpu' '--no-first-run' '--virtual-time-budget=1400' "--user-data-dir=$profile" "--window-size=$($v.Size)" "--screenshot=$shot" $url
      if($LASTEXITCODE -ne 0 -or !(Test-Path $shot)){ throw "Phase 4 screenshot failed: $($v.Name)" }
      $domProfile=$profile+'-dom'
      $dom=& $edge '--headless=new' '--disable-gpu' '--no-first-run' '--virtual-time-budget=1400' "--user-data-dir=$domProfile" "--window-size=$($v.Size)" '--dump-dom' $url 2>$null
      $text=$dom -join "`n"
      foreach($needle in $v.Need){if(!$text.Contains($needle)){throw "Phase 4 browser contract missing '$needle' in $($v.Name)"}}
    }
    Add-Content (Join-Path $artifactDir 'UX-VERIFICATION.txt') "phase4_windows_edge_smoke=true`nphase4_analyse_1440=true`nphase4_analyse_1024_no_horizontal_overflow=true`nphase4_filtered_analysis=true`nphase4_write_1440=true`nphase4_write_1024_no_horizontal_overflow=true"
} finally {
    if($server -and !$server.HasExited){Stop-Process -Id $server.Id -Force}
    Remove-Item $fixture -Force -ErrorAction SilentlyContinue
}
