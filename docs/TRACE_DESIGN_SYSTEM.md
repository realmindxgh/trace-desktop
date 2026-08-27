# Trace Design System

This document is the normative UI system for Trace UX Foundation. It exists so agents do not redesign individual screens independently or infer product rules from whichever CSS selector they happen to find first.

The governing product rule is simple: **research material is more important than Trace's interface**. The interface must stay calm, truthful and legible while making the researcher's current evidence, location and next useful action obvious.

## 1. Desktop shell

The canonical shell is:

`Navigation rail | Context pane | Main workspace | Inspector`

- The navigation rail owns major modes: Home, Data, Code, Themes, Analyse, Write and contextual Trace AI access.
- The context pane changes with the active major mode. It must not become a second global navigation system.
- The main workspace owns the research material and receives the largest share of available space.
- The inspector follows the current selection and is resizable/collapsible.
- Document/source tabs belong immediately above the research material, not in the global top bar.
- Source identity belongs in the dedicated workspace identity strip and must never overlap the document tabs.
- Do not restore the historical floating bottom dock.
- Do not create a second rounded 'app window' inside the native Windows frame.

## 2. Information hierarchy

Permanent visual priority, highest to lowest:

1. Active research material or active research task.
2. Current source/theme/code/analysis/writing identity.
3. Primary action for the current state.
4. Context navigation and inspector information.
5. Project/global status and secondary metadata.
6. Decorative treatment.

If a lower-priority element competes visually with a higher-priority element, reduce the lower-priority element.

## 3. Typography

Trace must remain readable at standard Windows scaling without relying on the operating system to repair tiny UI text.

- Page/workspace headings: approximately 28-32 px equivalent.
- Section headings: approximately 20-24 px.
- Standard controls and interface body: 15-16 px.
- Research reading/transcript text: 16-18 px with generous line height.
- Secondary labels: 13-14 px.
- Absolute meaningful-text floor: 12 px.
- Do not use microcopy below 12 px for actionable, explanatory or status information.
- Use weight and spacing before adding more font sizes.
- Long research text should favour comfortable line height and measure over dense dashboard-style packing.

Application Settings exposes Compact, Comfortable and Large interface size modes. Density may alter spacing and control height, but must not violate the 12 px floor.

## 4. Spacing

Use a small shared spacing scale rather than arbitrary one-off gaps. Preferred increments are 4, 8, 12, 16, 20, 24 and 32 px.

- 4-8 px: tightly related inline elements.
- 12-16 px: controls within one functional group.
- 20-24 px: separation between groups/sections.
- 32 px or more: major workspace boundaries and empty-state breathing room.

Whitespace must communicate structure. Do not fill empty space with statistics, cards or decoration simply because room exists.

## 5. Surfaces, borders and shadows

Trace is a native research application, not a SaaS dashboard.

- Prefer flat workspace surfaces with subtle tonal separation.
- Use borders only when they communicate an actual boundary, selection or input affordance.
- Do not outline every panel, card, search box and region simultaneously.
- Cards are reserved for self-contained information or choices, not every block of content.
- Shadows should be rare and shallow. Use them for floating menus/dialogs where depth explains interaction.
- Decorative lines must never run behind research content.
- Colour is semantic, not ornamental.

## 6. Corner radii

Rounded rectangles are structural tools, not the default shape of every object.

- Inputs/buttons: modest consistent radius.
- Menus/dialogs: modest radius sufficient to distinguish floating layers.
- Major workspace/pane containers: normally square or minimally rounded because the native window already provides the outer container.
- Do not wrap the entire application in a giant rounded rectangle.

## 7. Colour

Colour may communicate:

- active mode/selection,
- code identity,
- status/severity,
- focus,
- progress,
- destructive action.

Do not use colour solely to make structural chrome more noticeable. Never rely on colour alone for state; use text, iconography, shape or placement as a second signal.

## 8. Icons

- Familiar icons may accompany labels.
- Unfamiliar actions require text labels or tooltips.
- Core research actions must not be icon-only mystery controls.
- Trace AI must be named `Trace AI` or `Assistant`; sparkle iconography may support the label but may not replace it.
- Keep icon sizing consistent within each control class.

## 9. Buttons and actions

- One clear primary action per immediate state when possible.
- Secondary actions should visually recede.
- Destructive actions use destructive styling and explicit consequence copy.
- Retry is shown only when retrying can plausibly fix the problem.
- Disable unavailable actions only when the disabled state remains understandable; otherwise hide controls that are meaningless in the current state.

## 10. Context panes

Context panes are mode-specific:

- Data: Sources, Participants/Cases, Attributes, Collections/Sets and Imports.
- Code: code system/tree, code search/filtering and compact source launcher when useful.
- Themes: theme structures, linked codes/evidence and relationships.
- Analyse: queries/tools, saved analyses and results.
- Write: findings/writing documents, evidence targets and export actions.

The context pane must remain useful at large-project scale. Lists require filtering/search/hierarchy where the object count can become large.

## 11. Inspector

- Default practical width: roughly 320-440 px where the window permits.
- Resizable within safe bounds; current implementation uses remembered bounded width.
- Collapsible without losing the researcher's place.
- Pane size is remembered only when `Remember my layout` is enabled.
- Inspector tabs are Details, Codes, Notes and Memos.
- Counts are badges, not long tab labels.
- Inspector tabs must never require a horizontal scrollbar. Lower-priority actions move into `More` where needed.
- Inspector content follows the selected source, passage, code, participant/case, theme or analysis result.

## 12. Tabs and source identity

