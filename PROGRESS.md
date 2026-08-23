# Trace Desktop Progress Ledger

This file is the live status ledger for Trace Desktop. It complements `AGENTS.md`.

- `AGENTS.md` defines the execution contract, priorities, acceptance criteria, safety rules, and intended UX direction.
- `PROGRESS.md` records what has actually been completed, what evidence proves it, what was learned, what remains open, and the exact next continuation point.

## Mandatory agent rule

Any agent making a material Trace change must update this file before handing off work when one or more of the following occurs:

1. a milestone is completed;
2. a release gate changes state;
3. a significant failure is reproduced or fixed;
4. implementation direction changes because of evidence;
5. a new release artifact is produced;
6. a task is intentionally deferred;
7. the exact next action changes.

Do not mark work complete from source inspection alone. Record the concrete build, test, installer, upgrade, launch, uninstall, or data-preservation evidence that supports the status.

---

# Current snapshot

**Last updated:** 2026-08-23

**Working branch:** `trace-v0121`

**Current version:** `0.12.1`

**Milestone:** UX and Installer Hardening

**Engineering status:** **VERIFIED WINDOWS RELEASE BUILT SUCCESSFULLY**

**Remaining before closing the milestone:** user acceptance on the real Windows machine, especially visual/readability inspection at the user's normal display scaling. Automated release engineering is complete.

## Proven source checkpoint

- Source gate workflow: `Trace v0.12.1 UX and installer hardening gate`
- Source gate run: `32649590459`
- Result: `success`
- Green source artifact: `Trace-v0.12.1-Hardening-Green-Source`
- Artifact ID: `9495924443`
- Artifact SHA-256: `95bcb2674b8146214ad17944cc89923f02643f3817ea6549e058e399d8c4e510`
- Gate source commit: `63083fca29982781b2d800ec2c4f71ff1718f826`

The gate proved exact overlay reconstruction, all carried JavaScript/Python research contracts, v0.12.1 hardening contracts, both frontend builds, main Rust compile/tests, and setup-shell Rust compile.

## Proven final Windows release

- Final workflow: `Trace Windows v0.12.1 exact installer and upgrade verification`
- Final release run: `32651178336`
- Result: `success`
- Trigger commit: `69fd23c120f90106ac6b2b493327ca221c94a8f7`
- Release artifact: `Trace-v0.12.1-Exact-Verified-Windows-Release`
- Artifact ID: `9496529233`
- Artifact ZIP SHA-256: `d11cc13472fbd7168d7bd06d231633506624754a88d480daac58306316ec59c0`
- Verified branded installer SHA-256: `8bdd651c64cb787cc0f0d6da3eb5331b0240d8b7c76a5bf8a29a371ad700c4f4`

Local post-download verification reproduced the exact installer SHA-256 recorded by CI.

---

# v0.12.1 work completed

## 1. Installer diagnosis and maintenance-path hardening

Completed:

- Reproduced and investigated the update problem using real prior-release installers on Windows CI.
- Determined that the visible `9% / Checking this PC` state was not a reliable locator for the underlying failure because the setup UI forced an early progress value.
- Demonstrated that the underlying native NSIS update path can replace an existing Trace installation correctly.
- Isolated the problematic layer to the branded setup/wrapper behavior rather than the native app payload itself.
- Made setup progress-event subscription non-blocking so a listener problem cannot prevent installation.
- Added more actionable error classification and technical-detail support.
- Preserved installer logging without exposing research content.
- Corrected maintenance terminology from generic install wording toward update/review behavior.
- Raised setup typography and improved layout reservation around setup controls.

## 2. Version consistency

Completed:

- Removed the stale visible `0.9.0` release string from shipped setup behavior.
- Updated v0.12.1 version assertions and metadata contracts.
- Added a hardening test that fails if the stale release version reappears.
- Final Windows verification reports `version_0_12_1_consistent=true` and `stale_0_9_0_removed=true`.

