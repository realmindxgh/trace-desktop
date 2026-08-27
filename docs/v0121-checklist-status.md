# Trace v0.12.1 Full Checklist Status

This file tracks completion of the implementation checklist in `AGENTS.md` during the final hardening pass requested on 2026-08-23.

Status legend: `DONE`, `LOCAL GREEN`, `IN PROGRESS`, `PENDING`, `PHYSICAL UAT`.

| Area | Status | Current evidence / next action |
| --- | --- | --- |
| Proven source baseline and v0.12 regression suite | DONE | final full source gate `32723424461` green |
| Installer diagnosis / 9% misleading state | DONE | diagnosis completed; wrapper isolated; native update path verified |
| Version authority / stale 0.9.0 | DONE | final-v2 consistency contract green; stale `0.9.0` removed |
| Clean install / previous-version upgrade | DONE | final-v2 run `32724433832` green |
| Running-process update | DONE | final-v2 safely blocks a running Trace, preserves old bytes, then succeeds after close/retry |
| Global typography | DONE | final source gate browser/DPI matrix green |
| Structural bottom dock / stray wave | DONE | final source gate green |
| Inspector primary tabs | DONE | final source gate browser/DPI matrix green |
| Side panel resizing + persistence | DONE | final source gate browser/DPI matrix green |
| Recovery notice placement | DONE | final source gate browser/DPI matrix green |
| Code workspace full hardening | DONE | final source gate browser/DPI matrix green |
| Data onboarding | DONE | final source gate browser/DPI matrix green |
| Themes hardening | DONE | final source gate browser/DPI matrix green |
| Analyse hardening | DONE | final source gate browser/DPI matrix green |
| Write hardening | DONE | final source gate browser/DPI matrix green |
| Search standardization / Ctrl+F | DONE | final source gate browser/DPI matrix green |
| Forms/dialogs/dropdowns | DONE | final source gate browser/DPI matrix green |
| Accessibility | DONE | final source gate browser/DPI matrix green |
| Responsive + DPI matrix contracts | DONE | run `32723424461` browser matrix green across the required display/workspace cases |
| Performance / large-project safeguards | DONE | final workload contract and source gate green |
| Import UX | DONE | final carried research/import contracts green |
| Saving/recovery/diagnostics | DONE | final carried contracts plus rollback/recovery verification green |
| Visual/layout regression contracts | DONE | final browser/DPI matrix and full-checklist source contract green |
| Installer diagnostics / repair UI | DONE | final source and maintenance verification green |
| Expanded installer matrix | DONE | run `32724433832` green for clean install, upgrade, running-process block/retry, repair, partial install recovery, and custom path |
| Exact final Windows release after all above | DONE | artifact `Trace-v0.12.1-Exact-Verified-Windows-Release`, run `32724433832` |
| Physical real-machine visual UAT | PHYSICAL UAT | tracked in [issue #5](https://github.com/realmindxgh/trace-desktop/issues/5); requires the user's actual Windows display and scaling |

## Final source gate evidence

Run `32723424461` completed successfully from source SHA `a5bdc5335264db679d8cc98abac5b73a18effb3d`.

The final source gate passed:

- all carried research and regression contracts
- both frontends
- viewport/DPI matrix
- native Rust compile and unit tests
- setup-shell Rust checks
- NSIS custom-path raw-argument contract

Exact source artifact: `Trace-v0.12.1-Full-Checklist-Green-Source`  
Artifact digest: `sha256:dad38e53e5149190d97c65762cb4362accc84467f38c1b59c2aa97216cca123e`

## Final Windows release evidence

Run `32724433832` completed successfully as `Trace Windows v0.12.1 exact final v2`.

Final artifact: `Trace-v0.12.1-Exact-Verified-Windows-Release`  
Artifact digest: `sha256:233e76f199eb711f1de4fa02cc9cf95bdc3062e46e40cffa7239f06c921472f9`  
Final `TraceSetup.exe` SHA-256: `262186eea6ca1dc70c267ac81278cd0f77960e4a7525cc62b0d8ffbaeb0ba77d`

The final Windows verification passed:

- exact branded clean install
- installed executable hash equivalence with the native reference
- installed-copy launch and survival
- clean uninstall
- v0.12 -> v0.12.1 closed-app upgrade
- running-process safe block and retry
- same-version missing-EXE repair
- missing-uninstaller recovery
- custom install path with spaces
- custom-path maintenance and uninstall
- forced rollback with exact application-byte restoration
- successful retry after rollback
- research-project preservation
- verified-backup preservation
- version consistency
- stale `0.9.0` removal

## Repository promotion

The verified `trace-v0121` line was fast-forwarded to `main` on 2026-08-27. The default branch now contains the completed v0.12.1 engineering state instead of the older v0.11-era checkpoint.

## Local checkpoint evidence

The expanded source passed locally before reconstruction and was then revalidated on the Windows source gate. The final-v2 workflow also reran the carried research contracts before building the release.

## Physical UAT boundary

CI cannot truthfully replace inspection on the user's own Windows machine. The remaining item is a short physical UAT pass covering the installer maintenance flow and the Data, Code, Themes, Analyse, and Write workspaces at the user's actual display and scaling.

The acceptance steps are tracked in [issue #5](https://github.com/realmindxgh/trace-desktop/issues/5). Agents must update this file and `PROGRESS.md` if physical UAT reveals a defect or when physical UAT is completed.
