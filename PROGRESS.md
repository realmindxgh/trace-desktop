# Trace Desktop Progress Ledger

This is the live execution ledger for Trace Desktop. Read it after `AGENTS.md`.

- `AGENTS.md` is now the **240-point Trace UX Foundation master product and execution contract**.
- `docs/v0121-checklist-status.md` records the completed v0.12.1 engineering-hardening checklist.
- `PROGRESS.md` records what has actually happened, with evidence and the exact continuation point.

Any agent making a material change must update this ledger before handoff.

## Current snapshot

**Date:** 2026-08-27  
**Branch:** `main`  
**Verified engineering baseline:** `0.12.1`  
**Current milestone:** Trace UX Foundation  
**Status:** **v0.12.1 ENGINEERING BASELINE VERIFIED; 240-POINT UX FOUNDATION CONTRACT ACTIVE**

The final v0.12.1 Windows engineering verification remains valid. The exact final-v2 release artifact came from run `32724433832`.

However, the v0.12.1 hardening checklist is no longer the full product definition of done. On 2026-08-27 the complete 240-point Trace UX/UI master backlog was promoted into `AGENTS.md` as the authoritative UX Foundation contract. That contract explicitly permits rebuilding the application shell and information architecture while preserving the working research engine.

The previous statement that only physical UAT remained applied to the narrower v0.12.1 engineering-hardening checklist. Under the new master contract, substantial UX Foundation work remains before the product UX can be called complete.

## Contract transition

Commit `cd69e2246bce0de0d76505f4701e2855e0766b27` replaced the old hardening-only `AGENTS.md` mission with the 240-point Trace UX Foundation master contract.

The new contract establishes these eight phases:

1. production-state hygiene, Home and first launch
2. navigation architecture and the context-pane/workspace/inspector shell
3. typography, spacing, component design and responsive behaviour
4. Data/import/source/participant workflows
5. Code, Themes, Analyse and Write within the shared shell
6. contextual Trace AI
7. keyboard productivity, command palette, accessibility and advanced interaction polish
8. visual and first-launch regression gates in the Windows release pipeline

The target desktop shell is now:

`Navigation rail | Context pane | Main workspace | Inspector`

The existing Data -> Code -> Themes -> Analyse -> Write research model remains the conceptual backbone, but the old giant floating bottom dock is not a protected architectural requirement.

The master completion rule now requires the real end-to-end researcher journey to be exercised:

`create project -> import data -> organise participants -> code passages -> create notes/memos -> build themes -> analyse -> write/export -> close -> reopen -> recover/backup`

## Main-branch promotion

On 2026-08-27, `main` was fast-forwarded from the stale pre-v0.12 line to the verified v0.12.1 lineage. A normal clone of the default branch now receives the v0.12.1 engineering baseline rather than the older snapshot.

The promotion triggered an old v0.10 status workflow on `main`; its status-recording commit is historical CI bookkeeping and does not redefine the verified v0.12.1 release evidence below.

## Physical UAT tracking

GitHub issue #5, `v0.12.1 final physical UAT`, tracks the real-machine acceptance work that could not be truthfully substituted by CI.

That issue remains useful as validation of the v0.12.1 baseline, but closing it alone will not close the 240-point UX Foundation contract.

## Previously proven intermediate release

Source gate:
- run `32649590459`
- result `success`
- artifact `Trace-v0.12.1-Hardening-Green-Source`

Intermediate Windows release:
- run `32651178336`
- result `success`
- artifact `Trace-v0.12.1-Exact-Verified-Windows-Release`
- branded installer SHA-256 `8bdd651c64cb787cc0f0d6da3eb5331b0240d8b7c76a5bf8a29a371ad700c4f4`

That build proved clean install, installed-copy launch, uninstall preservation, real v0.12 -> v0.12.1 upgrade, and a running-process update scenario. It is superseded by the final-v2 release below.

## Expanded v0.12.1 full-checklist implementation

The expanded source was reconstructed from the exact green v0.12.1 source artifact from run `32649590459`, then received the committed full-checklist and installer-hardening transforms.

Implemented areas include:
- persistent/resizable/collapsible Data and Inspector rails
- remembered transcript scroll position per source
- multi-file import, drag-and-drop, import queue, isolated failure states, duplicate handling
- theme evidence inspection
- stronger Analyse matrix behavior and sticky identifiers
- Write autosave and save-state feedback
- context-aware search behavior
- modal focus trapping and Escape handling
- visible keyboard focus and larger targets
- reduced-motion and responsive desktop breakpoints
- typography readability floor
- running-app installer preflight
- writeability/partial-install checks
- repair mode
- application-file snapshot and rollback helpers that exclude research-data areas

These remain valuable foundations but should not be mistaken for completion of the new shell and information-architecture requirements in `AGENTS.md`.

