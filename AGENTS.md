# Trace Desktop Agent Execution Guide

This file is the primary execution guide for any coding agent, contributor, or automated development system working on Trace Desktop.

Read this file before changing application code, installer code, CI, release controls, or UX. Treat it as the current implementation contract unless a newer explicit project instruction supersedes it.

## 1. Current mission

The immediate target is **Trace v0.12.1: UX and Installer Hardening**.

Do **not** begin major v0.13 AI work until the v0.12.1 acceptance gates in this file are complete.

Trace already has a strong product architecture and a verified v0.12 Windows release. The present task is not a wholesale redesign. The task is to make the existing product reliable, readable, robust, easy to learn, comfortable for long research sessions, and safe to update over an existing installation.

The product model to preserve is:

`Data -> Code -> Themes -> Analyse -> Write`

The design should remain spacious and calm. Do not solve current problems by making the interface denser.

---

## 2. Verified v0.12 baseline

The v0.12 Windows release was successfully built and verified through the exact branded installer pipeline.

Reference baseline:

- Source gate run: `32638636953`
- Final Windows release verification run: `32639353769`
- Final workflow result: `success`
- Release artifact: `Trace-v0.12-Exact-Verified-Windows-Release`
- Verified branded installer SHA-256: `b4a5a69a889236c591f4aa3448e05927f5c6351c82a31b08970f8291ff00ba28`

That successful pipeline verified:

- green v0.12 source checkpoint
- JavaScript and schema contracts
- Rust compile and unit tests
- native Tauri Windows build
- generated NSIS payload
- branded `TraceSetup.exe`
- exact branded installation
- installed `Trace.exe` hash equivalence with the native installer payload
- launch of the installed copy
- installed copy surviving the launch test
- branded uninstall
- preservation of a research-data sentinel after uninstall
- release artifact creation

This baseline must remain reproducible. v0.12.1 work must not regress the functionality already proven in v0.12.

---

## 3. Why v0.12.1 is required

The verified clean-install pipeline exposed a gap once the installer was used on a real machine with an existing Trace installation.

Known release-blocking observations:

1. The branded installer correctly detects an existing Trace installation and enters maintenance mode.
2. The visible setup version is incorrectly shown as `0.9.0` instead of the current release version.
3. Pressing **Update Trace** can fail at roughly 9 percent during **Checking this PC**.
4. The failure UI reports only generic text such as **Setup stopped safely** and does not expose the real cause or an actionable recovery step.
5. Therefore, clean installation is verified, but real in-place update or repair over an existing normal installation is not yet proven.

Known application UX observations:

1. Important text is too small throughout the app.
2. The bottom workspace navigation overlaps page content.
3. Blue and green decorative or SVG-like lines escape across the bottom of the UI.
4. The right inspector clips the Memos tab and shows a horizontal scrollbar for its own primary navigation.
5. The recovered-session notification overlaps the workspace awkwardly.
6. The Data page presents too many equally prominent actions to a new user.
7. The Code workspace has a weak dead-end empty state when no source is open.
8. Missing participant metadata is shown as dangling punctuation and placeholder dashes.
9. Some controls and helper text are sized for screenshots rather than long research sessions.
10. Current layout robustness is insufficient across common Windows resolutions and DPI scaling levels.

These are not cosmetic nice-to-haves. They directly affect readability, learnability, confidence, and update safety.

---

## 4. Non-negotiable product principles

Every agent must preserve the following.

### 4.1 Research data is more important than application files

Never delete or overwrite research projects merely because the app is updated, repaired, or uninstalled.

Protect:

- Trace project databases
- imported project copies
- participant records
- codes
- coding references
- coder assignments
- themes
- notes
- memos
- analysis state where persisted
- verified backups
- local project metadata
- user-created outputs

Application binaries may be replaced. Research data must survive maintenance unless the user explicitly asks to delete it.

### 4.2 Local-first behavior must remain true

Trace is a local-first research workspace. Do not silently introduce network dependency into core research workflows.

### 4.3 Existing v0.12 research capabilities must not regress

Preserve and retest:

- Office and survey imports
- coding and annotations
- undo and redo
- offline transcription
- PDF text analysis
- named coders
- participant x code matrix
- code co-occurrence
- negative-case finder
- participant-group comparison
- intercoder comparison
- raw agreement
- Cohen's kappa
- analysis CSV export
- recovery and project preservation behavior

### 4.4 Readability beats artificial density

Trace is used for long periods. Researchers may read transcripts and code material for hours.

