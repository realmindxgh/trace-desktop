param(
  [Parameter(Mandatory=$true)][string]$NewSetup,
  [Parameter(Mandatory=$true)][string]$OldSetup,
  [Parameter(Mandatory=$true)][string]$ReferenceHash,
  [Parameter(Mandatory=$true)][string]$ReleaseDir
)

$ErrorActionPreference = 'Stop'
$ReferenceHash = $ReferenceHash.ToLowerInvariant()
$NewSetup = (Resolve-Path $NewSetup).Path
$OldSetup = (Resolve-Path $OldSetup).Path
New-Item -ItemType Directory -Force -Path $ReleaseDir | Out-Null

$currentScenario = 'initialization'
$diagnosticPath = Join-Path $ReleaseDir 'MAINTENANCE-DIAGNOSTICS.txt'
$diagnosticWritten = $false
$records = [ordered]@{}

function Write-MatrixFailure([string]$Message){
  if($script:diagnosticWritten){ return }
  $script:diagnosticWritten = $true
  $safeMessage = ($Message -replace '[\r\n]+',' ').Trim()
  $completed = @($script:records.Keys | Where-Object { $script:records[$_] -eq 'green' }) -join ','
  @(
    'Trace 0.12.1 exact installer maintenance diagnostic',
    'result=failure',
    "scenario=$script:currentScenario",
    "assertion=$safeMessage",
    "completed_green=$completed",
    "run_id=$env:GITHUB_RUN_ID",
    "run_attempt=$env:GITHUB_RUN_ATTEMPT",
    "timestamp_utc=$([DateTime]::UtcNow.ToString('o'))"
  ) | Set-Content $script:diagnosticPath
  Write-Host "TRACE_MAINTENANCE_FAILURE scenario=$script:currentScenario assertion=$safeMessage"
  Get-Content $script:diagnosticPath | ForEach-Object { Write-Host $_ }

  # Persist only sanitized CI metadata. Never write research content into the repository.
  try {
    $controlRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
    $statusDir = Join-Path $controlRoot 'build-status'
    New-Item -ItemType Directory -Force -Path $statusDir | Out-Null
    $statusPath = Join-Path $statusDir 'windows-v0121-maintenance-diagnostic.txt'
    Copy-Item $script:diagnosticPath $statusPath -Force
    Push-Location $controlRoot
    try {
      git config user.name 'trace-build-bot'
      git config user.email 'actions@users.noreply.github.com'
      git add build-status/windows-v0121-maintenance-diagnostic.txt
      if(git status --porcelain -- build-status/windows-v0121-maintenance-diagnostic.txt){
        git commit -m 'ci: record v0.12.1 maintenance failure diagnostic [skip ci]'
        git pull --rebase origin trace-v0121
        git push origin HEAD:trace-v0121
      }
    } finally {
      Pop-Location
    }
  } catch {
    Write-Warning "Could not persist maintenance diagnostic to build-status: $($_.Exception.Message)"
  }
}

function Assert-True([bool]$Condition,[string]$Message){
  if(-not $Condition){
    Write-MatrixFailure $Message
    throw $Message
  }
}

function Invoke-TraceSetup([string]$Setup,[string[]]$Arguments){
  & $Setup @Arguments | Out-Host
  $code=$LASTEXITCODE
  return $code
}