## Full-checklist Windows gate history

### Run `32698021215`
- source reconstruction completed
- first failing carried contract was `v11_usability.py`
- cause: duplicated insertion in the generated `renderThemes()` / `buildAnalysisIndex()` source
- action: corrected the once-only finalizer logic

### Run `32698173746`
- stopped in reconstruction before tests
- cause: portable text-file SHA check disagreed after Windows CRLF checkout normalization
- action: replaced the checkout-byte integrity assumption

### Run `32698269359`
- stopped in reconstruction before tests
- cause: the large plaintext finalizer blob had been corrupted during transport
- action: removed plaintext finalizer transport and moved to a binary-safe compressed finalizer bundle

### Run `32698675246`
This was the first successful exact reconstruction using the binary-safe finalizer path.

Green in this run:
- exact v0.12.1 base source download
- exact base reconstruction bundle SHA verification
- exact finalizer compressed/raw SHA verification
- application JavaScript syntax
- setup-shell JavaScript syntax
- v0.12 intercoder mathematics
- schema contract
- Office/survey/display regression
- usability regression
- transcription regression
- PDF regression
- v0.12 analysis/intercoder regression
- original v0.12.1 hardening contract
- expanded full-checklist static contract
- 10,000-reference / 500-source workload contract (`5.2ms` in CI)
- Trace frontend build
- Trace Setup frontend build

First failure:
- browser viewport/DPI matrix
- Playwright timed out waiting for `[data-section="Data"]`

Root cause:
- the new accessibility `MutationObserver` tried to observe `#modal-root` before the first application render had created that node
- the resulting runtime exception prevented the UI from rendering, so the browser test never reached a layout assertion

Correction:
- the finalizer now attaches the observer to the already-existing application host instead
- the corrected finalizer was regenerated from a clean source and validated as once-only/syntax-clean
- corrected raw finalizer: `32665` bytes, SHA-256 `ddda44167b37b0f090552885901031d67fcb8feca08cb2effa42fa3b9df631ef`
- corrected compressed finalizer: `9288` bytes, SHA-256 `5f26a74248f9b7a8147f9c5f4922156bb36c5bebbd4f1c866780d0dce0ac1389`

## Final full-checklist source gate

Run `32723424461` completed successfully from source SHA `a5bdc5335264db679d8cc98abac5b73a18effb3d`.

The green source gate proved:
- all carried research and regression contracts
- both frontends
- the browser viewport/DPI matrix
- native Rust compilation and unit tests
- the NSIS custom-path raw-argument fix

The exact source artifact was `Trace-v0.12.1-Full-Checklist-Green-Source` with digest `sha256:dad38e53e5149190d97c65762cb4362accc84467f38c1b59c2aa97216cca123e`.

## Final Windows release verification

Run `32724433832` completed successfully as `Trace Windows v0.12.1 exact final v2`.

Final artifact:
- `Trace-v0.12.1-Exact-Verified-Windows-Release`
- artifact SHA-256 `233e76f199eb711f1de4fa02cc9cf95bdc3062e46e40cffa7239f06c921472f9`
- artifact expires `2026-09-23`
- final `TraceSetup.exe` SHA-256 `262186eea6ca1dc70c267ac81278cd0f77960e4a7525cc62b0d8ffbaeb0ba77d`

The final-v2 workflow passed all of these gates:
- exact full-checklist source reconstruction
- carried research contracts
- native Trace compile and tests
- setup-shell compile and tests
- generated native NSIS payload equivalence
- exact branded clean installation
- installed executable hash equivalence with the native reference
- installed-copy launch and survival test
- clean uninstall
- closed v0.12 -> v0.12.1 upgrade
- upgraded-copy hash and launch verification
- safe running-process update block with old executable preservation
- successful retry after closing Trace
- same-version missing-EXE repair
- missing-uninstaller recovery
- custom install path containing spaces
- custom-path maintenance and uninstall
- forced rollback with exact application-byte restoration
- successful maintenance retry after rollback
- research-project and verified-backup preservation through maintenance, rollback, and uninstall
- version consistency and removal of stale `0.9.0`

Maintenance matrix evidence recorded all scenarios as green.
Rollback evidence recorded exact application-byte restoration and successful post-rollback maintenance.

## Current continuation point

Begin **Trace UX Foundation Phase 1** from the verified v0.12.1 baseline on `main`.

The first implementation target is production-state hygiene, Home and first launch. Prove that a genuinely fresh installed copy:

- opens to Trace Home
- contains no development/demo/fixture project
- contains no phantom participant such as `P01`
- does not show source-specific or transcript-specific controls without a real source
- offers New Project, Open Project, Import Project and Recover from backup clearly
- can create a short-form new project and land on a purposeful Project Overview

Preserve the existing v0.12.1 research and data-preservation gates while the shell is rebuilt.