Do not use tiny text simply to fit more controls on screen.

### 4.5 Progressive disclosure beats feature dumping

Advanced capabilities should remain accessible without competing with the user's immediate task.

For a new project, the first job is usually to bring in research material, not to think about QDC, QDPX, backup verification, group matrices, and every advanced export format simultaneously.

### 4.6 The installed app is the deliverable

Source inspection is not completion.

A release is complete only when the real Windows installer has built, installed, launched, updated or repaired where required, uninstalled, and passed data-preservation verification.

---

## 5. Definition of done for v0.12.1

Do not mark v0.12.1 complete until all of these are true.

### Installer and maintenance

- [ ] Fresh installation succeeds through the exact branded `TraceSetup.exe`.
- [ ] An existing previous Trace installation can be updated in place.
- [ ] Repair over the same version works or is intentionally and clearly defined.
- [ ] Update while Trace is running is handled safely and clearly.
- [ ] Custom install paths are handled.
- [ ] Normal `%LOCALAPPDATA%\Trace` installations are handled.
- [ ] A failed update leaves the prior usable installation intact or rolls back safely.
- [ ] Research projects survive update, repair, and uninstall.
- [ ] The installer shows the correct version everywhere.
- [ ] Installer errors are actionable and expose technical details without exposing research content.
- [ ] The installed executable matches the native payload expected by CI.
- [ ] The installed copy launches successfully.

### UX and visual robustness

- [ ] Global typography has been raised to a readable scale.
- [ ] No important application text is rendered at an unnecessarily tiny size.
- [ ] Bottom navigation never covers content.
- [ ] No stray blue or green lines escape their component boundaries.
- [ ] Inspector tabs fit without horizontal scrolling.
- [ ] No primary tab label is clipped.
- [ ] Empty states tell the user what to do next.
- [ ] Missing participant metadata is hidden rather than represented by meaningless punctuation.
- [ ] Data onboarding is quieter and clearer.
- [ ] The app remains usable at all required resolutions and scaling factors.
- [ ] The UI has no unexplained horizontal page scrollbars.
- [ ] Keyboard focus and interaction states remain visible.

### Regression and release

- [ ] Existing v0.12 research contracts remain green.
- [ ] New v0.12.1 UX and installer tests are green.
- [ ] Upgrade CI is green.
- [ ] Manual QA on a real Windows machine is complete.
- [ ] Final Windows release workflow is green.
- [ ] Release artifact contains installer, hashes, and verification record.

---

## 6. Priority system

Agents should work in this order unless a blocking dependency requires otherwise.

### P0: Release blockers

1. Real update or repair failure at 9 percent.
2. Incorrect visible installer version.
3. Data-preservation risk during update.
4. Lack of rollback or safe abort behavior.
5. Layout overlap that hides controls or content.
6. Stray graphical lines that visibly corrupt the interface.
7. Clipped inspector navigation.

### P1: Core usability

1. Global typography scale.
2. Data-page onboarding simplification.
3. Code-workspace empty state.
4. Side panel sizing and resizing.
5. Recovered-session notification placement.
6. Common-resolution and DPI robustness.
7. Accessibility and keyboard interaction.

### P2: Fit and finish

1. Menu sizing.
2. Tooltip consistency.
3. minor spacing refinements.
4. optional collapsible navigation behavior.
5. additional polish once P0 and P1 are verified.

Do not spend significant time on P2 while a P0 issue remains open.

---

# PART I: INSTALLER AND UPDATE HARDENING

## 7. Phase 0: Re-establish the proven source before editing

The repository has historically reconstructed exact working source through bootstrap overlays and CI-produced source artifacts. Do not assume an arbitrary local or partial directory is canonical.

Before implementation:

1. Inspect the current `trace-v012` branch.
2. Inspect `.github/workflows/v012-analysis-check.yml`.
3. Inspect `.github/workflows/windows-v012-final.yml`.
4. Inspect `build-status/windows-v012-exact-final.txt`.
5. Reconstruct or obtain the same complete v0.12 source checkpoint used by the successful final release.
6. Verify version `0.12.0` and all required source files before changing anything.
7. Preserve the verified v0.12 checkpoint so a regression comparison remains available.

Required baseline checks should include the existing tests carried by v0.12, such as:

- `tests/schema_contract.py`
- `tests/v11_imports_display.py`
- `tests/v11_usability.py`
- `tests/v11_transcription.py`
- `tests/v11_pdf_text.py`
- `tests/v12_analysis.py`
- `tests/v12_analysis_math.mjs`
- Rust unit tests

