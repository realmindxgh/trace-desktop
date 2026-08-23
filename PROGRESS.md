# Trace Desktop Progress Ledger

This is the live execution ledger for Trace Desktop. Read it after `AGENTS.md`.

- `AGENTS.md` defines the full checklist and acceptance contract.
- `docs/v0121-checklist-status.md` tracks checklist areas.
- `PROGRESS.md` records what has actually happened, with evidence and the exact continuation point.

Any agent making a material change must update this ledger before handoff.

## Current snapshot

**Date:** 2026-08-23  
**Branch:** `trace-v0121`  
**Version:** `0.12.1`  
**Milestone:** Full v0.12.1 UX + Installer Hardening checklist  
**Status:** **FULL CHECKLIST COMPLETION PASS IN PROGRESS**

The previously verified v0.12.1 Windows release is now an **intermediate build**, not the final deliverable, because the user explicitly required every implementable item in `AGENTS.md` to be completed before the final EXE is produced.

The only checklist category that cannot be truthfully completed by CI is physical visual/UAT inspection on the user's own Windows display. Everything else remains in scope for implementation and automated/native verification.

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

That build already proved clean install, installed-copy launch, uninstall preservation, real v0.12 -> v0.12.1 upgrade, and a running-process update scenario. It remains valuable evidence, but it is superseded by the current full-checklist pass.

## Full-checklist implementation tranche: implemented locally, Windows gate pending

The current expanded source is based directly on the exact green source artifact from run `32649590459`. All carried Python/JavaScript research contracts are still green locally after the following additions.

### Code workspace and panel behavior
- persistent left Data rail width
- persistent right Inspector width
- left/right drag resize handles
- collapse/restore controls for both panels
- remembered transcript scroll position per source
- no-source and no-search-match states remain distinct

### Data/import UX
- multi-file import
- drag-and-drop import zone
- visible import queue
- per-file queued/working/success/error/skipped states
- isolated failures so one bad file does not invalidate unrelated valid files
- duplicate-source handling before import
- source originals remain untouched

### Themes / Analyse / Write
- theme evidence inspection from theme cards
- stronger Analyse status and matrix behavior
- sticky matrix headers/identifier column for large matrices
- Write autosave scheduling
- visible save/save-failure status
- improved zero-content guidance

### Search, dialogs and accessibility
- context-aware Ctrl/Cmd+F behavior
- modal focus trapping
- Escape handling where safe
- restored visible keyboard focus treatment
- larger pointer targets
- reduced-motion support
- responsive breakpoints for narrow desktop windows
- residual literal sub-12px meaningful CSS sizes raised to the minimum readability floor

### Installer/maintenance hardening
- preflight detects a running `Trace.exe`
- update is blocked while Trace is running, with save/close/recheck guidance
- target writeability probe
- partial installation detection using executable/uninstaller state
- repair mode for incomplete application installations
- application-file snapshot before update/repair
- rollback helper that excludes `Projects`, `Backups`, and `Installer` research-data areas
- rollback restoration tests for application binaries
- bounded uninstall cleanup verification

### Local verification after this tranche
Green locally:
- application JS syntax
- setup-shell JS syntax
- schema contract
- Office/survey/display regression
- usability regression
- transcription regression
- PDF regression
- v0.12 analysis/intercoder contract
- Cohen kappa mathematics fixture
- existing v0.12.1 hardening contract

Rust compilation of the newest installer changes is **not yet claimed**. It must pass the next Windows source gate.

## Current technical work

The current task is to finish and verify the remaining automated checklist categories:

1. add full-checklist static/regression contract;
2. add research-sized workload/performance contract;
3. standardize search in Themes and Analyse;
4. finish modal/menu viewport handling and save/recovery assertions;
5. add browser-driven layout/visual regression across the required viewport and DPI matrix;
6. add installer browser fixtures for fresh, maintenance, repair, running-app, and error states;
7. refactor branded setup silent verification so CI and GUI share the same core install/uninstall logic;
8. expand Windows maintenance matrix for same-version repair, missing application file, partial metadata, custom path, running-app block/retry, and forced rollback preservation;
9. run a new Windows full-checklist source gate;
10. fix every gate failure;
11. update this ledger and checklist tracker with the exact run/artifact evidence;
12. build a completely new final `TraceSetup.exe` only from that new green checkpoint.

## Release rule

Do **not** hand the prior installer to the user as the final checklist-complete release.

A new final EXE is allowed only after:
- all implementable `AGENTS.md` items are green or concretely verified;
- the expanded Windows maintenance matrix passes;
- browser/DPI/layout regression passes;
- carried research features remain green;
- exact native build/install/upgrade/repair/rollback/uninstall verification passes;
- `docs/v0121-checklist-status.md` and this ledger are updated with final evidence.

## Physical UAT boundary

After the engineering checklist is complete, the final EXE can be produced. The remaining physical-machine visual check must be clearly labeled as physical UAT rather than silently simulated. It should inspect the real installer and Data/Code/Themes/Analyse/Write workspaces at the user's actual Windows scaling.

## Exact next continuation point

Continue from the exact green v0.12.1 source artifact, finish the expanded automated contracts and installer-core refactor, package the source reproducibly into the repo, and launch the new Windows full-checklist gate.
