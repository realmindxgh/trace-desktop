$ErrorActionPreference='Stop'
$work=Join-Path (Join-Path (Resolve-Path '.').Path 'source') 'work'
$fixture=Join-Path $work 'phase3-ci.html'
Copy-Item 'ci/phase3-ci.html' $fixture -Force
$server=Start-Process -FilePath python -ArgumentList @('-m','http.server','4181','--directory',$work) -PassThru -WindowStyle Hidden
try{
    $ready=$false
    foreach($i in 1..30){try{$r=Invoke-WebRequest 'http://127.0.0.1:4181/phase3-ci.html' -UseBasicParsing -TimeoutSec 1;if($r.StatusCode -eq 200){$ready=$true;break}}catch{};Start-Sleep -Milliseconds 500}
    if(!$ready){ throw 'Phase 3 browser fixture server did not start.' }
    $edge=@("${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe","$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe")|Where-Object{Test-Path $_}|Select-Object -First 1
    if(!$edge){ throw 'Microsoft Edge not found for Phase 3 browser gate.' }
    $artifactDir=Join-Path $work 'ux-artifacts'
    $views=@(
      @{Name='themes-1440x900';View='themes';Size='1440,900';Need=@('CODES &amp; THEMES','Workload pressure','Pressure without recovery','ready=5;overflow=false')},
      @{Name='themes-1024x640';View='themes';Size='1024,640';Need=@('CODES &amp; THEMES','Staffing gaps','Protective relationships','ready=5;overflow=false')},
      @{Name='code-review-1440x900';View='code-review';Size='1440,900';Need=@('CODE REVIEW','Emotional exhaustion','Passages coded here')},
      @{Name='theme-review-1440x900';View='theme-review';Size='1440,900';Need=@('THEME REVIEW','Pressure without recovery','Evidence represented by this theme')},
      @{Name='code-editor-1440x900';View='code-editor';Size='1440,900';Need=@('NEW CODE','Parent code','Create an analytical code.')}
    )
    foreach($v in $views){
      $profile=Join-Path $env:RUNNER_TEMP ("TracePhase3Edge-"+$v.Name)
      $url='http://127.0.0.1:4181/phase3-ci.html?view='+$v.View
      $shot=Join-Path $artifactDir ($v.Name+'.png')
      & $edge '--headless=new' '--disable-gpu' '--no-first-run' '--virtual-time-budget=1200' "--user-data-dir=$profile" "--window-size=$($v.Size)" "--screenshot=$shot" $url
      if($LASTEXITCODE -ne 0 -or !(Test-Path $shot)){ throw "Phase 3 screenshot failed: $($v.Name)" }
      $domProfile=$profile+'-dom'
      $dom=& $edge '--headless=new' '--disable-gpu' '--no-first-run' '--virtual-time-budget=1200' "--user-data-dir=$domProfile" "--window-size=$($v.Size)" '--dump-dom' $url 2>$null
      $text=$dom -join "`n"
      foreach($needle in $v.Need){if(!$text.Contains($needle)){throw "Phase 3 browser contract missing '$needle' in $($v.Name)"}}
    }
    Add-Content (Join-Path $artifactDir 'UX-VERIFICATION.txt') "phase3_windows_edge_smoke=true`nphase3_themes_1440=true`nphase3_themes_1024_no_horizontal_overflow=true`nphase3_code_review=true`nphase3_theme_review=true`nphase3_code_editor=true"
} finally {
    if($server -and !$server.HasExited){Stop-Process -Id $server.Id -Force}
    Remove-Item $fixture -Force -ErrorAction SilentlyContinue
}