If source reconstruction changes, update this guide and CI so the next agent does not have to rediscover the process.

---

## 8. Phase 1: Diagnose the 9 percent maintenance failure

Do not patch around the failure blindly.

Instrument the installer so **Checking this PC** produces a precise result.

Check at minimum:

- detected install path
- detected installed version
- whether `Trace.exe` exists
- whether `Trace.exe` is running
- whether application files are locked
- whether the install directory is writable
- whether previous uninstall metadata exists
- whether the embedded payload can be extracted and verified
- whether the old installation is complete or partial
- whether the requested path is supported
- available disk space
- relevant process exit codes
- installer or NSIS return codes

Diagnostic requirements:

- errors must be structured internally
- the user-facing message must be short and actionable
- technical details must be available separately
- logs must not contain transcript text, code contents, notes, memos, participant data, or other research content

Examples of acceptable user-facing errors:

- `Trace is still running. Close Trace and try the update again.`
- `Windows could not write to the existing Trace installation.`
- `The existing installation is incomplete. Repair can restore the missing application files.`
- `The installer payload could not be verified.`
- `There is not enough free space to complete the update.`

The generic message `Setup stopped safely` is not enough on its own.

Acceptance gate:

- [ ] The original 9 percent failure can be reproduced or its exact cause can be demonstrated.
- [ ] The installer reports the underlying cause accurately.
- [ ] Retry is offered only when retrying can plausibly succeed.

---

## 9. Phase 2: Make maintenance mode reliable

Support these scenarios explicitly.

### 9.1 Fresh install

- no previous Trace installation
- default per-user directory
- custom supported directory
- shortcuts on or off
- launch after setup on or off

### 9.2 Update previous version

- previous version installed in normal `%LOCALAPPDATA%\Trace`
- previous version installed in a custom directory
- previous version closed normally
- previous version was previously launched and has project data
- previous version has shortcuts
- previous version has backups

### 9.3 Trace is running

Preferred behavior:

1. Detect the running process.
2. Explain that the app must close before binaries are replaced.
3. Offer a safe `Close Trace and continue` action where practical.
4. If automatic closure is not appropriate, tell the user exactly what to do.
5. Never silently kill a process while research data may still be saving.

### 9.4 Repair same version

Repair must restore missing or damaged application files without touching research projects.

### 9.5 Partial or malformed previous installation

Handle missing executable, missing uninstaller, or stale installation metadata without blindly deleting unknown directories.

### 9.6 Safe abort and rollback

Before modifying the installed application, know how to recover.

At minimum:

- do not destroy the previous installation before the new payload is validated
- stage replacement files before committing destructive changes where practical
- if replacement fails, restore the previous application state or leave the old installation usable
- remove temporary payloads after success or failure
- never roll research data backward as part of application rollback

Acceptance gate:

- [ ] Previous version -> v0.12.1 succeeds.
- [ ] Same-version repair succeeds or is intentionally unsupported with a clear explanation.
- [ ] Running-process scenario is handled safely.
- [ ] Failed update does not strand the user without a usable installation.
- [ ] Projects survive every path.

---

## 10. Phase 3: Create a single version authority

Current visible `0.9.0` text proves version information has drifted.

Create one authoritative release version mechanism and derive all shipped version strings from it.

Synchronize:

- root package version
- setup-shell package version
- main Rust package version
- setup-shell Rust package version
- Tauri config version
- setup-shell Tauri config version
- installer UI
- top-right setup version
- review page version
- Windows file metadata where applicable
- NSIS metadata
- MSI metadata if MSI remains part of release
- Add/Remove Programs entry
- verification output

For the hardening release, the intended version is `0.12.1`.

Add CI that fails if:

- a shipped UI still contains `0.9.0`
- application and installer versions differ
- package/Tauri/Rust release versions disagree

Acceptance gate:

- [ ] One change updates all shipped version surfaces.
- [ ] No stale `0.9.0` remains in production UI or metadata.

---

## 11. Phase 4: Installer UX hardening

### Typography

Raise installer typography globally.

Recommended working targets:

- normal body text: 14 to 16 px
- control text: 14 to 15 px
- secondary metadata: 12.5 to 13.5 px
- page headings: large enough for hierarchy but not at the expense of microscopic supporting text

Do not place important information below 12 px.

### Bottom setup controls

The floating bottom control capsule must never cover setting cards, error content, or progress content.

Preferred implementation:

- visually floating if desired
- structurally accounted for by layout
- permanent reserved bottom space or a true docked layout region

