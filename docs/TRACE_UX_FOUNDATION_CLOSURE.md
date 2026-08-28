# Trace UX Foundation 240-Point Closure Ledger

This is the item-by-item acceptance ledger for the master contract in `AGENTS.md`.

It deliberately separates **implementation/automated evidence** from **physical real-machine UAT**. A green source gate or attractive screenshot is not sufficient to close the Trace UX Foundation.

## Candidate under acceptance

- Branch: `trace-ux-foundation-v2`
- Strict green source gate: `33152414998`
- Source SHA: `69b5f788f6b5723140efcc1e9fe970191e2225a3`
- Green source artifact: `Trace-UX-Foundation-v2-Green-Source`
- Green source artifact digest: `sha256:510adf1546f00b5160ed530adfa57d51c14b01eaf945776e6b7db732c7104787`
- Reviewed visual reference run: `33117906540`
- Reviewed visual artifact digest: `sha256:20bf964fef8ab8721d5d89c0b2b0d77c3781bb9ec1712bd5effcef6eb2c63e93`
- Windows acceptance run: `33154626340` (`IN PROGRESS` when this ledger was created)
- Physical real-machine UAT: issue #5 (`PENDING`)

## Evidence codes

- **S** = implemented and accepted by strict source/research/browser contract run `33152414998`.
- **V** = accepted by reviewed screenshots, structural geometry/DPI checks and strict perceptual visual regression.
- **L** = accepted by large-project/performance regression, including the carried 500-source / 10,000-reference workload contract.
- **R** = accepted by inherited research-engine/data-preservation regressions from the exact verified v0.12.1 baseline and rerun in the UX source gate.
- **W** = must be accepted by the exact installed Windows acceptance build. Run `33154626340` is the current candidate.
- **P** = final judgement also requires physical real-machine UAT on issue #5.
- **RESOLVED** = the requirement was intentionally resolved rather than implemented literally, for example an optional feature that should exist only if its underlying capability is shipped.

A row is not finally closed while its `Remaining` column contains `W` or `P`.

## Items 1–30: first launch, Home and truthful state

| # | Closure | Evidence | Remaining |
|---:|---|---|---|
| 1 | Deliberate first-launch experience replaces unexplained Code launch. | S,V | W,P |
| 2 | Production-state hygiene removes `Downloading Videos`/fixture contamination. | S,V | W,P |
| 3 | Phantom `P01`/zero-participant contradiction removed, including REFI-QDA fallback. | S,V | W,P |
| 4 | Fresh installs default to Trace Home unless explicit resume preference is enabled. | S,V | W,P |
| 5 | Welcome/Home explains Trace and exposes clear starting actions. | S,V | W,P |
| 6 | No sample is auto-injected. Optional sample remains conditional on a real shipped sample. | S,RESOLVED | P |
| 7 | Recover from backup is visible on Home. | S,V | W,P |
| 8 | Lightweight optional Getting Started experience implemented. | S | P |
| 9 | Getting Started tracks project/import/code/memo/theme milestones and can disappear when complete. | S | P |
| 10 | Home remains the persistent project launcher after onboarding. | S,V | W,P |
| 11 | Home exposes recent projects with useful recency/project information. | S,V | W,P |
| 12 | New/Open/Import/Recover are prominent Home actions. | S,V | W,P |
| 13 | Explicit startup resume preference implemented. | S | W,P |
| 14 | New Project flow is intentionally short. | S,V | W,P |
| 15 | Essential project creation is name plus optional description. | S,V | W,P |
| 16 | Methodology/research/institution metadata moved to Project Settings. | S | W,P |
| 17 | Empty project opens Project Overview rather than Code. | S,V | W,P |
| 18 | Project Overview has a purposeful truthful empty state. | S,V | W,P |
| 19 | Empty project exposes import/transcription/project-import next actions. | S,V | W,P |
| 20 | Supported input types are surfaced without dominating the empty state. | S,V | P |
| 21 | Participant UI is absent when there is no participant. | S,V | W,P |
| 22 | Transcript controls are absent/inactive without a transcript. | S,V | W,P |
| 23 | Source-specific inspector content is absent before a source exists. | S,V | W,P |
| 24 | Unfiltered empty source state says `No sources yet`, not `No matching sources`. | S,V | W,P |
| 25 | Shared empty states teach the next useful action. | S,V | P |
| 26 | Code empty state explains how to create/apply the first code. | S,V | P |
| 27 | Themes empty state explains progression from organised codes. | S,V | P |
| 28 | Analyse empty state presents available analysis/query choices. | S,V | P |
| 29 | Write empty state offers findings/report/evidence starting actions. | S,V | P |
| 30 | Counts, source, participant, inspector and navigation state are cross-checked for truthfulness. | S,V,R | W,P |