- Multiple open research sources use document/source tabs.
- Active tab must be unmistakable without relying only on colour.
- The source identity strip may show mode/source context but must remain physically separate from tabs.
- Closing/switching tabs must not silently change project-level state.
- `Resume exactly where I was` controls restoration of transient source/workspace state independently from layout-memory preferences.

## 13. Empty states

Use one reusable pattern:

- concise title stating the true state,
- one sentence explaining why the area is empty or what it is for,
- one primary next action,
- optional secondary action.

Examples:

- `No sources yet` rather than `No matching sources` when no filter exists.
- `Create your first code or code a passage to get started.`
- Themes explain the relationship between organised codes and themes.
- Analyse exposes available query/analysis choices.
- Write offers a findings/report/evidence-based starting action.

Never fabricate participant/source UI to make an empty state look populated.

## 14. Loading and progress

Long operations must describe what Trace is doing:

- importing files,
- extracting PDF text,
- transcribing media,
- running analysis,
- exporting,
- backup/recovery/migration.

Prefer task-specific progress text to generic indefinite spinners. A spinner may accompany useful progress copy but must not be the only feedback.

## 15. Errors

Use the shared human/actionable error pattern:

1. plain-language description,
2. useful recovery action when one exists,
3. `Technical details` disclosure for developer/framework information.

Rust, Tauri, database/plugin names and stack-oriented details must not be the primary message shown to researchers.

## 16. Destructive confirmations

Confirmations must preview research consequences rather than asking generic `Are you sure?` questions.

Depending on the object, disclose effects on:

- coded passages/media coding,
- annotations,
- notes/memos,
- evidence anchors,
- participant/case relationships,
- collections/sets,
- theme/code relationships.

Retranscription of coded/annotated material requires explicit research-protection explanation.

## 17. Dialogs and context menus

Dialogs:

- consistent title/body/action hierarchy,
- primary action in a predictable location,
- Escape closes non-destructive dialogs where safe,
- focus is trapped while modal,
- first destructive action is never accidentally focused as the default.

Context menus:

- one reusable implementation,
- mouse and keyboard accessible,
- closes on Escape/click-away/action,
- appears only for high-frequency contextual actions,
- does not become the only way to discover core beginner actions.

## 18. Keyboard and focus

Current productivity standard includes:

- `Ctrl+K`: command palette,
- `Ctrl+Shift+C`: new code,
- `Ctrl+Shift+M`: new memo,
- `Ctrl+Shift+I`: import,
- `Alt+Left/Right`: previous/next source tab,
- native undo/redo shortcuts where applicable.

Shortcuts must be discoverable in menus/tooltips/Application Settings. Every interactive control requires a visible keyboard focus state.

## 19. Search

Search is contextual:

- project-wide search,
- current-source search,
- code search,
- participant/case filtering,
- theme/analysis navigation.

Do not show transcript search when no transcript exists. Labels/placeholders must make search scope obvious.

## 20. Import UX

Import distinguishes documents/PDFs, spreadsheets/surveys, audio/video and qualitative-project imports where supported.

- Drag/drop and multi-file import remain first-class.
- Completed batches show aggregate outcomes.
- Partial failures identify the specific files needing attention.
- Completion offers useful next actions such as Open first source, Review participants and Begin coding.
- Media import produces a non-blocking next-action choice: `Transcribe now` or `Add without transcription`.
- Local transcription states that processing happens locally.
- Application Settings owns default transcription language/model; per-job choices may override them.

## 21. Project versus application settings

Project Settings owns project-specific research state such as metadata, participant/case terminology, backup/recovery preferences and export behaviour.

Application Settings owns UI appearance/size, shortcuts, layout/workspace-resume preferences, default transcription settings and application/update behaviour.

Do not mix the two scopes.

## 22. Responsive behaviour

Trace must adapt at realistic desktop sizes rather than shrinking text until it fits.

Required automated coverage includes:

- common workstation viewport,
- 1366x768 laptop viewport,
- 100%, 125% and 150% Windows scaling where practical,
- maximised and non-maximised conditions.

At constrained widths:

- preserve research content,
- collapse/move lower-priority inspector controls,
- keep major navigation usable,
- avoid root horizontal overflow,
- never allow inspector tabs or source identity to collide with neighbouring UI.

## 23. Accessibility

- Semantic accessible names for controls.
- Visible focus states.
- Keyboard traversal of primary workflows.
- Contrast appropriate to text/control importance.
- Active/status information not communicated by colour alone.
- Resizable panes expose keyboard alternatives where practical.
- Screen-reader labels reflect researcher-facing terminology, not implementation jargon.

## 24. AI

Trace AI is contextual assistance, not the product's visual centre.

- It follows the current task/source/theme/write context.
- It must not fabricate output when no provider is configured.
- It must preserve provenance and distinguish researcher decisions from generated suggestions.
- Research evidence remains visually dominant.

## 25. Visual-regression contract

Every release candidate must capture deterministic evidence for at least:

- Home,
- empty project,
- Data,
- Code with visible coding,
- Themes,
- Analyse,
- Write,
- Code at laptop size/125% scaling.

The gate combines structural assertions (overflow, font floor, collisions, pane visibility) with perceptual image fingerprints against an explicitly approved baseline. Baseline changes require an intentional reviewed update, never silent regeneration during CI.

## 26. Change rule

New UI work should use existing primitives and rules first. If a new pattern is genuinely required:

1. define the reusable behaviour,
2. add/update the design-system rule,
3. implement the shared primitive,
4. add rendered/regression coverage,
5. only then use it in individual workspaces.

A screen-specific CSS patch that contradicts this document is not considered a completed UX fix.