### Scroll behavior

- avoid full-page scrolling on standard installer screens where practical
- keep scrollbars visually consistent with Trace
- never let a scrollbar overlap content
- ensure the Options page fits comfortably at 1366 x 768 at 100 percent scaling if possible

### Maintenance terminology

Fresh install may use:

`Welcome -> Options -> Ready -> Install`

Maintenance mode should adapt, for example:

`Welcome -> Options -> Review -> Update`

Uninstall mode should end in `Remove` or `Uninstall`, not `Install`.

Use consistent wording for `Update / repair Trace`.

### Maintenance summary

Where useful, show:

- installed version
- new version
- installation location
- whether projects are protected
- shortcut behavior
- post-setup behavior

Acceptance gate:

- [ ] No installer content is hidden behind the bottom controls.
- [ ] Important text is readable at common Windows scaling levels.
- [ ] Maintenance wording matches the selected action.

---

# PART II: APPLICATION UX HARDENING

## 12. Phase 5: Introduce a global typography system

This is a cross-application task, not a one-screen patch.

Audit every CSS `font-size` and remove arbitrary tiny values where they are used for meaningful content.

Create reusable design tokens. Exact names may vary, but the system should represent at least:

- page title
- section title
- body
- UI/control text
- secondary metadata
- caption or microcopy

Recommended targets:

| Role | Target |
| --- | --- |
| Page heading | 26 to 34 px |
| Section heading | 18 to 22 px |
| Body / reading text | 15 to 16 px |
| Controls / tabs / buttons | 14 to 15 px |
| Secondary metadata | 12.5 to 13.5 px |

Important rules:

- meaningful text should normally not be below 12 px
- transcript reading text should favor comfort over density
- larger fonts require appropriate line height and component height
- do not shrink text just to avoid fixing layout

Audit at minimum:

- project title and subtitle
- breadcrumbs
- save status
- sidebar labels
- sidebar counts
- search fields
- participant metadata
- transcript text
- code labels
- themes
- inspector tabs
- notes
- memos
- tables
- matrices
- chart labels
- dropdowns
- context menus
- buttons
- form labels
- empty states
- toasts
- interoperability copy
- backup copy
- installer copy

Acceptance gate:

- [ ] Typography is tokenized.
- [ ] No page relies on clusters of tiny text.
- [ ] Long reading sessions are comfortable at 1600 x 900 and 1920 x 1080.

---

## 13. Phase 6: Fix global layout robustness

### 13.1 Bottom workspace navigation

The current Data/Code/Themes/Analyse/Write dock visibly overlaps page content.

Requirements:

- content must never flow underneath it
- reserve its full height in layout
- no buttons, cards, table rows, editors, or messages may be hidden behind it
- selected workspace must remain obvious
- keyboard focus must be visible
- the Assistant/sparkle action must have a text label or an unambiguous accessible label

Preferred approach: keep the current visual character but make it structurally docked.

### 13.2 Stray blue and green lines

Find the source of the lines crossing the lower interface.

Investigate:

- SVG overflow
- canvas or path animation
- decorative component overflow
- Assistant button decoration
- transform or clipping bugs

Fix the root cause. Do not merely cover the lines with another layer.

### 13.3 Header

Increase legibility of:

- project name
- project type
- breadcrumbs
- save status

Handle:

- long project names
- narrow windows
- deep breadcrumbs
- truncation with tooltip where useful

### 13.4 Recovered-session notice

The recovery message must not float awkwardly over workspace content.

Use either:

- a proper reserved notification strip below the header, or
- a normal toast that does not cover task controls

Acceptance gate:

- [ ] No overlap at supported sizes.
- [ ] No escaped graphical artifacts.
- [ ] Header remains readable under long-title and scaling tests.

---

## 14. Phase 7: Harden the Code workspace

### Left data sidebar

- make the sidebar resizable
- define sensible minimum and maximum widths
- persist width where practical
- increase source and search text
- distinguish `no sources exist` from `no sources match search`

For zero sources use guidance such as:

`No sources yet. Import your first source.`

For a failed search use guidance such as:

`No sources match "...".`

### Main coding canvas empty state

Do not leave a researcher with only:

`No text source is open.`

Provide a useful next action:

- `Import source`
- `Go to Data`
- if sources already exist, show available or recent sources

If exactly one source exists, consider opening it automatically if doing so is predictable and safe.

Disable or hide transcript-only controls when no transcript exists.

### Transcript reading experience