## Items 31–91: desktop shell, Data architecture, import, inspector and settings

| # | Closure | Evidence | Remaining |
|---:|---|---|---|
| 31 | Empty whitespace was reduced in favour of working context/research content. | S,V | P |
| 32 | Main research material owns the dominant workspace. | S,V | P |
| 33 | Navigation chrome was visually demoted relative to evidence. | S,V | P |
| 34 | Canonical shell is `Navigation rail | Context pane | Main workspace | Inspector`. | S,V | W,P |
| 35 | Giant floating bottom dock is no longer rendered by the new shell. | S,V | W,P |
| 36 | Data/Code/Themes/Analyse/Write remain the conceptual backbone. | S,V | W,P |
| 37 | Major modes live in a slim permanent left rail. | S,V | W,P |
| 38 | Active mode has an explicit non-ambiguous state. | S,V | W,P |
| 39 | Competing global navigation systems were removed from the visible shell. | S,V | W,P |
| 40 | Second left pane is mode-contextual. | S,V | W,P |
| 41 | Data context includes Sources, Participants/Cases, Collections/Sets, Attributes and Imports. | S,V | W,P |
| 42 | Code context is the code system/tree rather than a second source browser. | S,V | W,P |
| 43 | Themes context exposes theme structures/relationships. | S,V | W,P |
| 44 | Analyse context exposes analysis tools/queries/results. | S,V | W,P |
| 45 | Write context exposes writing/findings/evidence/export targets. | S,V | W,P |
| 46 | Data context was rebuilt beyond the old search/counts stub. | S,V | W,P |
| 47 | Source navigation now behaves as research-data navigation rather than a tiny web accordion. | S,V | P |
| 48 | Source architecture includes filtering/collections/attributes/sorting hooks for large projects. | S,L | P |
| 49 | Permanent Project Counts card removed from scarce context-pane space. | S,V | P |
| 50 | Useful project health/count information belongs on Overview rather than the source tree. | S,V | P |
| 51 | Import is the primary empty-project action. | S,V | W,P |
| 52 | Import is a first-class workflow rather than one generic button. | S | W,P |
| 53 | Import distinguishes documents/PDFs, spreadsheets/surveys, media and project/REFI-QDA inputs. | S,R | W,P |
| 54 | Drag/drop and multi-file import remain first-class. | S,R | P |
| 55 | Import batches produce truthful aggregate success/failure summaries. | S | W,P |
| 56 | Import completion offers Open first source / Review participants / Begin coding. | S | W,P |
| 57 | Media transcription is integrated as a first-class Data workflow. | S,R | W,P |
| 58 | Media import offers `Transcribe now` / `Add without transcription` without blocking the batch. | S | W,P |
| 59 | Language/model/progress controls are exposed; speaker workflow remains conditional on actual capability. | S,R,RESOLVED | W,P |
| 60 | Local transcription is explicitly described as local processing. | S,R | W,P |
| 61 | Participant header was simplified and cleaned up. | S,V | P |
| 62 | Missing participant fields disappear rather than rendering dash chains. | S,V | P |
| 63 | Participant profile UI appears only for genuinely linked participant data. | S | W,P |
| 64 | Participant metadata is compact and secondary to evidence. | S,V | P |
| 65 | Active source/document identity is visually prominent. | S,V | W,P |
| 66 | Multi-document/source tab model implemented. | S,V | W,P |
| 67 | Tabs support a professional multi-source desktop workflow. | S,V | W,P |
| 68 | Breadcrumb/source identity moved next to the workspace it describes. | S,V | W,P |
| 69 | Disconnected global-header breadcrumb removed from the visible navigation model. | S,V | W,P |
| 70 | Inspector width was increased to a realistic desktop range. | S,V | P |
| 71 | Inspector is bounded and resizable. | S,V | W,P |
| 72 | Inspector is collapsible. | S,V | W,P |
| 73 | Inspector tabs have explicit no-horizontal-scroll/collision regression checks. | S,V | W,P |
| 74 | Inspector tabs use Details / Codes / Notes / Memos terminology. | S,V | P |
| 75 | Counts use compact badges rather than bloated tab labels. | S,V | P |
| 76 | Narrow-width inspector behaviour moves/de-emphasises lower-priority controls instead of scrolling tabs. | S,V | P |
| 77 | Inspector follows active source/participant/code/theme/selection context. | S | W,P |
| 78 | Top bar responsibilities were reduced and separated. | S,V | P |
| 79 | Top bar now centres compact project identity, optional global command/search and save/settings actions. | S,V | P |
| 80 | Project title/header footprint reduced. | S,V | P |
| 81 | Old large project-title presentation replaced by compact project identity/switcher treatment. | S,V | P |
| 82 | Interactive project switching is presented with clear affordance rather than a tiny mystery indicator. | S,V | P |
| 83 | Undo/redo is contextual/shortcut-driven rather than permanently dominant while unavailable. | S,R | P |
| 84 | Persistent save state is calm `Saved` rather than noisy elapsed-time chrome. | S,V | W,P |
| 85 | Precise save/backup/project detail is available in contextual protection/details UI rather than the global badge. | S | P |
| 86 | Data confidence/protection is treated as a first-class UX concern. | S,R | W,P |
| 87 | Autosave/backup state is surfaced unobtrusively. | S | W,P |
| 88 | Protection/recovery UI exposes backup state and restore actions. | S,R | W,P |
| 89 | Project Settings and Application Settings are separate surfaces. | S,V | W,P |
| 90 | Project Settings owns project metadata, participant terminology, backup/research and export behaviour. | S | W,P |
| 91 | Application Settings owns appearance/size, shortcuts, transcription defaults, resume/layout and app preferences. | S | W,P |

