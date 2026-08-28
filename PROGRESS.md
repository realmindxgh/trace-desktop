# Trace Desktop Progress Ledger

This is the live execution ledger for Trace Desktop. Read it after `AGENTS.md`.

- `AGENTS.md` is the authoritative **240-point Trace UX Foundation master contract**.
- `docs/TRACE_UX_FOUNDATION_CLOSURE.md` is the item-by-item closure ledger.
- `docs/TRACE_DESIGN_SYSTEM.md` is the normative UI system.
- `docs/v0121-checklist-status.md` and the historical section below preserve the verified v0.12.1 engineering baseline.

Any agent making a material change must update this ledger before handoff.

## Current snapshot

**Date:** 2026-08-28  
**Active branch:** `trace-ux-foundation-v2`  
**Verified engineering baseline:** `0.12.1`  
**Current milestone:** Trace UX Foundation final acceptance  
**Status:** **STRICT UX SOURCE GREEN; WINDOWS INSTALLED ACCEPTANCE IN PROGRESS; PHYSICAL UAT PENDING**

The application-shell redesign and automated source-side implementation of the 240-point contract are at the acceptance boundary. Do not restart Phase 1. Do not use the older v0.12.1 hardening checklist as the current definition of done.

The current finish line is:

`strict green UX source -> installed Windows acceptance -> physical real-machine UAT -> final closure/promotion`

## Exact current UX source candidate

Strict source gate:

- workflow: `Trace UX Foundation v2 gate`
- run: `33152414998`
- result: `success`
- source/control SHA: `69b5f788f6b5723140efcc1e9fe970191e2225a3`
- artifact: `Trace-UX-Foundation-v2-Green-Source`
- artifact digest: `sha256:510adf1546f00b5160ed530adfa57d51c14b01eaf945776e6b7db732c7104787`

Run `33152414998` proved:

- deterministic reconstruction from the exact verified v0.12.1 source baseline
- Trace UX Foundation static contract
- schema contract
- Office/survey imports
- coding/usability regressions
- local transcription regressions
- PDF text regressions
- analysis/intercoder regressions and mathematics
- v0.12.1 hardening/full-checklist contracts
- 500-source / 10,000-reference workload contract
- both frontend builds
- full browser researcher journey
- truthful zero/populated-state checks
- trust/error/destructive-action checks
- responsive/DPI/layout gates
- strict reviewed visual-regression baseline
- native Trace Rust compile/tests
- setup-shell Rust compile/tests

This is the only source artifact currently eligible for Windows acceptance unless superseded by a later fully green strict source run.

## Reviewed visual baseline

The corrected eight-screen visual candidate was manually reviewed from run `33117906540` after fixing the stale `24407h ago` timestamp presentation.

Reviewed visual artifact digest:

`sha256:20bf964fef8ab8721d5d89c0b2b0d77c3781bb9ec1712bd5effcef6eb2c63e93`

The strict source gate now compares deterministic screenshots against that reviewed baseline rather than silently regenerating it.

Required screens include:

- Home
- empty Project Overview
- Data
- Code with visible coding
- Themes
- Analyse
- Write
- Code at 1366x768 / 125% scaling

Structural checks also cover font floor, root overflow, pane visibility and source-identity/document-tab collision.

## Windows installed acceptance

Current workflow:

- workflow: `Trace UX Foundation Windows acceptance`
- run: `33154626340`
- run number: `2`
- release-control SHA: `e312fea034f42af9ddc84a6d21a4837a4171f008`
- source pointer: run `33152414998`
- status at this ledger update: `IN PROGRESS`

Already green in the Windows acceptance run:

- exact source pointer and artifact digest resolution
- exact green source download
- exact historical v0.12 installer download for upgrade/maintenance comparison
- Node/Python/Rust setup
- full research + UX source-contract replay
- both frontend builds
- browser researcher journey
- strict visual evidence
- viewport/DPI replay
- branded setup verification CLI staging

Current long-running stage at this ledger update:

- native Tauri release bundle build

Still to run in the same Windows acceptance lane:

1. stage native NSIS payload and build branded `TraceSetup.exe`
2. establish exact installed native reference/hash
3. install the branded candidate
4. attach Playwright over CDP to the actual installed Tauri/WebView2 application
5. verify fresh Home/no fixture/no phantom participant
6. execute real TXT/XLSX/PDF/WAV research workflow
7. create/apply code, memo, theme, Analyse and Write findings
8. close/relaunch and prove persistence
9. export findings
10. create a verified backup and restore it as a new project
11. run branded maintenance/update/repair matrix
12. run rollback verification
13. upload installed evidence and the Windows acceptance build

Do not call the Windows build green until all of those stages succeed.

## 240-point closure ledger

`docs/TRACE_UX_FOUNDATION_CLOSURE.md` was created as the explicit 1–240 acceptance receipt.

It separates:

- `S`: strict source evidence
- `V`: reviewed visual evidence
- `L`: large-project evidence
- `R`: carried research/data-preservation evidence
- `W`: installed Windows acceptance still required
- `P`: physical real-machine UAT still required
- `RESOLVED`: intentionally conditional/not-literal product resolution

Do not write `240/240 COMPLETE` while any required `W` or `P` boundary remains.

## Physical real-machine UAT

GitHub issue #5 is now titled:

`Trace UX Foundation final physical UAT`

It supersedes its original narrower v0.12.1-only purpose and now tracks final human-machine acceptance of the 240-point contract.

After Windows acceptance turns green, update issue #5 with:

- exact Windows acceptance run
- artifact name/digest
- exact `TraceSetup.exe` SHA-256

Then test only that exact build on the real Windows machine.

Physical UAT covers:

- installer readability at actual Windows scaling
- first-launch comprehension and truthful state
- Home
- Data / Code / Themes / Analyse / Write
- shell, panes, tabs and inspector behaviour
- real transcript/XLSX/PDF/media use
- coding/memos/themes/analysis/writing/export
- close/reopen persistence
- backup/restore
- keyboard/focus/accessibility
- errors and destructive-action clarity
- maintenance/recovery where practical

Any physical-UAT defect must be fixed and the affected automated gates rerun before final closure.

## UX Foundation implementation summary

The active branch now includes, among other work:

- deliberate Trace Home and first-launch experience
- production-state hygiene and phantom-participant fixes
- recent projects, recovery and optional Getting Started
- short New Project flow and Project Overview
- permanent left navigation rail
- contextual Data/Code/Themes/Analyse/Write panes
- Sources / Participants-Cases / Attributes / Collections-Sets / Imports IA
- document/source tabs and source identity strip
- contextual shared inspector, resize/collapse and layout memory
- separate Project Settings and Application Settings
- Compact / Comfortable / Large interface sizing
- contextual Trace AI
- command palette and keyboard shortcuts
- contextual search
- reusable keyboard-accessible context menus
- distinct layout-memory vs exact-workspace-resume preferences
- first-class media transcription workflow
- aggregate import summaries and next actions
- human/actionable error dialogs with technical-detail disclosure
- destructive-action consequence previews
- stable save-state presentation
- formal Trace design system
- strict perceptual visual regression
- realistic installed-app acceptance scripts
- real TXT/XLSX/PDF/WAV acceptance fixtures
- findings export + verified backup/restore installed test
- Windows maintenance/rollback acceptance lane

The research engine underneath remains protected by the full carried regression suite.

## CI hygiene

The obsolete one-shot `.github/workflows/v0121-wire-layout-fix.yml` was retired from `trace-ux-foundation-v2` at commit `67f82797b81a2337cd91bc0e3b3782d35c3fdc9f`.

That workflow was historical v0.12.1 wiring machinery, not a product test, and was producing meaningless red noise on UX branch commits. The historical `trace-v0121` branch was not altered.

## Historical v0.12.1 engineering baseline

The final pre-UX v0.12.1 engineering verification remains valid and must not be discarded.

Final full-checklist source gate:

- run `32723424461`
- source SHA `a5bdc5335264db679d8cc98abac5b73a18effb3d`
- artifact `Trace-v0.12.1-Full-Checklist-Green-Source`
- digest `sha256:dad38e53e5149190d97c65762cb4362accc84467f38c1b59c2aa97216cca123e`

Final exact Windows v0.12.1 release verification:

- run `32724433832`
- artifact `Trace-v0.12.1-Exact-Verified-Windows-Release`
- artifact digest `sha256:233e76f199eb711f1de4fa02cc9cf95bdc3062e46e40cffa7239f06c921472f9`
- `TraceSetup.exe` SHA-256 `262186eea6ca1dc70c267ac81278cd0f77960e4a7525cc62b0d8ffbaeb0ba77d`

That verified clean install, launch, uninstall, v0.12 -> v0.12.1 upgrade, running-process safety, repair, missing-uninstaller recovery, custom paths, rollback, research-project preservation, verified-backup preservation and version consistency.

The UX Foundation preserves and reruns those research/data-safety contracts while replacing the application shell.

## Exact continuation point

Do **not** begin a new UX phase.

Continue with Windows acceptance run `33154626340`.

If it fails:

1. read the exact failing step/log,
2. classify it as product, installed-app test, installer, or acceptance-infrastructure defect,
3. fix the real defect without weakening an existing research/visual/data-preservation contract,
4. if the green source artifact itself changes, run a new strict source gate before repointing Windows acceptance,
5. rerun Windows acceptance from the exact eligible artifact.

If it succeeds:

1. record the exact Windows artifact names/digests and `TraceSetup.exe` SHA-256,
2. update `docs/TRACE_UX_FOUNDATION_CLOSURE.md` to close the `W` boundary,
3. update issue #5 with the exact build to physically test,
4. perform physical real-machine UAT,
5. fix/retest any physical defect,
6. only then mark the 240-point Trace UX Foundation complete and consider promotion to `main` / final release acceptance.