- comfortable font size
- comfortable line height
- stable selection behavior
- clear coding highlights
- overlapping code highlights remain interpretable
- preserve scroll position
- preserve selected source across workspace switches
- support keyboard-oriented coding where practical

### Participant header

Do not render empty metadata as:

`Participant • — years exp. • —`

Hide absent values entirely. Reveal metadata only when present.

### Right inspector

The current inspector has clipped tabs and a horizontal scrollbar.

Requirements:

- `Info | Codes | Notes | Memos` must fit at normal width
- no horizontal scrollbar for primary inspector navigation
- make inspector resizable
- define min and max widths
- persist width where practical
- vertical scrolling is allowed for content
- active tab and counters remain readable
- long code names wrap or truncate intentionally
- consider collapse/show controls for focused reading

Acceptance gate:

- [ ] Code workspace has no dead-end empty state.
- [ ] Inspector primary tabs are fully visible.
- [ ] Side panels are robust at supported resolutions.

---

## 15. Phase 8: Simplify the Data workspace

The Data page should guide a new project toward one obvious first action.

Primary onboarding goal:

`Bring in your research material`

Primary CTA:

`Import sources`

Current actions such as New project, Open `.trace` project, Collections, QDC, QDPX, and backup tools should remain available but must not all compete at equal visual weight.

### Recommended hierarchy

Primary:

- Import sources

Secondary:

- Open existing Trace project

Application-level or menu-level:

- New project

Advanced or progressively disclosed:

- QDC import/export
- QDPX import/export
- detailed backup controls

### Active / Starred / Archived

If all counts are zero, these controls can be visually quiet. Consider hiding advanced filtering until it becomes relevant, but do not make existing functionality unreachable.

### Search and Collections

- ensure search placeholder is not clipped
- keep source search visually associated with source listing
- keep Collections secondary during zero-source onboarding

### Source cards

Once populated, source cards should be scannable and show useful metadata without becoming dense.

Possible metadata:

- source name
- source type
- participant or case where linked
- coding count
- modified or imported status where useful

Acceptance gate:

- [ ] A first-time user can identify the first action within a few seconds.
- [ ] Advanced interoperability no longer dominates zero-source onboarding.

---

## 16. Phase 9: Harden Themes, Analyse, and Write

These workspaces may not show every defect visible in the current screenshots, but the same global hardening rules apply.

### Themes

- increase typography
- make relationship between codes and themes understandable
- provide a meaningful empty state
- make theme creation obvious after codes exist
- allow evidence contributing to themes to be inspected easily
- preserve context when moving between Code and Themes

### Analyse

Preserve all v0.12 analysis features.

Harden:

- Matrix
- Co-occurrence
- Negative cases
- Groups
- Intercoder

Requirements:

- readable tabs
- readable filters
- readable evidence text
- no accidental tab overflow
- horizontal scrolling only where genuinely required by a large matrix
- freeze matrix headers where useful
- clear coder A / coder B selection
- clear plain-language explanation of raw agreement and Cohen's kappa
- do not present kappa as an absolute quality score
- loading or progress feedback for large calculations
- easy evidence drill-down

### Write

- comfortable editor font and line height
- readable toolbar
- no bottom-dock overlap
- reliable autosave
- visible save failure state
- recovery after abnormal closure
- evidence/code/theme insertion remains understandable

Acceptance gate:

- [ ] Each workspace has a clear zero-content state.
- [ ] Global typography and overlap fixes apply consistently.
- [ ] Existing v0.12 analysis math remains unchanged unless a tested bug is found.

---

# PART III: CROSS-CUTTING UX QUALITY

## 17. Empty-state system

Audit every empty, filtered, loading, and error state.

Do not use one generic empty message for different conditions.

Every empty state should answer:

1. What is empty?
2. Why does that matter?
3. What should the user do next?

Distinguish:

- zero content
- zero search results
- content hidden by filters
- loading
- failure

Avoid meaningless placeholders and dangling punctuation.

---

## 18. Search behavior

Standardize search across Data, Code, Themes, and Analyse.

Requirements:

- readable input text
- readable result text
- clear match highlighting where appropriate
- visible active filters
- clear distinction between no data and no matches
- predictable clear action
- sensible keyboard shortcuts such as Ctrl+F where contextually appropriate
- transcript search must not be confused with app-wide or source-list search

---

## 19. Forms, menus, dialogs, and dropdowns

Audit all of them for:

- typography
- control height
- focus state
- z-index
- keyboard navigation
- viewport edge handling
- modal fit at 1366 x 768
- consistent primary/secondary/destructive ordering
- accessible labels
- safe Escape behavior

