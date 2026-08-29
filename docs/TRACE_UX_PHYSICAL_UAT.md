# Trace UX Foundation Physical Windows UAT

This procedure is the final human acceptance boundary for the Trace UX Foundation programme. Automated source, browser, visual, native-build and installed-Windows acceptance must be green first. A green CI run does **not** replace this physical UAT.

## Release boundary

Until every required check below is completed and recorded:

- keep `physical_real_machine_uat=false`;
- keep the Windows acceptance build labelled `ACCEPTANCE_BUILD_NOT_FINAL_RELEASE`;
- do not describe the 240-point UX contract as finally accepted;
- do not promote the installer as a final public release.

## Candidate identity

Record before testing:

- Windows acceptance run ID:
- Control SHA:
- Source gate run ID:
- Source gate SHA:
- Source artifact digest:
- `TraceSetup.exe` SHA-256:
- Installed `Trace.exe` SHA-256:
- Test machine and Windows version:
- Display resolution:
- Test date:
- Tester:

The installer SHA-256 must match the value in `UX-WINDOWS-ACCEPTANCE.txt` from the exact acceptance artifact being tested.

## 1. Clean-install and first-launch truth

1. Uninstall any earlier Trace test build.
2. Confirm no Trace process remains running.
3. Install the exact Windows acceptance `TraceSetup.exe`.
4. Launch Trace normally from the installed application, not from source or a development server.
5. Confirm the first screen is Trace Home.
6. Confirm no development, demo or fixture project appears automatically.
7. Confirm `Downloading Videos`, `P01`, or any other phantom research state is absent.
8. Confirm Home clearly exposes New Project, Open Project, Import Project and Recover from backup.
9. Confirm a first-time user can understand what Trace is for and how to begin without prior Trace knowledge.

Result: PASS / FAIL
Notes:

## 2. Empty-project truth and orientation

1. Create a new project using only a project name and optional description.
2. Confirm the project opens to Project Overview, not directly to Code.
3. Confirm the empty state explains what to do next.
4. Confirm no participant card, fake avatar, participant metadata, transcript search, source-specific inspector content or other nonexistent state is rendered.
5. Confirm Data, Code, Themes, Analyse and Write each present a purposeful empty/default state.
6. Confirm the research journey is understandable without being presented as gamification.

Result: PASS / FAIL
Notes:

## 3. Desktop shell and navigation

1. Confirm the permanent navigation rail is the only primary mode-navigation system.
2. Confirm the active major mode is unmistakable.
3. Confirm the contextual left pane changes appropriately between Data, Code, Themes, Analyse and Write.
4. Confirm the main research material dominates the workspace when a source is open.
5. Confirm the right inspector can be resized and collapsed.
6. Confirm inspector tabs never require a horizontal scrollbar.
7. Confirm document/source identity remains obvious while navigating.
8. Open multiple sources and confirm the active source/tab is unmistakable.
9. Confirm no persistent floating control obstructs research material.

Result: PASS / FAIL
Notes:

## 4. Readability, visual hierarchy and Windows scaling

Repeat the core shell inspection at each practical Windows display scale available on the machine: 100%, 125% and 150%.

For each scale:

1. Test maximised and non-maximised windows.
2. Test a laptop-like window size around 1366×768 where practical.
3. Confirm normal interface text is comfortably readable.
4. Confirm transcript/document reading text is comfortably readable.
5. Confirm no meaningful control, label, tab, inspector content or primary action is clipped.
6. Confirm there is no root horizontal interface overflow.
7. Confirm the interface adapts by layout rather than collapsing into tiny text.
8. Confirm borders, cards, radii and decorative elements do not visually compete with evidence.
9. Confirm no coloured/decorative lines cross through or beneath the research workspace.
10. Confirm Trace feels coherent as Windows research software rather than a web dashboard inside another frame.

Result: PASS / FAIL
Notes:

## 5. Real-file import and organisation

Use representative researcher-owned or disposable test copies of real files. Include at least:

- one transcript/text document;
- one searchable PDF;
- one spreadsheet/survey with participant/case attributes;
- one audio or video file supported by Trace.

Then verify:

1. Drag/drop and explicit import are understandable.
2. Import distinguishes the relevant file/workflow types.
3. Import progress says what Trace is doing.
4. Completion accurately summarises successes and files needing attention.
5. Completion offers useful next actions such as Open first source, Review participants and Begin coding.
6. Spreadsheet participant/case data and attributes are represented truthfully.
7. Missing participant metadata disappears instead of becoming chains of placeholder dashes.
8. Audio/video import offers Transcribe now and Add without transcription.
9. Local transcription wording clearly communicates local processing.
10. Source, participant and collection terminology remains consistent.

