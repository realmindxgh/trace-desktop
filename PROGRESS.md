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

The previously verified v0.12.1 Windows release remains an intermediate build. A new final installer will only be produced from a newly green full-checklist source checkpoint.

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

That build already proved clean install, installed-copy launch, uninstall preservation, real v0.12 -> v0.12.1 upgrade, and a running-process update scenario. It is superseded by the expanded checklist pass now underway.

## Expanded full-checklist implementation

The expanded source is reconstructed from the exact green v0.12.1 source artifact from run `32649590459`, then receives the committed full-checklist and installer-hardening transforms.

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

The corrected four-part bundle and workflow hash contract are being committed together before the next gate run.

## Release rule

Do not hand the prior installer to the user as the final checklist-complete release.

A new final EXE is allowed only after:
- the full source/contracts/browser/DPI/Rust gate is green
- the expanded Windows maintenance matrix is green
- carried research features remain green
- exact native build/install/upgrade/repair/rollback/uninstall verification passes
- `docs/v0121-checklist-status.md` and this ledger contain final evidence

## Physical UAT boundary

Physical inspection on the user's own Windows display cannot be simulated by CI. After engineering gates are complete, the final installer still requires a short physical UAT pass for the installer and Data/Code/Themes/Analyse/Write workspaces at the user's actual scaling.

## Exact next continuation point

Commit the corrected four-part finalizer bundle plus updated workflow integrity constants, rerun the full Windows gate, fix any browser/DPI or Rust failure it exposes, then use only the resulting green source artifact for the expanded maintenance matrix and new exact final Windows release.