## Items 92–123: typography, visual language and Trace AI

| # | Closure | Evidence | Remaining |
|---:|---|---|---|
| 92 | Tiny typography was replaced by a readable system. | S,V | P |
| 93 | Typography is token/system driven rather than isolated fixes. | S,V | P |
| 94 | Standard interface body text targets readable 15–16 px equivalents. | S,V | P |
| 95 | Secondary labels remain around the readable 13–14 px band with a hard 12 px meaningful-text floor. | S,V | P |
| 96 | Transcript/research reading text is larger with comfortable line height. | S,V | P |
| 97 | Compact / Comfortable / Large interface-size modes implemented. | S | W,P |
| 98 | Trace no longer depends on Windows scaling alone to rescue tiny UI text. | S,V | P |
| 99 | Heading/body/metadata/control hierarchy was strengthened. | S,V | P |
| 100 | Excessive outlines reduced. | S,V | P |
| 101 | Spacing/surfaces/typography replace unnecessary borders. | S,V | P |
| 102 | Bordered cards are reserved for genuinely bounded information/actions. | S,V | P |
| 103 | Rounded rectangles are no longer the default treatment for every region. | S,V | P |
| 104 | Corner radii are governed by the formal design system. | S,V | P |
| 105 | Giant rounded inner-app container removed from the new shell. | S,V | W,P |
| 106 | UI no longer simulates a browser/dashboard window inside the native window. | S,V | W,P |
| 107 | SaaS-dashboard visual language was deliberately reduced. | S,V | P |
| 108 | New shell follows a desktop research-tool visual language. | S,V | W,P |
| 109 | Double Trace branding was reduced. | S,V | P |
| 110 | Navigation/workspace now derive from one design system. | S,V | P |
| 111 | Formal shared design system covers nav, panes, controls, tabs, menus and surfaces. | S,V | P |
| 112 | Historical blue/green decorative/rendering lines are absent from the rebuilt workspace. | S,V | W,P |
| 113 | Decorative elements do not cross research content. | S,V | P |
| 114 | AI visual emphasis was reduced relative to the research workflow. | S,V | P |
| 115 | Mystery sparkle-only control is no longer the dominant action. | S,V | P |
| 116 | AI is explicitly named Trace AI / Assistant. | S,V | P |
| 117 | Trace AI is integrated into the navigation/context architecture. | S,V | W,P |
| 118 | AI follows current research task/context instead of acting as an isolated destination. | S | W,P |
| 119 | Transcript AI actions are source-contextual. | S | W,P |
| 120 | Theme AI actions are theme/code-contextual. | S | W,P |
| 121 | Write AI actions are evidence/writing-contextual. | S | W,P |
| 122 | Research evidence and researcher decisions remain visually dominant over AI. | S,V | P |
| 123 | Every major mode has a purposeful mode-specific default rather than a generic empty shell. | S,V | W,P |