## 3. Application readability and layout

Completed in the verified v0.12.1 source:

- Raised the global typography scale.
- Raised Compact, Comfortable, and Large readability presets rather than fixing one screen only.
- Changed bottom workspace navigation from an overlapping floating layer into a layout-owned dock region.
- Removed the stray blue/green wave rendering observed across the bottom of the application.
- Rebuilt inspector primary tabs as a stable four-column grid so Info, Codes, Notes, and Memos do not require a primary horizontal scrollbar.
- Removed meaningless missing-participant punctuation/placeholder metadata.
- Added an actionable Code empty state with clear next actions.
- Simplified first-run Data onboarding around importing research material.
- Demoted advanced interoperability actions through progressive disclosure.
- Added a visible Assistant label instead of relying only on the sparkle icon.

## 4. Regression contracts

The v0.12.1 source and release pipeline preserve and re-run the existing research functionality contracts for:

- schema integrity;
- Office and survey imports;
- display behavior;
- coding/search/annotations;
- usability regressions;
- offline transcription;
- PDF text analysis;
- named coders;
- participant x code matrix;
- code co-occurrence;
- negative-case finder;
- group comparisons;
- intercoder agreement;
- raw agreement and Cohen's kappa mathematics;
- analysis CSV exports.

A dedicated `tests/v0121_hardening.py` contract was added for the new release-hardening behavior.

---

# Final release verification evidence

The final run `32651178336` passed every substantive workflow step and the outer job completed with `success`.

The generated `FINAL-VERIFICATION.txt` records all of the following as true:

- exact branded clean install;
- embedded payload matches generated native NSIS installer;
- installed executable matches native payload;
- clean installed copy launches;
- clean installed copy survives the launch test;
- exact branded uninstall succeeds;
- local project data survives uninstall;
- verified backups survive uninstall;
- real v0.12 -> v0.12.1 in-place upgrade succeeds;
- upgraded executable matches a clean v0.12.1 installation;
- upgraded copy launches;
- upgrade preserves project data;
- upgrade preserves verified backups;
- post-upgrade uninstall preserves data;
- update while the previous v0.12 process is running completes in the automated scenario;
- the post-update v0.12.1 copy launches after the old process is closed;
- larger typography contract is green;
- dock no longer overlays content;
- inspector tab overflow contract is green;
- stray wave is removed;
- Code empty state is actionable;
- Data onboarding uses progressive disclosure;
- branded setup errors are actionable;
- branded setup progress listener is non-blocking;
- all carried research contracts remain green.

## Closed-app upgrade evidence

`UPGRADE-VERIFICATION.txt` records:

- previous v0.12 installed hash: `ca6577e267bb5737d6bbd90733e2d335fb54628c1ecadc23e55d06db3ea6c2d7`
- upgraded v0.12.1 installed hash: `fa890fe40cdb4fa7ab8a10fe29654cd251b32819149ce197a944bf2ae80f5559`
- matches clean v0.12.1: `true`
- project data preserved: `true`
- backup data preserved: `true`
- upgraded copy launched: `true`
- post-upgrade uninstall preserved data: `true`

## Running-process update evidence

`RUNNING-UPGRADE-VERIFICATION.txt` records:

- previous v0.12 hash: `ca6577e267bb5737d6bbd90733e2d335fb54628c1ecadc23e55d06db3ea6c2d7`
- update exit while previous app process was running: `0`
- on-disk v0.12.1 hash after update: `fa890fe40cdb4fa7ab8a10fe29654cd251b32819149ce197a944bf2ae80f5559`
- exact v0.12.1 written during running-process scenario: `true`
- upgraded copy launched after the old process was closed: `true`

---

# Important findings discovered during v0.12.1

## The old 9 percent screen was misleading

The setup UI could display 9 percent before the actual underlying installation operation had progressed far enough to prove that `Checking this PC` itself was the failure. Future debugging must rely on structured setup diagnostics and exit/error details, not only the visible progress percentage.

