param(
  [Parameter(Mandatory=$true)][string]$NewSetup,
  [Parameter(Mandatory=$true)][string]$ReferenceHash,
  [Parameter(Mandatory=$true)][string]$ReleaseDir
)

$ErrorActionPreference='Stop'
$NewSetup=(Resolve-Path $NewSetup).Path
$ReferenceHash=$ReferenceHash.ToLowerInvariant()
New-Item -ItemType Directory -Force -Path $ReleaseDir | Out-Null

function Invoke-Setup([string[]]$Arguments){
  & $NewSetup @Arguments | Out-Host
  $code=$LASTEXITCODE
  return $code
}
function Hash-Of([string]$Path){
  if(!(Test-Path $Path)){return 'missing'}
  return (Get-FileHash $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Assert-True([bool]$Condition,[string]$Message){if(!$Condition){throw $Message}}

$dir=Join-Path $env:RUNNER_TEMP 'TraceV0121Matrix-Rollback'
if(Test-Path $dir){Remove-Item $dir -Recurse -Force}

$root=Join-Path $env:LOCALAPPDATA 'com.trace.research'
$projectDir=Join-Path $root 'Projects/ci-v0121-rollback'
$backupDir=Join-Path $root 'Backups/ci-v0121-rollback'
New-Item -ItemType Directory -Force -Path $projectDir,$backupDir | Out-Null
$project=Join-Path $projectDir 'research-project-must-survive.txt'
$backup=Join-Path $backupDir 'verified-backup-must-survive.txt'
'Rollback project sentinel' | Set-Content $project
'Rollback backup sentinel' | Set-Content $backup

$exit=Invoke-Setup @('--silent-install','--install-dir',$dir)
Assert-True ($exit -eq 0) "Initial rollback-fixture install failed with exit code $exit."
$exe=Join-Path $dir 'Trace.exe'
$before=Hash-Of $exe
Assert-True ($before -eq $ReferenceHash) 'Rollback fixture did not begin with exact v0.12.1 bytes.'

$env:TRACE_SETUP_FORCE_ROLLBACK_TEST='1'
try {
  $rollbackExit=Invoke-Setup @('--silent-install','--install-dir',$dir)
} finally {
  Remove-Item Env:TRACE_SETUP_FORCE_ROLLBACK_TEST -ErrorAction SilentlyContinue
}
Assert-True ($rollbackExit -ne 0) 'Forced rollback probe unexpectedly reported success.'
$after=Hash-Of $exe
Assert-True ($after -eq $before) 'Forced rollback did not restore the previous Trace.exe exactly.'
Assert-True (Test-Path $project) 'Forced rollback removed research project data.'
Assert-True (Test-Path $backup) 'Forced rollback removed verified backup data.'

# Prove the installation remains maintainable immediately after rollback.
$retryExit=Invoke-Setup @('--silent-install','--install-dir',$dir)
Assert-True ($retryExit -eq 0) "Maintenance retry after rollback failed with exit code $retryExit."
$retryHash=Hash-Of $exe
Assert-True ($retryHash -eq $ReferenceHash) 'Retry after rollback does not match exact v0.12.1 bytes.'
Assert-True (Test-Path $project) 'Retry after rollback removed research project data.'
Assert-True (Test-Path $backup) 'Retry after rollback removed verified backup data.'

$uninstallExit=Invoke-Setup @('--silent-uninstall','--install-dir',$dir)
Assert-True ($uninstallExit -eq 0) "Uninstall after rollback verification failed with exit code $uninstallExit."
Start-Sleep -Seconds 3
Assert-True (!(Test-Path $exe)) 'Trace.exe remains after rollback-verification uninstall.'
Assert-True (Test-Path $project) 'Rollback-verification uninstall removed research project data.'
Assert-True (Test-Path $backup) 'Rollback-verification uninstall removed verified backup data.'

@(
  'Trace 0.12.1 exact branded rollback verification',
  "before_hash=$before",
  "forced_rollback_exit=$rollbackExit",
  "restored_hash=$after",
  'exact_application_bytes_restored=true',
  'research_project_preserved=true',
  'verified_backup_preserved=true',
  'retry_after_rollback_green=true',
  'post_rollback_uninstall_green=true'
) | Set-Content (Join-Path $ReleaseDir 'ROLLBACK-VERIFICATION.txt')
Get-Content (Join-Path $ReleaseDir 'ROLLBACK-VERIFICATION.txt')
