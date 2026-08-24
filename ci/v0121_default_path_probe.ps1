param(
  [Parameter(Mandatory=$true)][string]$NewSetup,
  [Parameter(Mandatory=$true)][string]$OldSetup,
  [Parameter(Mandatory=$true)][string]$ReferenceHash,
  [Parameter(Mandatory=$true)][string]$ReleaseDir
)

$ErrorActionPreference='Stop'
$NewSetup=(Resolve-Path $NewSetup).Path
$OldSetup=(Resolve-Path $OldSetup).Path
$ReferenceHash=$ReferenceHash.ToLowerInvariant()
New-Item -ItemType Directory -Force -Path $ReleaseDir | Out-Null

function Invoke-Setup([string]$Setup,[string[]]$Arguments){
  & $Setup @Arguments | Out-Host
  $code=$LASTEXITCODE
  return $code
}
function Hash-Of([string]$Path){if(!(Test-Path $Path)){return 'missing'};return (Get-FileHash $Path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Assert-True([bool]$Condition,[string]$Message){if(!$Condition){throw $Message}}

$dir=Join-Path $env:LOCALAPPDATA 'Trace'
if(Test-Path $dir){Remove-Item $dir -Recurse -Force}

$dataRoot=Join-Path $env:LOCALAPPDATA 'com.trace.research'
$projectDir=Join-Path $dataRoot 'Projects/ci-v0121-default-path'
$backupDir=Join-Path $dataRoot 'Backups/ci-v0121-default-path'
New-Item -ItemType Directory -Force -Path $projectDir,$backupDir | Out-Null
$project=Join-Path $projectDir 'research-project-must-survive.txt'
$backup=Join-Path $backupDir 'verified-backup-must-survive.txt'
'Default-path project sentinel' | Set-Content $project
'Default-path backup sentinel' | Set-Content $backup

# Install the exact previous release without an explicit path. This exercises
# the same %LOCALAPPDATA%\Trace location seen on the real Windows machine.
$oldExit=Invoke-Setup $OldSetup @('--silent-install')
Assert-True ($oldExit -eq 0) "Default-path v0.12 install failed with exit code $oldExit."
$exe=Join-Path $dir 'Trace.exe'
Assert-True (Test-Path $exe) "Default-path v0.12 Trace.exe was not found at $exe."
$oldHash=Hash-Of $exe

$upgradeExit=Invoke-Setup $NewSetup @('--silent-install')
Assert-True ($upgradeExit -eq 0) "Default-path v0.12 -> v0.12.1 upgrade failed with exit code $upgradeExit."
$upgradedHash=Hash-Of $exe
Assert-True ($upgradedHash -ne $oldHash) 'Default-path upgrade did not replace the v0.12 executable.'
Assert-True ($upgradedHash -eq $ReferenceHash) 'Default-path upgrade does not match exact v0.12.1 reference bytes.'
Assert-True (Test-Path $project) 'Default-path upgrade removed research project data.'
Assert-True (Test-Path $backup) 'Default-path upgrade removed verified backup data.'

# Same-version maintenance at the implicit default path must remain green.
$maintenanceExit=Invoke-Setup $NewSetup @('--silent-install')
Assert-True ($maintenanceExit -eq 0) "Default-path same-version maintenance failed with exit code $maintenanceExit."
$maintainedHash=Hash-Of $exe
Assert-True ($maintainedHash -eq $ReferenceHash) 'Default-path same-version maintenance changed the exact executable bytes.'
Assert-True (Test-Path $project) 'Default-path maintenance removed research project data.'
Assert-True (Test-Path $backup) 'Default-path maintenance removed verified backup data.'

$p=Start-Process -FilePath $exe -WorkingDirectory $dir -PassThru
Start-Sleep -Seconds 10
if($p.HasExited){throw "Default-path upgraded Trace.exe exited unexpectedly with code $($p.ExitCode)."}
Stop-Process -Id $p.Id -Force
Start-Sleep -Seconds 2

$uninstallExit=Invoke-Setup $NewSetup @('--silent-uninstall')
Assert-True ($uninstallExit -eq 0) "Default-path uninstall failed with exit code $uninstallExit."
Start-Sleep -Seconds 3
Assert-True (!(Test-Path $exe)) 'Default-path uninstall left Trace.exe behind.'
Assert-True (Test-Path $project) 'Default-path uninstall removed research project data.'
Assert-True (Test-Path $backup) 'Default-path uninstall removed verified backup data.'

@(
  'Trace 0.12.1 real default-path maintenance verification',
  "default_install_dir=$dir",
  "previous_v012_hash=$oldHash",
  "upgraded_v0121_hash=$upgradedHash",
  "maintained_v0121_hash=$maintainedHash",
  'implicit_default_path_upgrade_green=true',
  'implicit_default_path_same_version_maintenance_green=true',
  'default_path_upgraded_copy_launched=true',
  'default_path_uninstall_green=true',
  'research_project_preserved=true',
  'verified_backup_preserved=true'
) | Set-Content (Join-Path $ReleaseDir 'DEFAULT-PATH-VERIFICATION.txt')
Get-Content (Join-Path $ReleaseDir 'DEFAULT-PATH-VERIFICATION.txt')
