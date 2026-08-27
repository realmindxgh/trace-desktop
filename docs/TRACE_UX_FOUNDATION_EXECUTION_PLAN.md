# Trace UX Foundation Execution Plan

This plan executes the 240-point master contract in `AGENTS.md` on top of the exact verified Trace v0.12.1 engineering baseline. The research engine, data model, analysis mathematics, imports, transcription, PDF support, recovery and installer safety remain regression-protected throughout.

## Baseline

- Exact source gate: run `32723424461`
- Source artifact: `Trace-v0.12.1-Full-Checklist-Green-Source`
- Source artifact digest: `sha256:dad38e53e5149190d97c65762cb4362accc84467f38c1b59c2aa97216cca123e`
- Verified Windows release: run `32724433832`
- Final v0.12.1 `TraceSetup.exe` SHA-256: `262186eea6ca1dc70c267ac81278cd0f77960e4a7525cc62b0d8ffbaeb0ba77d`
- UX development branch: `trace-ux-foundation-v2`

## Execution model

The programme is one continuous development pass, but changes are landed in gated slices rather than one opaque commit. Each slice must preserve all previously green research contracts. A later phase may refine an earlier phase, but no phase may silently weaken the master contract.

### Phase 1. Production-state hygiene, Home and first launch

Implement truthful fresh-launch state, Trace Home, recent projects, explicit resume preference, recovery entry points, short project creation, Project Overview for empty projects, and zero-data truthfulness. Eliminate phantom participants, injected demo state and source-specific controls before a source exists.

Gate: a genuinely fresh launch shows Home, no test/demo project, no `P01`, and an empty project opens Overview with meaningful next actions.

### Phase 2. Navigation architecture and desktop shell

Replace the floating bottom dock with the permanent navigation rail and establish `Navigation rail | Context pane | Main workspace | Inspector`. Make active location, project identity and source identity unmistakable. Add desktop document tabs and contextual side panes.

Gate: one coherent navigation system, no competing dock, no ambiguous active mode, no content hidden by fixed chrome.

### Phase 3. Design system, typography and responsive behaviour

Establish shared spacing, type, surface, radius, control and pane rules. Remove dashboard-within-a-window styling, excessive borders and decorative competition. Keep all meaningful text readable at realistic Windows resolutions and scaling.

Gate: shared tokens and primitives, no important text below the readability floor, no root horizontal overflow or clipped primary navigation at the required matrix.

### Phase 4. Data, import, source and participant workflows

Redesign source organisation and import around real research material. Preserve multi-file import, drag/drop and existing formats. Add honest import summaries and next actions, distinguish documents/surveys/media/project imports, suppress absent participant metadata and prepare source navigation for large projects.

Gate: empty, importing, successful, partial-failure and populated states are all truthful and actionable.

### Phase 5. Code, Themes, Analyse and Write

Rework every core mode inside the shared shell while preserving the verified research engine. The research material must dominate. Improve code navigation, contextual inspector behaviour, theme evidence inspection, analysis query navigation and evidence-based writing states.

Gate: complete researcher flow from opened source through coding, themes, analysis and writing is usable without navigation ambiguity or dead-end empty states.

### Phase 6. Contextual Trace AI

Move AI from a visually dominant mystery control to contextual assistance that follows the active task. Do not fabricate AI output when no provider is configured. Keep evidence and researcher decisions visually primary.

Gate: AI is clearly named, contextual, subordinate to research material, and explicit about availability/provenance.

### Phase 7. Productivity, accessibility and interaction polish

Add command palette, useful keyboard shortcuts, contextual search, visible focus, accessible pane controls, human error states, destructive-action previews, tooltips and consistent dialogs/context menus.

Gate: primary workflows are keyboard-reachable, destructive actions are protected, error messages are actionable, and controls have accessible names/states.

### Phase 8. Release and visual regression gates

Expand CI from engineering correctness to product truth. Test first launch, empty project, populated source, every major mode, realistic viewports/scaling, project reopen/recovery, and exact Windows install/launch. Preserve all previous v0.12.1 release and data-safety gates.

Gate: automated source/browser/native/Windows gates green, followed by physical UAT on the actual user machine for visual/readability and real-file end-to-end acceptance.

## Required end-to-end acceptance journey

`create project -> import data -> organise participants -> code passages -> create notes/memos -> build themes -> analyse -> write/export -> close -> reopen -> recover/backup`

This journey must be exercised with realistic transcripts, PDFs, spreadsheets and media. Empty/demo fixtures alone are not sufficient for final acceptance.

## Progress rule

`PROGRESS.md` is the live ledger. Every material phase completion must record the branch/commit, tests, CI run IDs, artifacts, known defects and exact continuation point. The UX programme is not complete merely because the v0.12.1 engineering checklist remains green.