Result: PASS / FAIL
Notes:

## 6. Researcher journey

Using the populated project:

1. Open a transcript/source.
2. Select evidence and create/apply at least two codes.
3. Create a source/project memo or note.
4. Create a theme from coded evidence.
5. Inspect the theme and its evidence relationships.
6. Open Analyse and exercise at least one meaningful analysis/query path available for the project.
7. Open Write and create/save findings linked to the project evidence.
8. Export findings and open the exported file outside Trace.
9. Confirm the export identifies the correct project and preserves the expected findings text.
10. Confirm the interface remains oriented around evidence and researcher decisions throughout.

Result: PASS / FAIL
Notes:

## 7. Close, reopen and workspace memory

1. Return to Home with the populated project available to resume.
2. Close Trace completely.
3. Reopen Trace normally.
4. Confirm default startup returns to Home unless the explicit auto-resume preference was enabled.
5. Resume the project.
6. Confirm sources, participants/attributes, coding, notes/memos, themes and findings remain intact.
7. Confirm remembered pane layout and exact-workspace-resume behaviour obey their separate preferences.
8. Confirm no confusing transient selection is restored when exact resume is disabled.

Result: PASS / FAIL
Notes:

## 8. Backup, restore and recovery trust

1. Create a verified backup from the populated project.
2. Confirm backup/protection status is understandable.
3. Start restore and read the consequence/confirmation copy before proceeding.
4. Confirm Trace explains that the current project remains safe when restoration creates a recovered copy.
5. Restore the backup.
6. Confirm the restored copy retains imported sources, participant attributes, coding, notes/memos, themes and findings.
7. Exercise Recover from backup from Home where practical.
8. If a recent-project location is deliberately made unavailable, confirm Trace offers sensible recovery actions rather than broken placeholders.

Result: PASS / FAIL
Notes:

## 9. Keyboard, focus and accessibility inspection

1. Navigate primary controls with the keyboard.
2. Confirm visible keyboard focus is never lost against the background.
3. Exercise Ctrl+K command palette.
4. Exercise Create code, memo and search shortcuts shown by the application.
5. Confirm tooltips/menus expose useful shortcuts.
6. Confirm active state is not communicated by colour alone.
7. Confirm pane collapse/resize controls are keyboard-reachable where implemented.
8. Confirm unfamiliar icons have labels or meaningful tooltips.
9. Confirm dialogs have sensible focus order, Escape/close behaviour and clear primary/destructive actions.
10. Confirm context menus can be opened and navigated without a mouse where supported.

Result: PASS / FAIL
Notes:

## 10. Human error and destructive-action inspection

Exercise safe disposable cases for the following where practical:

1. unsupported or damaged import;
2. missing recent project;
3. delete a coded source;
4. retranscribe coded/annotated material;
5. merge/delete a code or theme;
6. a failed or unavailable operation that legitimately supports Retry.

Confirm plain-language consequences/recovery appear first and implementation details remain behind Technical details. Raw Rust, Tauri, SQLite/database or plugin terminology must not be the primary user-facing error.

Result: PASS / FAIL
Notes:

## 11. Calmness and research-material priority

Inspect Home, Overview, Data, Code, Themes, Analyse and Write after actual use, not only empty states.

Confirm:

- research material remains more visually important than application chrome;
- Trace AI is named, contextual and subordinate to the research workflow;
- permanent statistics are useful rather than decorative;
- colour communicates meaning/status rather than decorating the shell;
- navigation, source identity and next actions remain clear without visual noise;
- no overlap, tiny text, clipped controls, unexpected horizontal scrollbars or obviously broken geometry is visible.

Result: PASS / FAIL
Notes:

## 12. Final sign-off

A physical-UAT PASS requires every required section above to pass or to have a documented, explicitly accepted non-blocking deviation. Any defect that contradicts research data, risks project loss, blocks a core researcher step, makes primary text unreadable, breaks common display sizes, or causes obviously broken geometry is blocking.

Final result: PASS / FAIL

Blocking defects:

Accepted non-blocking deviations:

Tester sign-off:

Date:

After a PASS, record the exact acceptance run and installer hash in the project progress ledger, update the 240-point closure matrix, and only then change `physical_real_machine_uat` from `false` to `true` in the final release acceptance record.