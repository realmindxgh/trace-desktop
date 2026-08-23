$ErrorActionPreference='Stop'

$basePath='ci/ux_foundation_gate_v3.ps1'
if(!(Test-Path $basePath)){ throw 'Phase 2 UX gate is missing.' }
$base=Get-Content $basePath -Raw

$advancedPhases=@'
# Phase 3: hierarchical codebook, evidence-led theme development and review workflows.
Apply-TraceOverlay -PartsPath 'bootstrap/v011ux4' -ExpectedParts 7 -ExpectedBase64Length 29884 -ExpectedXzSha256 '33776b10bed121116c321c1e3a7639c6de3fc80b5d59395c80c19479b2dd9fea' -ExpectedPatchSha256 '0b61b70a4bd676518b59500090ea2a9cd77a48a37564f55682ac9da2a8eb4b0b' -Label 'UX-Foundation-Phase-3'

# Phase 4: evidence-led analysis and findings writing workbenches.
Apply-TraceOverlay -PartsPath 'bootstrap/v011ux5' -ExpectedParts 8 -ExpectedBase64Length 15840 -ExpectedXzSha256 'f8129cea9f12efef9977e14c3d038704103691e457acd671698d6f0194d99028' -ExpectedPatchSha256 '4ec781b1c2648768ce2372834ff4d73f44a7a2d4d1979162acd07ce241f502f3' -Label 'UX-Foundation-Phase-4'

# Phase 5: guided import, processing/error feedback, settings, accessibility and keyboard productivity.
Apply-TraceOverlay -PartsPath 'bootstrap/v011ux6' -ExpectedParts 11 -ExpectedBase64Length 20888 -ExpectedXzSha256 'f8ed9be2b5b35edbacf7c699e9ff6e8ea7cf03d6987a471d1c30c59f6d0c71cb' -ExpectedPatchSha256 'f05643fb05119b404aa0bbf50b0462084fb137f7a07d9037071f16a3b46abfb4' -Label 'UX-Foundation-Phase-5'
'@
$workMarker='$work=Join-Path $source ''work'''
if(!$base.Contains($workMarker)){ throw 'Could not locate advanced UX overlay insertion point.' }
$base=$base.Replace($workMarker,$advancedPhases+"`r`n"+$workMarker)

$advancedChecks=@'
node tests/phase3_logic.js
if($LASTEXITCODE -ne 0){ throw 'Phase 3 dynamic Codes/Themes logic failed.' }
node tests/phase4_logic.js
if($LASTEXITCODE -ne 0){ throw 'Phase 4 dynamic Analyse/Write logic failed.' }
node tests/phase5_logic.js
if($LASTEXITCODE -ne 0){ throw 'Phase 5 dynamic Import/Settings/Productivity logic failed.' }
$app=Get-Content src/app.js -Raw
$css=Get-Content src/styles.css -Raw
foreach($required in @('codeDescendantIds','codeEvidenceStats','themeEvidenceStats','visibleCodeSet','renderCodebookRows','renderThemeCard','openCodeReview','openThemeReview','ce-parent')){
    if(!$app.Contains($required)){ throw "Phase 3 source contract missing: $required" }
}
foreach($required in @('themes-workbench','codebook-tree','theme-evidence-metrics','evidence-review-modal','code-editor-modal')){
    if(!$css.Contains($required)){ throw "Phase 3 style contract missing: $required" }
}
foreach($required in @('analysisRefs','analysisCellCount','writeTargets','writeEvidenceCandidates','analysisParticipantFilter','analysis-search','write-evidence-search','data-analysis-cell')){
    if(!$app.Contains($required)){ throw "Phase 4 source contract missing: $required" }
}
foreach($required in @('phase4-analysis','analysis-command-bar','analysis-filter-bar','analysis-workbench','phase4-write','writing-workbench','phase4-evidence')){
    if(!$css.Contains($required)){ throw "Phase 4 style contract missing: $required" }
}
foreach($required in @('IMPORT_GROUPS','chooseImportFile','openImporter','reportError','beginOperation','offerMediaNextStep','commandActions','openKeyboardShortcuts','id="file-import"','reducedMotion','Version information unavailable')){
    if(!$app.Contains($required)){ throw "Phase 5 source contract missing: $required" }
}
foreach($required in @('import-hub-modal','operation-toast','error-dialog','shortcut-list','data-reduced-motion',':focus-visible')){
    if(!$css.Contains($required)){ throw "Phase 5 style contract missing: $required" }
}
if($app.Contains("imported.participants=clone(defaults.participants).slice(0,1)")){throw 'Phase 5 phantom REFI participant fallback returned.'}
'@
$phase2Marker='# Ensure the Phase 2 organiser contracts are present in the built source before packaging.'
if(!$base.Contains($phase2Marker)){ throw 'Could not locate advanced UX contract insertion point.' }
$base=$base.Replace($phase2Marker,$advancedChecks+"`r`n"+$phase2Marker)

$receiptMarker='phase2_xz_sha256=f8f1432d16e4314cbaed9c7ae30657e8227a419ccd60f82f51a724003757f24e'
if(!$base.Contains($receiptMarker)){ throw 'Could not locate verification receipt insertion point.' }
$receipt=$receiptMarker+"`r`nphase3_patch_sha256=0b61b70a4bd676518b59500090ea2a9cd77a48a37564f55682ac9da2a8eb4b0b`r`nphase3_xz_sha256=33776b10bed121116c321c1e3a7639c6de3fc80b5d59395c80c19479b2dd9fea`r`nphase3_logic_green=true`r`nphase4_patch_sha256=4ec781b1c2648768ce2372834ff4d73f44a7a2d4d1979162acd07ce241f502f3`r`nphase4_xz_sha256=f8129cea9f12efef9977e14c3d038704103691e457acd671698d6f0194d99028`r`nphase4_logic_green=true`r`nphase5_patch_sha256=f05643fb05119b404aa0bbf50b0462084fb137f7a07d9037071f16a3b46abfb4`r`nphase5_xz_sha256=f8ed9be2b5b35edbacf7c699e9ff6e8ea7cf03d6987a471d1c30c59f6d0c71cb`r`nphase5_logic_green=true`r`nux_foundation_contract_checks=102"
$base=$base.Replace($receiptMarker,$receipt)

$expanded=Join-Path $env:RUNNER_TEMP 'trace-ux-foundation-expanded-v6.ps1'
Set-Content $expanded $base
& pwsh -NoProfile -File $expanded
if($LASTEXITCODE -ne 0){ throw 'Expanded Phase 5 Windows gate failed.' }

& pwsh -NoProfile -File 'ci/phase3_browser_gate.ps1'
if($LASTEXITCODE -ne 0){ throw 'Phase 3 Windows Edge visual gate failed.' }
& pwsh -NoProfile -File 'ci/phase4_browser_gate.ps1'
if($LASTEXITCODE -ne 0){ throw 'Phase 4 Windows Edge visual gate failed.' }
& pwsh -NoProfile -File 'ci/phase5_browser_gate.ps1'
if($LASTEXITCODE -ne 0){ throw 'Phase 5 Windows Edge visual gate failed.' }