## Items 124–180: research journey, productivity, trust, accessibility and scale

| # | Closure | Evidence | Remaining |
|---:|---|---|---|
| 124 | Data defaults to project/data organisation. | S,V | W,P |
| 125 | Code defaults to the code system/coding overview without an open source. | S,V | W,P |
| 126 | Themes defaults to theme organisation. | S,V | W,P |
| 127 | Analyse defaults to analysis/query choices/results. | S,V | W,P |
| 128 | Write defaults to writing/findings/evidence actions. | S,V | W,P |
| 129 | Research journey is legible across the product. | S,V | P |
| 130 | Bring data in → Organise → Code → Themes → Analyse → Write is the IA backbone. | S,V | P |
| 131 | Journey is embodied in context/default states, not just five buttons. | S,V | P |
| 132 | First coding activity can give a subtle next-step hint toward Themes. | S | P |
| 133 | Transition guidance is non-gamified. | S,V | P |
| 134 | Global Ctrl+K command palette implemented. | S | W,P |
| 135 | Palette exposes core import/code/search/memo/recent/export/participant-oriented actions as applicable. | S | W,P |
| 136 | Keyboard workflow is part of the product contract and automated interaction tests. | S | W,P |
| 137 | Common repetitive research actions have shortcuts. | S | W,P |
| 138 | Code/memo/import/source-switch/undo-redo/palette shortcuts are implemented. | S,R | W,P |
| 139 | Shortcut discoverability lives in menus/tooltips/Application Settings. | S | P |
| 140 | Search scopes are contextual rather than one ambiguous global field. | S | W,P |
| 141 | Transcript search is not presented as useful before a transcript exists. | S,V | W,P |
| 142 | Long operations expose task-specific processing state. | S,R | W,P |
| 143 | Progress copy describes the operation rather than relying on generic spinners. | S | W,P |
| 144 | Research-facing errors use a shared human/actionable pattern. | S | W,P |
| 145 | Rust/Tauri/database/plugin jargon is not the primary researcher error. | S | W,P |
| 146 | Plain-language recovery direction appears first. | S | W,P |
| 147 | Technical details are behind disclosure. | S | W,P |
| 148 | Retry is only offered for retryable situations. | S | W,P |
| 149 | Destructive actions use explicit guarded confirmations. | S,R | W,P |
| 150 | Source deletion previews impacts on coding/notes/memos/participants and other research links. | S | W,P |
| 151 | Retranscription of coded/annotated material explains consequences. | S,R | W,P |
| 152 | Code/theme deletion/merge paths preview affected relationships/evidence where applicable. | S,R | W,P |
| 153 | Existing data-protection rules are surfaced rather than remaining invisible engine logic. | S,R | W,P |
| 154 | Undo/redo remains covered by carried coding/usability regressions. | R | W,P |
| 155 | Recovery is presented through a friendly recovery surface rather than uncertain reopening. | S,R | W,P |
| 156 | Accessibility is part of the UX Foundation gate. | S,V | P |
| 157 | Focus, tab navigation, contrast and accessible labels have automated/static coverage. | S,V | P |
| 158 | Active/status state uses text/shape/placement as well as colour. | S,V | P |
| 159 | Resizable panes expose keyboard alternatives where practical. | S | W,P |
| 160 | Common laptop sizes have no root horizontal interface breakage. | S,V | P |
| 161 | Browser gates exercise multiple window sizes rather than one maximised workstation. | S,V | P |
| 162 | Inspector horizontal-scroll regression now has explicit coverage. | S,V | P |
| 163 | Constrained layouts adapt without shrinking meaningful text below the floor. | S,V | P |
| 164 | Large-project needs are built into navigation/rendering contracts. | S,L | P |
| 165 | Sources architecture/workload is tested at hundreds-of-sources scale. | L | P |
| 166 | Codes architecture includes hierarchy/filter/search and workload protection for large code systems. | S,L | P |
| 167 | Participants support attributes/cases/group comparisons. | S,R | W,P |
| 168 | Collections/Sets have a first-class place in Data IA. | S | W,P |
| 169 | Long-document/large-project rendering has workload and page-local/lazy safeguards. | R,L | P |
| 170 | Main workspace has no persistent floating dock/control obstruction. | S,V | W,P |
| 171 | Reusable desktop context menus reduce permanent clutter. | S | W,P |
| 172 | Unfamiliar icon controls use explanatory labels/tooltips. | S,V | P |
| 173 | Icons support language instead of replacing core labels. | S,V | P |
| 174 | Source/Document/Transcript/Participant/Case/Collection/Note/Memo terminology is governed consistently. | S,V | P |
| 175 | Internal/developer terminology is kept out of primary researcher UI. | S | W,P |
| 176 | Active project/source identity is persistently clear. | S,V | W,P |
| 177 | Active source tab/state is unmistakable across multiple open sources. | S,V | W,P |
| 178 | Source-level versus project-level Notes/Memos/Codes are distinguished contextually. | S | W,P |
| 179 | Inspector follows passage/code/participant/theme/source selection context. | S | W,P |
| 180 | Selection can be inspected in place without unnecessary navigation. | S | W,P |

