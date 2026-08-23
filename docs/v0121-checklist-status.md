# Trace v0.12.1 Full Checklist Status

This file tracks completion of the implementation checklist in `AGENTS.md` during the final hardening pass requested on 2026-08-23.

Status legend: `DONE`, `LOCAL GREEN`, `IN PROGRESS`, `PENDING`, `PHYSICAL UAT`.

| Area | Status | Current evidence / next action |
| --- | --- | --- |
| Proven source baseline and v0.12 regression suite | DONE | source gate `32649590459` and prior release evidence |
| Installer diagnosis / 9% misleading state | DONE | diagnosis completed; wrapper isolated; native update path verified |
| Version authority / stale 0.9.0 | DONE | v0.12.1 consistency contract green |
| Clean install / previous-version upgrade | DONE | first hardening release run `32651178336`; will be rerun after full checklist source |
| Running-process update | DONE, superseded by safer policy | first hardening run allowed update; full pass now detects/blocks a running Trace so research is not silently terminated |
| Global typography | LOCAL GREEN | literal sub-12px font-size audit is zero for both app and setup CSS; token scale retained |
| Structural bottom dock / stray wave | DONE | hardening contract green |
| Inspector primary tabs | LOCAL GREEN | four-column primary tabs + resizable/collapsible inspector |
| Side panel resizing + persistence | LOCAL GREEN | pointer + keyboard resize, min/max width, saved panel widths, inspector collapse |
| Recovery notice placement | LOCAL GREEN | notice is layout-owned, aria-live, dismissible, no absolute workspace overlay |
| Code workspace full hardening | LOCAL GREEN | actionable empty/recent-source flow, persistent transcript scroll, panel resize, keyboard coding shortcut, search handling |
| Data onboarding | LOCAL GREEN | progressive disclosure, no-data vs no-match states, multi-file queue, per-file results, cancel-pending, drag/drop |
| Themes hardening | LOCAL GREEN | zero-content onboarding, search, theme evidence counts and evidence inspection |
| Analyse hardening | LOCAL GREEN | zero-content onboarding, evidence search, five-view responsive tabs, sticky matrix headers, evidence drilldown |
| Write hardening | LOCAL GREEN | zero-content onboarding, larger editor, autosave state, save-failure state, linked evidence guidance |
| Search standardization / Ctrl+F | LOCAL GREEN | context-aware Ctrl+F routes to Data/Code/Themes/Analyse search; clear states present |
| Forms/dialogs/dropdowns | LOCAL GREEN | modal role/label, focus trap, Escape handling, viewport-safe modal CSS; browser regression still pending |
| Accessibility | LOCAL GREEN | visible focus, aria labels, keyboard resizers/cards, reduced motion, minimum control sizing; browser matrix still pending |
| Responsive + DPI matrix contracts | IN PROGRESS | CSS breakpoints complete; browser/DOM matrix test is next |
| Performance / large-project safeguards | LOCAL GREEN | debounced search, content-visibility for long lists, bounded evidence/matrix views, long-operation banners; workload contract still pending |
| Import UX | LOCAL GREEN | multi-file, drag/drop, queue, duplicate confirmation, failure isolation, cancellation, supported formats including DOCX/XLSX |
| Saving/recovery/diagnostics | LOCAL GREEN | truthful local save failure, findings autosave failure state, session recovery, privacy-safe diagnostic export already present; recovery test expansion pending |
| Visual/layout regression contracts | IN PROGRESS | new static `v0121_full_checklist.py` is green; browser DOM/layout fixture suite next |
| Installer diagnostics / repair UI | LOCAL GREEN | preflight now reports installed version, running/locked state, writeability, uninstaller, partial install, payload and free space; repair mode exposed |
| Expanded installer matrix | PENDING | same-version repair, custom path, running-app safe block, missing file/partial install, failed update old-copy preservation |
| Exact final Windows release after all above | PENDING | must rebuild from the new full-checklist green source |
| Physical real-machine visual UAT | PHYSICAL UAT | requires the user's actual display/machine; cannot be truthfully claimed from CI |

## Local checkpoint evidence

The expanded source currently passes locally:

- `node --check src/app.js`
- `node --check setup-shell/src/app.js`
- `tests/v12_analysis_math.mjs`
- `tests/schema_contract.py`
- `tests/v11_imports_display.py`
- `tests/v11_usability.py`
- `tests/v11_transcription.py`
- `tests/v11_pdf_text.py`
- `tests/v12_analysis.py`
- `tests/v0121_hardening.py`
- new `tests/v0121_full_checklist.py`
- root frontend build
- setup-shell frontend build

These remain `LOCAL GREEN` until reconstructed and compiled on the Windows source gate.

Agents must update this file and `PROGRESS.md` as groups move to `DONE`.
