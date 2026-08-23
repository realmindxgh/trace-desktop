$ErrorActionPreference='Stop'

$basePath='ci/ux_foundation_gate_v3.ps1'
if(!(Test-Path $basePath)){ throw 'Phase 2 UX gate is missing.' }
$base=Get-Content $basePath -Raw

$phase3=@'
# Phase 3: hierarchical codebook, evidence-led theme development and review workflows.
Apply-TraceOverlay -PartsPath 'bootstrap/v011ux4' -ExpectedParts 7 -ExpectedBase64Length 29884 -ExpectedXzSha256 '33776b10bed121116c321c1e3a7639c6de3fc80b5d59395c80c19479b2dd9fea' -ExpectedPatchSha256 '0b61b70a4bd676518b59500090ea2a9cd77a48a37564f55682ac9da2a8eb4b0b' -Label 'UX-Foundation-Phase-3'
'@
$workMarker='$work=Join-Path $source ''work'''
if(!$base.Contains($workMarker)){ throw 'Could not locate Phase 3 overlay insertion point.' }
$base=$base.Replace($workMarker,$phase3+"`r`n"+$workMarker)

$phase3Checks=@'
node tests/phase3_logic.js
if($LASTEXITCODE -ne 0){ throw 'Phase 3 dynamic Codes/Themes logic failed.' }
$app=Get-Content src/app.js -Raw
$css=Get-Content src/styles.css -Raw
foreach($required in @('codeDescendantIds','codeEvidenceStats','themeEvidenceStats','visibleCodeSet','renderCodebookRows','renderThemeCard','openCodeReview','openThemeReview','ce-parent')){
    if(!$app.Contains($required)){ throw "Phase 3 source contract missing: $required" }
}
foreach($required in @('themes-workbench','codebook-tree','theme-evidence-metrics','evidence-review-modal','code-editor-modal')){
    if(!$css.Contains($required)){ throw "Phase 3 style contract missing: $required" }
}
'@
$phase2Marker='# Ensure the Phase 2 organiser contracts are present in the built source before packaging.'
if(!$base.Contains($phase2Marker)){ throw 'Could not locate Phase 3 contract insertion point.' }
$base=$base.Replace($phase2Marker,$phase3Checks+"`r`n"+$phase2Marker)

$receiptMarker='phase2_xz_sha256=f8f1432d16e4314cbaed9c7ae30657e8227a419ccd60f82f51a724003757f24e'
if(!$base.Contains($receiptMarker)){ throw 'Could not locate verification receipt insertion point.' }
$base=$base.Replace($receiptMarker,$receiptMarker+"`r`nphase3_patch_sha256=0b61b70a4bd676518b59500090ea2a9cd77a48a37564f55682ac9da2a8eb4b0b`r`nphase3_xz_sha256=33776b10bed121116c321c1e3a7639c6de3fc80b5d59395c80c19479b2dd9fea`r`nphase3_logic_green=true")

$expanded=Join-Path $env:RUNNER_TEMP 'trace-ux-foundation-expanded-v4.ps1'
Set-Content $expanded $base
& pwsh -NoProfile -File $expanded
if($LASTEXITCODE -ne 0){ throw 'Expanded Phase 3 Windows gate failed.' }

& pwsh -NoProfile -File 'ci/phase3_browser_gate.ps1'
if($LASTEXITCODE -ne 0){ throw 'Phase 3 Windows Edge visual gate failed.' }