## Clean-install verification alone was insufficient

The v0.12 pipeline proved a high-quality clean installation but did not originally prove upgrade over a real previous release. v0.12.1 permanently adds previous-version upgrade verification as a release requirement.

## Installed executable hashes must be compared on equivalent paths

A raw build-folder executable can differ from an executable installed through NSIS. Upgrade verification therefore compares the upgraded installed copy against a clean-installed reference generated through the same release installer path.

## Harness failures must not be confused with product failures

During diagnosis, a PowerShell evidence script failed because it attempted `.Trim()` on an empty stderr value. That was a test-harness defect, not a Trace installer defect. The diagnostic workflow was rewritten so evidence collection does not prematurely abort the scenario being investigated.

---

# Open / deferred items

These items are not allowed to be silently forgotten. They are either still pending user acceptance or intentionally deferred beyond v0.12.1.

## Pending real-machine user acceptance

- [ ] Install/update the new verified `TraceSetup.exe` on the user's actual Windows machine.
- [ ] Confirm the previously observed maintenance-screen failure is gone in real interactive GUI use.
- [ ] Inspect installer typography and error/details layout at the user's normal Windows scaling.
- [ ] Inspect Data workspace typography and layout visually.
- [ ] Inspect Code workspace typography, participant header, left source panel, inspector tabs, and bottom dock visually.
- [ ] Confirm no blue/green line leakage remains.
- [ ] Confirm no content hides behind workspace navigation.
- [ ] Confirm text remains comfortable rather than merely technically larger.
- [ ] Capture screenshots for any remaining visual corrections.

## Deferred beyond this hardening release unless UAT reveals them as blockers

- richer coder-management UI beyond add/select;
- media-selection intercoder comparison beyond shared transcript units;
- semantic/AI contradiction detection beyond systematic A-present/B-absent negative cases;
- REFI variables/links/graphs and deeper interoperability;
- local AI layer planned for the next major development tranche.

---

# Exact next continuation point

1. Hand the verified v0.12.1 `TraceSetup.exe` to the user with SHA-256 `8bdd651c64cb787cc0f0d6da3eb5331b0240d8b7c76a5bf8a29a371ad700c4f4`.
2. User runs it against the existing local Trace installation and inspects the interactive maintenance flow.
3. User opens Trace and provides screenshots of the main Data and Code workspaces at normal display scaling.
4. If real-machine UAT exposes any remaining layout or setup defect, fix it on `trace-v0121`, update this ledger, and repeat the exact release gate.
5. If UAT is clean, close v0.12.1, clean temporary diagnostic/helper workflows if appropriate, merge/promote the accepted source according to repository policy, and only then begin the next milestone.

---

# Progress history

| Date | Milestone | Result | Evidence |
| --- | --- | --- | --- |
| 2026-08-23 | v0.12 verified baseline | Complete | source run `32638636953`, release run `32639353769` |
| 2026-08-23 | UX/installer visual assessment | Complete | user screenshots; `AGENTS.md`; `docs/visuals/` |
| 2026-08-23 | v0.12.1 upgrade diagnosis | Complete | Windows reproduction/diagnosis workflows |
| 2026-08-23 | v0.12.1 source hardening gate | Success | run `32649590459`, artifact `9495924443` |
| 2026-08-23 | v0.12.1 final Windows release verification | Success | run `32651178336`, artifact `9496529233` |
| 2026-08-23 | v0.12.1 real-machine UAT | Pending | waiting for interactive user validation |

---

# Handoff standard

When another agent continues this project, it should read in this order:

1. `README.md`
2. `AGENTS.md`
3. `PROGRESS.md`
4. `docs/visuals/README.md`
5. relevant `build-status/*` file
6. relevant workflow and test files

Before ending a substantial work session, update `PROGRESS.md` with the new status and exact next continuation point.