No dropdown should appear beneath the bottom dock or sidebars.

No modal should require hidden nested scrolling unless genuinely necessary.

---

## 20. Accessibility

At minimum:

- logical keyboard tab order
- visible focus rings
- no color-only status communication
- sensible text/background contrast
- readable disabled states
- accessible names for icon-only controls
- tooltips for unfamiliar icons
- reasonable pointer targets
- support Windows text scaling without breaking layout
- respect reduced-motion preferences where animation exists
- do not remove focus outlines without replacing them with a clear equivalent

The Assistant/sparkle control must not rely solely on an unexplained symbol.

---

## 21. Responsive desktop and DPI matrix

Test at minimum:

### Viewport sizes

- 1280 x 720
- 1366 x 768
- 1440 x 900
- 1600 x 900
- 1920 x 1080
- 2560 x 1440

### Windows scaling

- 100 percent
- 125 percent
- 150 percent
- 175 percent where practical

### States

- maximized
- normal window
- narrow resized window
- long project title
- long source title
- long code name
- long memo title
- deep breadcrumbs

At every supported combination verify:

- no clipped primary labels
- no unexplained horizontal page scrollbar
- no hidden buttons
- no content beneath fixed navigation
- no unreadably tiny text
- no collapsed inspector tabs

---

## 22. Loading, performance, and responsiveness

Test real research-sized workloads.

Include:

- hundreds of sources
- long transcripts
- many participants
- thousands of codes or coding references where feasible
- large matrices
- large search result sets

Use list virtualization where needed.

Debounce expensive search operations.

Do not freeze the whole UI during long analysis or import operations.

Show progress for operations that are genuinely long:

- import
- transcription
- backup
- export
- large analyses

Allow cancellation where it can be made safe.

---

## 23. Import UX

Verify and improve:

- multi-file import
- supported-format explanation
- drag and drop if present
- import queue
- per-file result
- duplicate handling
- Unicode filenames
- long paths
- external-drive sources
- network paths where supported
- large files

Regression formats include at least:

- TXT or text transcript
- DOCX
- CSV
- XLSX survey
- PDF
- image
- audio
- video

One failed file should not unnecessarily invalidate unrelated valid files.

Original source files must remain untouched when Trace copies material into a local project.

---

## 24. Saving, recovery, and diagnostics

Autosave status must be truthful.

Test:

- successful save
- failed save
- forced process termination
- unclean close
- reopen and recovery
- no duplicate records after recovery

Application logs must be useful for diagnostics without leaking research content.

Where appropriate provide a way to export diagnostic logs.

---

# PART IV: AUTOMATED TESTING AND CI

## 25. Add visual regression and layout contracts

Automated tests should catch the classes of defects currently visible.

Add screenshot or DOM/layout tests for at least:

- Data empty state
- Data populated state
- Code empty state
- Code populated state
- Themes
- Analyse
- Write
- installer fresh-install mode
- installer maintenance mode
- installer error state

Add assertions for:

- no root horizontal overflow at supported viewport widths
- content bottom padding is at least sufficient for the workspace dock
- inspector tabs fit without horizontal scroll
- minimum typography tokens are respected
- known stale version strings are absent
- decorative elements are clipped to their intended component

A visual test is useful only if it detects a real regression. Avoid brittle pixel-perfect tests for harmless anti-aliasing differences.

---

## 26. Expand Windows installer CI with an upgrade matrix

The current final pipeline proves a clean install. v0.12.1 must prove maintenance too.

Required upgrade test flow:

1. Build or retrieve the previous verified Trace installer.
2. Install the previous version on a Windows GitHub Actions runner.
3. Launch the installed previous copy.
4. Create or stage representative research data.
5. Close the previous app cleanly.
6. Run the new exact branded `TraceSetup.exe` in update mode.
7. Verify update completes.
8. Verify the installed version is v0.12.1.
9. Verify installed `Trace.exe` hash matches the expected v0.12.1 native payload.
10. Launch the updated installed copy.
11. Verify representative research data remains.
12. Verify coding references remain.
13. Verify participants remain.
14. Verify notes and memos remain.
15. Verify themes remain.
16. Verify backups remain.
17. Uninstall through the new branded setup.
18. Verify research data remains after uninstall.

Also add focused scenarios where practical:

- update while previous Trace is running
- same-version repair
- custom install directory
- locked application file
- missing application file
- stale previous installer metadata

A failure in upgrade CI must block release.

---

