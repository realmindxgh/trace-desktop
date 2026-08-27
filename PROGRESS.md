# Trace Desktop Progress Ledger

This is the live execution ledger for Trace Desktop. Read it after `AGENTS.md`.

- `AGENTS.md` defines the full checklist and acceptance contract.
- `docs/v0121-checklist-status.md` tracks checklist areas.
- `PROGRESS.md` records what has actually happened, with evidence and the exact continuation point.

Any agent making a material change must update this ledger before handoff.

## Current snapshot

**Date:** 2026-08-27  
**Branch:** `main` and `trace-v0121` aligned after v0.12.1 promotion  
**Version:** `0.12.1`  
**Milestone:** Full v0.12.1 UX + Installer Hardening checklist  
**Status:** **ENGINEERING CHECKLIST COMPLETE; PHYSICAL UAT REMAINS**

The final v0.12.1 Windows verification has passed. The verified development line was fast-forwarded to `main` on 2026-08-27 so the default branch now carries the completed v0.12.1 engineering state. The prior intermediate installer is superseded by the exact final-v2 release artifact from run `32724433832`.

The only remaining acceptance item is physical real-machine UAT, tracked in [issue #5](https://github.com/realmindxgh/trace-desktop/issues/5).

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

## Expanded full-checklist implementation

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

## Repository promotion

On 2026-08-27, `main` was fast-forwarded from its older `6d23a97c3ab264af1f6deb3004fcb906a088d2c4` checkpoint to the verified v0.12.1 lineage. No force update was used. The default branch now exposes the completed v0.12.1 engineering state to normal clones and future work.

Documentation was then updated on `trace-v0121` to record the remaining physical UAT and its tracking issue. `main` must remain aligned with the latest `trace-v0121` documentation commit before handoff.

## Release rule

The engineering definition of done for v0.12.1 is now satisfied. The final installer is the artifact from run `32724433832`, not the earlier intermediate release.

## Physical UAT boundary

Physical inspection on the user's own Windows display cannot be simulated by CI. The only remaining acceptance item is a short real-machine UAT pass for the installer and Data/Code/Themes/Analyse/Write workspaces at the user's actual Windows scaling and display conditions.

The exact acceptance checklist is tracked in [issue #5](https://github.com/realmindxgh/trace-desktop/issues/5).

Until that physical pass is performed, v0.12.1 should be described as **engineering-complete and awaiting physical UAT**, not as fully UAT-complete.

## Continuation point

No further engineering gate is required before physical UAT. Use the final artifact from run `32724433832` for the real-machine acceptance pass. If physical UAT reveals a defect, return to the affected checklist item, patch from the verified v0.12.1 source lineage, and rerun the relevant source and Windows release gates before replacing the final artifact.

If physical UAT is clean, update `docs/v0121-checklist-status.md` and this ledger to mark UAT complete, close issue #5, and treat v0.12.1 as fully accepted.
