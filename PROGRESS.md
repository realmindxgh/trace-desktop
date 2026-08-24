# Trace Desktop Progress Ledger

This is the live execution ledger for Trace Desktop. Read it after `AGENTS.md`.

- `AGENTS.md` defines the full checklist and acceptance contract.
- `docs/v0121-checklist-status.md` tracks checklist areas.
- `PROGRESS.md` records what has actually happened, with evidence and the exact continuation point.

Any agent making a material change must update this ledger before handoff.

## Current snapshot

**Date:** 2026-08-24  
**Branch:** `trace-v0121`  
**Version:** `0.12.1`  
**Milestone:** Full v0.12.1 UX + Installer Hardening checklist  
**Status:** **FULL CHECKLIST COMPLETION PASS IN PROGRESS**

The previously verified v0.12.1 Windows release is an **intermediate build**, not the final deliverable. The user requires every implementable item in `AGENTS.md` to be completed before the final EXE is produced.

The only category that cannot be truthfully completed in CI is physical visual/UAT inspection on the user's own Windows display. Everything else remains in scope for implementation and automated/native verification.

## Previously proven intermediate release

Source gate:
- run `32649590459`
- result `success`
- artifact `Trace-v0.12.1-Hardening-Green-Source`
- artifact ID `9495924443`
- artifact digest `95bcb2674b8146214ad17944cc89923f02643f3817ea6549e058e399d8c4e510`

Intermediate Windows release:
- run `32651178336`
- result `success`
- artifact `Trace-v0.12.1-Exact-Verified-Windows-Release`
- artifact ID `9496529233`
- artifact digest `d11cc13472fbd7168d7bd06d231633506624754a88d480daac58306316ec59c0`
- branded installer SHA-256 `8bdd651c64cb787cc0f0d6da3eb5331b0240d8b7c76a5bf8a29a371ad700c4f4`

That build proved clean install, installed-copy launch, uninstall preservation, real v0.12 -> v0.12.1 upgrade, and the earlier running-process update scenario. It remains evidence only and is superseded by the current full-checklist pass.

## Full-checklist implementation currently in source reconstruction

The expanded source is reconstructed from the exact green artifact from run `32649590459`, rather than from an arbitrarily mutated local tree.

Implemented and locally verified additions include:

### Code workspace and panel behavior
- persistent left Data rail width
- persistent right Inspector width
- drag and keyboard resizing with bounded widths
- collapse/restore controls for both panels
- remembered transcript scroll position per source
- distinct no-source and no-search-match states

### Data/import UX
- multi-file import
- visible drag-and-drop import zone
- visible import queue
- per-file queued/working/success/error/skipped results
- isolated failures so one bad file does not invalidate unrelated files
- duplicate-source handling before import
- source originals remain untouched

### Themes / Analyse / Write
- searchable Themes workspace
- searchable Analyse evidence
- `buildAnalysisIndex()` for large-project summary/matrix work
- theme evidence inspection
- sticky matrix headers and identifier column
- bounded evidence results
- Write autosave scheduling
- visible save and save-failure state
- improved zero-content guidance

### Search, dialogs and accessibility
- context-aware Ctrl/Cmd+F
- modal focus trapping
- Escape handling where safe
- visible keyboard focus
- keyboard-accessible splitters
- larger pointer targets
- reduced-motion support
- responsive breakpoints
- literal meaningful CSS sizes below 12 px raised to the readability floor

### Installer/maintenance hardening
- running `Trace.exe` detection
- update blocked while Trace is running, with save/close/recheck guidance
- target writeability probe
- partial-install detection
- installed-version detection
- repair mode
- application-file snapshot before update/repair
- rollback helper excluding `Projects`, `Backups`, and `Installer`
- deterministic forced-rollback CI hook
- shared `perform_install` / `perform_uninstall` core so interactive GUI and silent verification do not prove separate installer paths
- rollback restoration and data-exclusion unit tests
- bounded uninstall cleanup verification

### Expanded local contracts
Green locally before the current Windows rerun:
- application JS syntax
- setup-shell JS syntax
- schema contract
- Office/survey/display regression
- usability regression
- transcription regression
- PDF regression
- v0.12 analysis/intercoder regression
- Cohen kappa mathematics
- original v0.12.1 hardening contract
- new `v0121_full_checklist.py`
- 10,000-coding-reference workload/indexing test
- root frontend build
- setup-shell frontend build

Rust compilation of the newest installer core remains a Windows-gate claim only.

## First full-checklist Windows gate

Run `32665034064` / job `97257005294` completed with **failure**.

What passed:
- exact previous green source retrieval
- reconstruction bundle integrity
- reconstruction execution
- application/setup JS syntax
- carried schema/import/usability/transcription/PDF/analysis/intercoder/kappa regressions
- original v0.12.1 hardening contract

What failed:
- new full-checklist contract reported missing `themeSearch`
- workload contract reported missing `buildAnalysisIndex`

The failure identified a **reconstruction packaging gap**, not a carried research regression. The later local changes existed outside the canonical transformation and therefore were correctly rejected by CI. Frontend builds, browser/DPI tests, Rust tests and artifact promotion were skipped after the contract failure.

The run's failure is preserved in `build-status/v0121-full-checklist-gate.txt`; it is not hidden or overwritten as success.

## Correction after run 32665034064

A once-only readable finalizer was created and committed as:

- `ci/v0121_finalize_full_checklist.py`
- SHA-256 `e43aba18ced41485e3303a14f40d5fefe8cb9a4b903732b7214d097896a3d0ca`
- source commit `b04b05b2453b05f934a3afda6242939dfb958d38`

It closes the missing canonical reconstruction gaps, including Themes/Analyse search, indexed analysis, Data drop-zone rendering, accessibility/responsive CSS, setup browser fixtures, installed-version reporting, shared setup core, and deterministic rollback verification.

The Windows gate was updated at commit `aa8c4ea7492b629da8c4e526472bfa76eefbf6d0` to:
- enforce the finalizer SHA before execution;
- run the finalizer after the two original reconstruction transforms;
- fail immediately on the first individual source/regression contract failure;
- continue to require both frontend builds, browser viewport/DPI matrix, main Rust tests, and setup repair/rollback Rust tests before source promotion.

A replacement Windows full-checklist gate is now the active checkpoint.

## Release rule

Do **not** hand the prior installer to the user as the final checklist-complete release.

A new final EXE is allowed only after:
- all implementable `AGENTS.md` items are green or concretely verified;
- the full Windows source/checklist gate is green;
- browser/DPI/layout regression passes;
- the expanded Windows maintenance matrix passes;
- carried research features remain green;
- exact native build/install/upgrade/repair/rollback/uninstall verification passes;
- `docs/v0121-checklist-status.md` and this ledger contain the final evidence.

## Physical UAT boundary

After engineering completion, the final EXE can be produced. Physical visual inspection on the user's actual Windows display must remain labeled **PHYSICAL UAT** rather than being simulated or falsely checked off.

## Exact next continuation point

Follow the replacement full-checklist Windows gate triggered from `aa8c4ea7492b629da8c4e526472bfa76eefbf6d0`. Fix any frontend/browser/Rust failure it exposes. Once that gate is green, record its artifact/run evidence here and move directly to the expanded exact-installer maintenance matrix and final Windows release build.