## 27. Preserve the v0.12 regression suite

The v0.12.1 pipeline must continue to run the existing research-feature tests.

Do not replace comprehensive tests with only visual checks.

Required categories:

- JavaScript syntax
- schema migration contract
- Office/survey import regression
- display/usability regression
- transcription regression
- PDF text regression
- v0.12 analysis/intercoder contract
- kappa math fixtures
- Rust compile
- Rust unit tests
- native Windows build

---

# PART V: MANUAL QA

## 28. Real-machine QA checklist

Before release, test the actual installer on a normal Windows machine, not only CI.

At minimum:

- [ ] Fresh install.
- [ ] Upgrade from the previous real installed version.
- [ ] Update while Trace is initially open.
- [ ] Repair same version if supported.
- [ ] Launch updated app.
- [ ] Open an existing project.
- [ ] Import DOCX.
- [ ] Import PDF.
- [ ] Import CSV/XLSX.
- [ ] Import audio.
- [ ] Import video.
- [ ] Transcribe audio.
- [ ] Create code.
- [ ] Apply coding.
- [ ] Undo and redo.
- [ ] Create second coder.
- [ ] Run intercoder comparison.
- [ ] Create or edit themes.
- [ ] Run participant x code matrix.
- [ ] Run co-occurrence.
- [ ] Run negative-case analysis.
- [ ] Run group comparison.
- [ ] Export analysis CSV.
- [ ] Create note.
- [ ] Create memo.
- [ ] Backup project.
- [ ] Force an abnormal close.
- [ ] Reopen and verify recovery.
- [ ] Uninstall.
- [ ] Verify project files still exist.

Also visually inspect Data, Code, Themes, Analyse, and Write at the supported DPI and resolution matrix.

---

# PART VI: RELEASE PIPELINE

## 29. v0.12.1 release workflow requirements

The final release workflow must use an actual Windows runner and must verify the exact installer users receive.

Required sequence:

1. Start from a proven v0.12.1 source checkpoint.
2. Run source and regression contracts.
3. Compile native Windows Trace.
4. Run Rust tests.
5. Produce the native Tauri NSIS installer.
6. Verify the native payload is a credible Windows executable.
7. Embed that exact native installer payload in the branded setup shell.
8. Build the branded `TraceSetup.exe`.
9. Calculate installer SHA-256.
10. Perform clean-install verification.
11. Perform upgrade verification from a previous installed release.
12. Hash the installed executable and compare it with the expected native payload.
13. Launch the installed copy.
14. Keep it alive long enough to detect immediate startup failure.
15. Uninstall the exact branded installation.
16. Verify research-data sentinels remain.
17. Produce a human-readable final verification file.
18. Upload release artifacts.

Release artifact should include at least:

- `TraceSetup.exe`
- `SHA256.txt`
- `FINAL-VERIFICATION.txt`
- native `Trace.exe`
- native installer artifacts useful for equivalence verification

Do not call the release complete if any required verification step is skipped, cancelled, or only inferred.

---

## 30. Expected final verification record

The final verification record should explicitly state booleans or equivalent evidence for:

- source checkpoint green
- previous regression contracts green
- v0.12.1 UX contracts green
- native build green
- native tests green
- generated NSIS payload verified
- branded setup built
- clean install green
- upgrade install green
- installed executable matches expected native payload
- installed copy launched
- installed copy remained running through launch smoke test
- exact branded uninstall green
- research data preserved
- version metadata consistent
- no stale 0.9.0 UI version

---

# PART VII: AGENT WORKFLOW

## 31. How an agent should pick up this project

Follow this order.

### Step 1: Read context

Read:

- this `AGENTS.md`
- `README.md`
- current v0.12 analysis workflow
- current Windows final workflow
- current build-status files

### Step 2: Establish baseline

Reconstruct or retrieve the exact green v0.12 source.

Run existing tests before making changes.

Do not debug a new failure until you know whether it existed before your change.

### Step 3: Work one phase at a time

Recommended implementation order:

1. installer diagnostics
2. maintenance/update reliability
3. version unification
4. installer typography/layout
5. global app typography
6. bottom dock and stray-line bugs
7. Code workspace
8. Data workspace
9. Themes/Analyse/Write hardening
10. accessibility/responsive matrix
11. visual regression tests
12. upgrade CI
13. manual QA
14. exact final release

### Step 4: Add tests with fixes

Every bug fix should include a test or contract capable of detecting recurrence where practical.

Examples:

- stale version string -> version consistency test
- clipped inspector tabs -> layout/overflow test
- bottom dock overlap -> reserved-space assertion
- upgrade failure -> previous-version upgrade CI
- empty participant punctuation -> rendered-state test

### Step 5: Keep changes reviewable

Prefer focused commits grouped by problem rather than one giant opaque patch.

Suggested commit categories:

- `fix(installer): ...`
- `fix(ui): ...`
- `refactor(styles): ...`
- `test(ui): ...`
- `test(installer): ...`
- `ci: ...`
- `docs: ...`

### Step 6: Do not declare success from local source checks alone

Source green is an intermediate milestone.

Windows native install and upgrade verification are the release gate.

---

## 32. What agents must not do

- Do not start major v0.13 AI work before v0.12.1 is green.
- Do not replace the entire UI architecture unnecessarily.
- Do not abandon `Data -> Code -> Themes -> Analyse -> Write`.
- Do not make text smaller to solve overflow.
- Do not hide an overlap behind another overlay.
- Do not remove research features just to simplify onboarding.
- Do not delete project data during uninstall tests.
- Do not silently introduce cloud dependency into core workflows.
- Do not treat source ZIPs or scaffolding as the final deliverable.
- Do not use a mock installer payload in final verification.
- Do not claim update support unless an actual previous installed version has been upgraded successfully.
- Do not weaken existing v0.12 tests to make a new build pass.
- Do not suppress installer errors without preserving actionable diagnostics.
- Do not expose research content in logs.

---

## 33. UX decision rules

When uncertain, use these rules.

### If two controls compete for attention

Prioritize the control needed for the user's current task. Move the advanced option to secondary styling, an overflow menu, or progressive disclosure.

### If text does not fit

Fix layout or allow intentional wrapping. Do not immediately shrink the font.

### If a panel needs horizontal scrolling for its own navigation

Treat that as a layout defect unless the content itself is inherently wide, such as a matrix.

### If a fixed/floating element covers content

The layout must reserve its space. Do not rely on users scrolling content behind it.

### If data is missing

Hide absent metadata instead of displaying placeholder punctuation.

### If an operation fails

Tell the user what happened, whether their project is safe, and what they can do next.

### If an advanced research term is unavoidable

Use plain-language explanation nearby. Trace should support expert work without requiring every user to already speak QDA software jargon.

---

## 34. UX success criteria

The hardening effort should move Trace toward these qualities:

- readable for hours
- calm rather than crowded
- obvious first actions
- advanced features available without overwhelming onboarding
- no hidden or overlapping content
- predictable navigation
- helpful empty states
- recoverable failures
- safe project handling
- reliable update behavior
- strong keyboard and DPI behavior

A new researcher should understand the basic workflow without reading a manual.

An experienced qualitative researcher should still be able to reach advanced tools quickly.

---

## 35. Progress ledger

Agents should update this section only when a phase is demonstrably completed and its acceptance tests are green.

Current status at creation of this guide:

- [x] v0.12 source gate verified
- [x] v0.12 exact Windows clean-install release verified
- [x] v0.12 native app launch verified in CI
- [x] v0.12 uninstall data-preservation sentinel verified in CI
- [ ] v0.12.1 source baseline prepared
- [ ] 9 percent maintenance failure diagnosed
- [ ] maintenance/update reliability fixed
- [ ] installer version authority unified
- [ ] installer typography/layout hardened
- [ ] global application typography hardened
- [ ] bottom dock overlap fixed
- [ ] stray blue/green line bug fixed
- [ ] Code workspace hardened
- [ ] Data workspace simplified
- [ ] Themes/Analyse/Write hardening complete
- [ ] accessibility and DPI matrix green
- [ ] visual regression tests green
- [ ] previous-version upgrade CI green
- [ ] real-machine manual QA green
- [ ] exact v0.12.1 Windows release green

---

## 36. Handoff requirements

Before handing work to another agent, leave enough evidence for the next agent to continue without rediscovering the state.

Record:

- branch and commit SHA
- phase being worked on
- tests run
- tests passing
- tests failing
- exact failure logs or error codes
- workflow run IDs
- artifact names
- known unresolved issues
- any intentional deviations from this guide and why

If a CI run fails, do not merely say `CI failed`. Name the exact step and error.

If a release is green, record the exact installer SHA-256 and verification run ID.

---

## 37. Final release rule

Trace v0.12.1 is complete only when the release pipeline proves both of these realities:

1. A new user can install and use Trace cleanly.
2. An existing user can update Trace without losing research work.

Anything less is an intermediate build.
