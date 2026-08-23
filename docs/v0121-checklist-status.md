# Trace v0.12.1 Full Checklist Status

This file tracks completion of the implementation checklist in `AGENTS.md` during the final hardening pass requested on 2026-08-23.

Status legend: `DONE`, `IN PROGRESS`, `PENDING`, `PHYSICAL UAT`.

| Area | Status | Current evidence / next action |
| --- | --- | --- |
| Proven source baseline and v0.12 regression suite | DONE | source gate `32649590459` and prior release evidence |
| Installer diagnosis / 9% misleading state | DONE | diagnosis completed; wrapper isolated; native update path verified |
| Version authority / stale 0.9.0 | DONE | v0.12.1 consistency contract green |
| Clean install / previous-version upgrade | DONE | final run `32651178336` |
| Running-process update | DONE | final run `32651178336` |
| Global typography | DONE, expanding audit | token scale exists; final audit covers residual tiny selectors |
| Structural bottom dock / stray wave | DONE | hardening contract green |
| Inspector primary tabs | DONE, expanding | overflow fixed; resizing/persistence still pending |
| Side panel resizing + persistence | IN PROGRESS | implementing left/right resize handles and saved widths |
| Recovery notice placement | IN PROGRESS | reserved layout exists; final keyboard/a11y behavior pending |
| Code workspace full hardening | IN PROGRESS | empty state done; resize/search/keyboard/scroll persistence pending |
| Data onboarding | DONE, expanding | progressive disclosure done; search/filter/empty distinctions and import queue pending |
| Themes hardening | PENDING | empty guidance, evidence inspection, context flow |
| Analyse hardening | PENDING | responsive tabs, sticky matrix headers, loading/progress, empty guidance |
| Write hardening | PENDING | empty state, autosave/save failure, recovery-oriented editor behavior |
| Search standardization / Ctrl+F | PENDING | implement context-aware shortcuts and visible filter state |
| Forms/dialogs/dropdowns | PENDING | focus trap, Escape behavior, viewport handling, control sizing audit |
| Accessibility | PENDING | focus rings, ARIA labels, keyboard order, reduced motion, pointer targets |
| Responsive + DPI matrix contracts | PENDING | automated viewport/layout contracts for required matrix |
| Performance / large-project safeguards | PENDING | debounce, chunking/limits, progress states, workload contracts |
| Import UX | PENDING | multi-file queue/results/duplicate/failure isolation contracts |
| Saving/recovery/diagnostics | PENDING | truthful save failure state, forced-close/recovery contracts, log safety |
| Visual/layout regression contracts | PENDING | DOM/layout fixture tests across main workspaces and installer states |
| Expanded installer matrix | PENDING | same-version repair, custom path, missing file, failed/locked update safety |
| Exact final Windows release after all above | PENDING | must rebuild from new green source |
| Physical real-machine visual UAT | PHYSICAL UAT | only item that requires the user's actual display/machine; cannot be truthfully simulated as physical UAT |

Agents must update this file and `PROGRESS.md` as groups move to `DONE`.