## Items 181–206: Overview, progressive disclosure, design system and recovery semantics

| # | Closure | Evidence | Remaining |
|---:|---|---|---|
| 181 | Project Overview communicates useful health/progress without vanity-dashboard clutter. | S,V | P |
| 182 | Overview surfaces actionable sources/participants/codes/themes/activity/protection information. | S,V | W,P |
| 183 | Permanent statistics are limited to decision/action value. | S,V | P |
| 184 | Beginner path stays simple while advanced features remain discoverable. | S,V | P |
| 185 | Advanced features are progressively disclosed rather than shown simultaneously. | S,V | P |
| 186 | Power-user functions live in context menus/panes/palette/shortcuts. | S,V | W,P |
| 187 | Visual system is deliberately calm. | V | P |
| 188 | Decorative competition is reduced so evidence/coding/themes remain the focus. | V | P |
| 189 | Colour is semantic rather than ornamental. | S,V | P |
| 190 | `docs/TRACE_DESIGN_SYSTEM.md` formally defines typography, spacing, radii, shadows, surfaces, borders, icons, states and responsive rules. | S | P |
| 191 | Shared shell/primitives replace isolated page-only patches. | S,V | P |
| 192 | Empty states share title/explanation/primary/secondary-action conventions. | S,V | P |
| 193 | Error states share plain-language + technical-details conventions. | S | W,P |
| 194 | Import/transcription/extraction/analysis progress follows a shared task-specific convention. | S,R | W,P |
| 195 | Modal/dialog behaviour is standardised, including focus/Escape/action placement. | S,R | W,P |
| 196 | Context-menu behaviour is reusable and keyboard accessible. | S | W,P |
| 197 | Sources/participants/codes/analysis lists share consistent interaction/density conventions. | S,V | P |
| 198 | Pane resizing/collapse uses consistent bounded behaviour. | S,V | W,P |
| 199 | Pane widths are remembered when layout memory is enabled. | S | W,P |
| 200 | Reasonable workspace state is remembered without blindly restoring transient selections. | S | W,P |
| 201 | `Remember my layout` and `Resume exactly where I was` have separate real behaviour. | S | W,P |
| 202 | Missing previous projects fail gracefully back to Home/recovery rather than broken placeholders. | S | W,P |
| 203 | Unavailable recent projects expose Locate / Remove / Restore recovery paths. | S | W,P |
| 204 | Project compatibility/migration/repair paths expose clear loading/recovery feedback. | S,R | W,P |
| 205 | Meaningful-risk migration is surfaced rather than silently hidden. | S,R | W,P |
| 206 | Project/backup data remains separate from app/demo/build files and installer maintenance preserves it. | R | W,P |

## Items 207–240: release gates, end-to-end acceptance and central rules