function File-Hash([string]$Path){
  if(!(Test-Path $Path)){ return 'missing' }
  return (Get-FileHash $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Fresh-Dir([string]$Name){
  $dir=Join-Path $env:RUNNER_TEMP $Name
  if(Test-Path $dir){ Remove-Item $dir -Recurse -Force }
  return $dir
}

function New-ResearchSentinels([string]$Scenario){
  $root=Join-Path $env:LOCALAPPDATA 'com.trace.research'
  $projectDir=Join-Path $root "Projects/ci-v0121-$Scenario"
  $backupDir=Join-Path $root "Backups/ci-v0121-$Scenario"
  New-Item -ItemType Directory -Force -Path $projectDir,$backupDir | Out-Null
  $project=Join-Path $projectDir 'research-project-must-survive.txt'
  $backup=Join-Path $backupDir 'verified-backup-must-survive.txt'
  "Trace project sentinel for $Scenario" | Set-Content $project
  "Trace backup sentinel for $Scenario" | Set-Content $backup
  return @{ Project=$project; Backup=$backup }
}

function Assert-Sentinels($Sentinels,[string]$Scenario){
  Assert-True (Test-Path $Sentinels.Project) "$Scenario removed research project data."
  Assert-True (Test-Path $Sentinels.Backup) "$Scenario removed verified backup data."
}

function Launch-And-Prove([string]$Exe,[string]$WorkingDir,[string]$Scenario){
  $p=Start-Process -FilePath $Exe -WorkingDirectory $WorkingDir -PassThru
  Start-Sleep -Seconds 10
  if($p.HasExited){
    $message="$Scenario installed copy exited unexpectedly with code $($p.ExitCode)."
    Write-MatrixFailure $message
    throw $message
  }
  Stop-Process -Id $p.Id -Force
  Start-Sleep -Seconds 2
}

# 1. Exact clean install, launch, uninstall, preservation.
$currentScenario='clean_install'
$dir=Fresh-Dir 'TraceV0121Matrix-Clean'
$sentinels=New-ResearchSentinels 'clean'
$exit=Invoke-TraceSetup $NewSetup @('--silent-install','--install-dir',$dir)
Assert-True ($exit -eq 0) "Clean install failed with exit code $exit."
$exe=Join-Path $dir 'Trace.exe'
Assert-True (Test-Path $exe) 'Clean install did not create Trace.exe.'
$hash=File-Hash $exe
Assert-True ($hash -eq $ReferenceHash) 'Clean branded install does not match native v0.12.1 reference hash.'
Launch-And-Prove $exe $dir 'Clean install'
$exit=Invoke-TraceSetup $NewSetup @('--silent-uninstall','--install-dir',$dir)
Assert-True ($exit -eq 0) "Clean uninstall failed with exit code $exit."
Start-Sleep -Seconds 3
Assert-True (!(Test-Path $exe)) 'Clean uninstall left Trace.exe behind.'
Assert-Sentinels $sentinels 'Clean uninstall'
$records.clean_install='green'
$records.clean_install_hash=$hash

# 2. Real exact v0.12 -> v0.12.1 closed-app upgrade.
$currentScenario='closed_upgrade'
$dir=Fresh-Dir 'TraceV0121Matrix-Upgrade'
$exit=Invoke-TraceSetup $OldSetup @('--silent-install','--install-dir',$dir)
Assert-True ($exit -eq 0) "Verified v0.12 install failed with exit code $exit."
$exe=Join-Path $dir 'Trace.exe'
Assert-True (Test-Path $exe) 'v0.12 Trace.exe is missing before upgrade.'
$oldHash=File-Hash $exe
$sentinels=New-ResearchSentinels 'upgrade'
$exit=Invoke-TraceSetup $NewSetup @('--silent-install','--install-dir',$dir)
Assert-True ($exit -eq 0) "Closed-app v0.12 -> v0.12.1 upgrade failed with exit code $exit."
$newHash=File-Hash $exe
Assert-True ($newHash -ne $oldHash) 'Closed-app upgrade did not replace the v0.12 executable.'
Assert-True ($newHash -eq $ReferenceHash) 'Closed-app upgrade does not match exact v0.12.1 reference hash.'
Assert-Sentinels $sentinels 'Closed-app upgrade'
Launch-And-Prove $exe $dir 'Closed-app upgrade'
$exit=Invoke-TraceSetup $NewSetup @('--silent-uninstall','--install-dir',$dir)
Assert-True ($exit -eq 0) "Post-upgrade uninstall failed with exit code $exit."
Start-Sleep -Seconds 3
Assert-True (!(Test-Path $exe)) 'Post-upgrade uninstall left Trace.exe behind.'
Assert-Sentinels $sentinels 'Post-upgrade uninstall'
$records.closed_upgrade='green'
$records.previous_v012_hash=$oldHash
$records.upgraded_v0121_hash=$newHash

# 3. Running old process must block safely, preserve old bytes, then succeed after close/retry.
$currentScenario='running_process_block_retry'
$dir=Fresh-Dir 'TraceV0121Matrix-Running'
$exit=Invoke-TraceSetup $OldSetup @('--silent-install','--install-dir',$dir)
Assert-True ($exit -eq 0) "Could not install v0.12 for running-process test; exit $exit."
$exe=Join-Path $dir 'Trace.exe'
$oldHash=File-Hash $exe
$sentinels=New-ResearchSentinels 'running-block'
$oldProcess=Start-Process -FilePath $exe -WorkingDirectory $dir -PassThru
Start-Sleep -Seconds 6
Assert-True (!$oldProcess.HasExited) 'v0.12 exited before the running-process maintenance test.'
$blockedExit=Invoke-TraceSetup $NewSetup @('--silent-install','--install-dir',$dir)
$blockedHash=File-Hash $exe
Assert-True ($blockedExit -ne 0) 'Installer did not safely block while the previous Trace process was running.'
Assert-True ($blockedHash -eq $oldHash) 'Blocked running-process update modified the existing Trace.exe.'
Assert-True (!$oldProcess.HasExited) 'Blocked maintenance unexpectedly terminated the running Trace process.'
Assert-Sentinels $sentinels 'Blocked running-process update'
Stop-Process -Id $oldProcess.Id -Force
Start-Sleep -Seconds 2
$retryExit=Invoke-TraceSetup $NewSetup @('--silent-install','--install-dir',$dir)
Assert-True ($retryExit -eq 0) "Retry after closing Trace failed with exit code $retryExit."
$retryHash=File-Hash $exe
Assert-True ($retryHash -eq $ReferenceHash) 'Retry after closing Trace did not install exact v0.12.1 bytes.'
Assert-Sentinels $sentinels 'Retry after closing Trace'
Launch-And-Prove $exe $dir 'Running-process retry'
$exit=Invoke-TraceSetup $NewSetup @('--silent-uninstall','--install-dir',$dir)
Assert-True ($exit -eq 0) "Uninstall after running-process retry failed with exit code $exit."
Assert-Sentinels $sentinels 'Uninstall after running-process retry'
$records.running_process_block='green'
$records.running_block_exit=$blockedExit
$records.running_retry='green'

# 4. Same-version repair / partial install with missing executable.
$currentScenario='missing_exe_repair'
$dir=Fresh-Dir 'TraceV0121Matrix-MissingExe'
$exit=Invoke-TraceSetup $NewSetup @('--silent-install','--install-dir',$dir)
Assert-True ($exit -eq 0) "Initial v0.12.1 install for repair failed with exit code $exit."
$exe=Join-Path $dir 'Trace.exe'
$sentinels=New-ResearchSentinels 'missing-exe-repair'
Remove-Item $exe -Force
Assert-True (!(Test-Path $exe)) 'Could not create missing-Trace.exe repair fixture.'
$repairExit=Invoke-TraceSetup $NewSetup @('--silent-install','--install-dir',$dir)
Assert-True ($repairExit -eq 0) "Same-version missing-EXE repair failed with exit code $repairExit."
$repairHash=File-Hash $exe
Assert-True ($repairHash -eq $ReferenceHash) 'Missing-EXE repair did not restore exact v0.12.1 bytes.'
Assert-Sentinels $sentinels 'Missing-EXE repair'
Launch-And-Prove $exe $dir 'Missing-EXE repair'
$exit=Invoke-TraceSetup $NewSetup @('--silent-uninstall','--install-dir',$dir)
Assert-True ($exit -eq 0) "Uninstall after missing-EXE repair failed with exit code $exit."
Assert-Sentinels $sentinels 'Uninstall after missing-EXE repair'
$records.missing_exe_repair='green'

# 5. Partial install with missing uninstaller should recover without touching research data.
$currentScenario='missing_uninstaller_recovery'
$dir=Fresh-Dir 'TraceV0121Matrix-MissingUninstaller'
$exit=Invoke-TraceSetup $NewSetup @('--silent-install','--install-dir',$dir)
Assert-True ($exit -eq 0) "Initial v0.12.1 install for uninstaller recovery failed with exit code $exit."
$exe=Join-Path $dir 'Trace.exe'
$sentinels=New-ResearchSentinels 'missing-uninstaller-repair'
$uninstaller=Get-ChildItem $dir -Filter '*uninstall*.exe' -File | Select-Object -First 1
Assert-True ($null -ne $uninstaller) 'Could not locate generated uninstaller for recovery fixture.'
Remove-Item $uninstaller.FullName -Force
Assert-True (!(Test-Path $uninstaller.FullName)) 'Could not create missing-uninstaller fixture.'
$repairExit=Invoke-TraceSetup $NewSetup @('--silent-install','--install-dir',$dir)
Assert-True ($repairExit -eq 0) "Missing-uninstaller recovery failed with exit code $repairExit."
Assert-True ((File-Hash $exe) -eq $ReferenceHash) 'Missing-uninstaller recovery changed Trace.exe away from exact v0.12.1 bytes.'
$restoredUninstaller=Get-ChildItem $dir -Filter '*uninstall*.exe' -File | Select-Object -First 1
Assert-True ($null -ne $restoredUninstaller) 'Missing-uninstaller recovery did not restore an uninstaller.'
Assert-Sentinels $sentinels 'Missing-uninstaller recovery'
$exit=Invoke-TraceSetup $NewSetup @('--silent-uninstall','--install-dir',$dir)
Assert-True ($exit -eq 0) "Uninstall after missing-uninstaller recovery failed with exit code $exit."
Assert-Sentinels $sentinels 'Uninstall after missing-uninstaller recovery'
$records.missing_uninstaller_recovery='green'

# 6. Custom install location, including spaces, must remain maintainable.
$currentScenario='custom_path'
$dir=Fresh-Dir 'Trace v0.12.1 Custom Install Path'
$sentinels=New-ResearchSentinels 'custom-path'
$exit=Invoke-TraceSetup $NewSetup @('--silent-install','--install-dir',$dir)
Assert-True ($exit -eq 0) "Custom-path install failed with exit code $exit."
$exe=Join-Path $dir 'Trace.exe'
Assert-True ((File-Hash $exe) -eq $ReferenceHash) 'Custom-path install does not match exact v0.12.1 bytes.'
# A second same-version maintenance pass must be harmless and path-stable.
$secondExit=Invoke-TraceSetup $NewSetup @('--silent-install','--install-dir',$dir)
Assert-True ($secondExit -eq 0) "Custom-path same-version maintenance failed with exit code $secondExit."
Assert-True ((File-Hash $exe) -eq $ReferenceHash) 'Custom-path maintenance changed the exact executable bytes.'
Assert-Sentinels $sentinels 'Custom-path maintenance'
Launch-And-Prove $exe $dir 'Custom-path install'
$exit=Invoke-TraceSetup $NewSetup @('--silent-uninstall','--install-dir',$dir)
Assert-True ($exit -eq 0) "Custom-path uninstall failed with exit code $exit."
Start-Sleep -Seconds 3
Assert-True (!(Test-Path $exe)) 'Custom-path uninstall left Trace.exe behind.'
Assert-Sentinels $sentinels 'Custom-path uninstall'
$records.custom_path='green'

$currentScenario='complete'
$recordPath=Join-Path $ReleaseDir 'MAINTENANCE-MATRIX.txt'
@(
  'Trace 0.12.1 exact installer maintenance matrix',
  "clean_install=$($records.clean_install)",
  "clean_install_hash=$($records.clean_install_hash)",
  "closed_upgrade=$($records.closed_upgrade)",
  "previous_v012_hash=$($records.previous_v012_hash)",
  "upgraded_v0121_hash=$($records.upgraded_v0121_hash)",
  "running_process_block=$($records.running_process_block)",
  "running_block_exit=$($records.running_block_exit)",
  "running_retry=$($records.running_retry)",
  "missing_exe_repair=$($records.missing_exe_repair)",
  "missing_uninstaller_recovery=$($records.missing_uninstaller_recovery)",
  "custom_path=$($records.custom_path)",
  'research_data_preserved=true',
  'verified_backups_preserved=true'
) | Set-Content $recordPath
Get-Content $recordPath
