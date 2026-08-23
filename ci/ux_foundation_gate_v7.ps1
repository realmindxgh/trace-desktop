$ErrorActionPreference='Stop'
$basePath='ci/ux_foundation_gate_v6.ps1'
if(!(Test-Path $basePath)){ throw 'Phase 5 UX gate is missing.' }
$base=Get-Content $basePath -Raw

$phase5Line="Apply-TraceOverlay -PartsPath 'bootstrap/v011ux6' -ExpectedParts 11 -ExpectedBase64Length 20888 -ExpectedXzSha256 'f8ed9be2b5b35edbacf7c699e9ff6e8ea7cf03d6987a471d1c30c59f6d0c71cb' -ExpectedPatchSha256 'f05643fb05119b404aa0bbf50b0462084fb137f7a07d9037071f16a3b46abfb4' -Label 'UX-Foundation-Phase-5'"
if(!$base.Contains($phase5Line)){ throw 'Could not locate Phase 5 overlay insertion point.' }
$phase6Line="Apply-TraceOverlay -PartsPath 'bootstrap/v011ux7' -ExpectedParts 4 -ExpectedBase64Length 57136 -ExpectedXzSha256 '8e86896217991e4e4d27bdeaaf09ac8c5b9b809116046b5cf3f8e1f1a5d7afaa' -ExpectedPatchSha256 '34acbc98206ce574e66cc259e24d8785de0980264fcd22bb6f79664b77d2059a' -Label 'UX-Foundation-Phase-6'"
$base=$base.Replace($phase5Line,$phase5Line+"`r`n`r`n# Phase 6: project persistence, contextual AI, safety, recovery, compatibility and large-project behavior.`r`n"+$phase6Line)

$phase5TestMarker="if(`$LASTEXITCODE -ne 0){ throw 'Phase 5 dynamic Import/Settings/Productivity logic failed.' }"
if(!$base.Contains($phase5TestMarker)){ throw 'Could not locate Phase 6 dynamic-test insertion point.' }
$phase6Test="node tests/phase6_logic.js`r`nif(`$LASTEXITCODE -ne 0){ throw 'Phase 6 project safety/recovery logic failed.' }"
$base=$base.Replace($phase5TestMarker,$phase5TestMarker+"`r`n"+$phase6Test)

$phase5Guard="if(`$app.Contains(\"imported.participants=clone(defaults.participants).slice(0,1)\")){throw 'Phase 5 phantom REFI participant fallback returned.'}"
if(!$base.Contains($phase5Guard)){ throw 'Could not locate Phase 6 source-contract insertion point.' }
$phase6Checks=@'
foreach($required in @('openTraceAssistantStatus','confirmResearchAction','openRecoveryCenter','openRecoveryDetails','openProjectSettings','sourceRenderLimit','participantRenderLimit','update_project_details','project_compatibility_status','aria-current="page"','skip-link')){
    if(!$app.Contains($required)){ throw "Phase 6 frontend contract missing: $required" }
}
foreach($required in @('trace-ai-modal','confirmation-modal','recovery-center-modal','project-compatibility','skip-link','large-project-more')){
    if(!$css.Contains($required)){ throw "Phase 6 style contract missing: $required" }
}
$models=Get-Content src-tauri/src/models.rs -Raw
$db=Get-Content src-tauri/src/db.rs -Raw
$lib=Get-Content src-tauri/src/lib.rs -Raw
foreach($required in @('UpdateProjectInput','ProjectCompatibilityStatus','ai_scope')){if(!$models.Contains($required)){throw "Phase 6 native model missing: $required"}}
foreach($required in @('update_project_details','project_compatibility_status','research_question_records')){if(!$db.Contains($required)){throw "Phase 6 native database contract missing: $required"}}
foreach($required in @('update_project_details','project_compatibility_status')){if(!$lib.Contains($required)){throw "Phase 6 native command registration missing: $required"}}
if($app.Contains('confirm(')){throw 'Raw browser confirm() returned to the production UX.'}
'@
$base=$base.Replace($phase5Guard,$phase5Guard+"`r`n"+$phase6Checks)

if(!$base.Contains('ux_foundation_contract_checks=102')){ throw 'Could not locate UX contract receipt count.' }
$phase6Receipt="phase6_patch_sha256=34acbc98206ce574e66cc259e24d8785de0980264fcd22bb6f79664b77d2059a`r`nphase6_xz_sha256=8e86896217991e4e4d27bdeaaf09ac8c5b9b809116046b5cf3f8e1f1a5d7afaa`r`nphase6_logic_green=true`r`nux_foundation_contract_checks=131"
$base=$base.Replace('ux_foundation_contract_checks=102',$phase6Receipt)
$base=$base.Replace("trace-ux-foundation-expanded-v6.ps1","trace-ux-foundation-expanded-v7.ps1")
$base=$base.Replace("Expanded Phase 5 Windows gate failed.","Expanded Phase 6 Windows gate failed.")

$expanded=Join-Path $env:RUNNER_TEMP 'trace-ux-foundation-driver-v7.ps1'
Set-Content $expanded $base
& pwsh -NoProfile -File $expanded
if($LASTEXITCODE -ne 0){ throw 'Expanded Phase 6 Windows gate failed.' }

& pwsh -NoProfile -File 'ci/phase6_browser_gate.ps1'
if($LASTEXITCODE -ne 0){ throw 'Phase 6 Windows Edge visual gate failed.' }