| # | Closure | Evidence | Remaining |
|---:|---|---|---|
| 207 | Automated UI coverage includes true first-launch state. | S,V | W,P |
| 208 | Release pipeline explicitly verifies what a newly installed user sees. | S | W,P |
| 209 | Installed Windows first-launch smoke checks Home/no fixture/no phantom participant. | S | W,P |
| 210 | Zero-source state tests prove source/participant controls remain truthful. | S,V | W,P |
| 211 | Populated imported-project tests verify title/participant/inspector state. | S,R | W,P |
| 212 | Responsive screenshots/layout gates cover realistic sizes. | S,V | P |
| 213 | Inspector-tab no-scroll/collision gate is explicit. | S,V | P |
| 214 | Typography floor is tested under standard scaling. | S,V | P |
| 215 | Automated DPI/scaling coverage includes 100%, 125% and 150% where practical. | S,V | P |
| 216 | Maximised and constrained/non-maximised viewport conditions are exercised. | S,V | P |
| 217 | Laptop and large-workstation viewport classes are both exercised. | S,V | P |
| 218 | Strict perceptual visual regression complements functional assertions. | S,V | P |
| 219 | Visual release evidence includes Home, empty project, Data/populated source, Code, Themes, Analyse and Write. | S,V | P |
| 220 | Release definition now includes truthful first launch, hierarchy, typography and responsiveness, not only installer/functionality. | S,V | W,P |
| 221 | UX Foundation was prioritised ahead of unrelated headline-feature work. | RESOLVED | none |
| 222 | Programme is explicitly named Trace UX Foundation. | S,RESOLVED | none |
| 223 | UX shell was rebuilt on top of the verified research engine, which remains regression-tested. | S,R | W,P |
| 224 | Phase 1 production-state hygiene/Home/first launch implemented and gated. | S,V | W,P |
| 225 | Phase 2 navigation/context/workspace/inspector shell implemented and gated. | S,V | W,P |
| 226 | Phase 3 typography/spacing/components/responsive system implemented and documented. | S,V | P |
| 227 | Phase 4 Data/import/source/participant workflows redesigned. | S,R | W,P |
| 228 | Phase 5 Code/Themes/Analyse/Write rebuilt within the shared shell. | S,R,V | W,P |
| 229 | Phase 6 contextual Trace AI implemented without visual dominance. | S,V | W,P |
| 230 | Phase 7 keyboard/palette/accessibility/interaction polish implemented and gated. | S,V | W,P |
| 231 | Phase 8 first-launch/visual/Windows acceptance pipeline implemented. | S,V | W,P |
| 232 | Acceptance uses real transcript, XLSX, searchable PDF and WAV fixtures in the installed application. | S | W,P |
| 233 | Installed acceptance is scripted for create → import → participants → code → memo → theme → analyse → write/export → close/reopen → backup/restore. | S | W,P |
| 234 | Large-project workload contract complements realistic populated and multi-format journeys. | L,R | W,P |
| 235 | Truthful-state rule is enforced through empty/populated/contradiction tests. | S,V | W,P |
| 236 | Research material receives the dominant workspace and visual priority. | S,V | P |
| 237 | Navigation/source identity/next-action rules maintain location and orientation. | S,V | W,P |
| 238 | State contradictions are explicit regression failures. | S,V,R | W,P |
| 239 | New shell targets serious Windows research-software behaviour rather than web-dashboard chrome. | S,V | W,P |
| 240 | First launch is designed/tested to be understandable within seconds, with final subjective judgement reserved for real-machine UAT. | S,V | W,P |

## Current closure summary

### Automated source side

The strict source candidate is green. Run `33152414998` proves the reconstructed UX source, carried research engine, both frontends, browser researcher journey, state-truth/trust checks, responsive/DPI matrix, reviewed strict visual baseline, native Trace compilation/tests and setup-shell compilation/tests.

### Windows installed side

`PENDING`: run `33154626340` must complete the actual installed Windows acceptance lane. It is responsible for the exact branded installer, installed executable equivalence, real installed WebView2 first launch, multi-format researcher journey, close/reopen persistence, findings export, verified backup/restore, maintenance matrix and rollback verification.

When that run is green, replace `W` in this ledger with accepted Windows evidence and record the installer/artifact hashes.

### Physical UAT

`PENDING`: GitHub issue #5 is the final human-machine acceptance boundary. Subjective requirements such as visual calm, real-display readability, desktop feel, first-use comprehension and actual machine behaviour cannot truthfully be closed by CI alone.

## Final closure rule

Do **not** write `240/240 COMPLETE` until:

1. Windows acceptance is green from the exact source artifact above (or a later fully green superseding source),
2. this ledger is updated with that Windows run/artifact/hash,
3. issue #5 physical UAT is complete,
4. any defect found in physical UAT is fixed and the affected gates are rerun,
5. `PROGRESS.md` records the same final evidence.
