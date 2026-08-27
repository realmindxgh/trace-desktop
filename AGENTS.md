# Trace Desktop Agent Execution Guide

This file is the primary product and execution contract for any coding agent, contributor, or automated development system working on Trace Desktop.

Read this file before changing application code, installer code, CI, release controls, product architecture, or UX.

## Contract precedence

The **Trace UX Foundation Master Contract** below is the current product goal and has priority over older implementation guidance when there is a conflict.

In particular, older instructions that describe the work as only a hardening pass, say the app shell should not be substantially redesigned, or require the existing bottom workspace dock to be preserved are historical v0.12.1 guidance and do **not** override this master contract.

The research engine and proven research capabilities must be preserved. The application shell, information architecture, first-launch experience, navigation model, state presentation, and interaction language may be rebuilt as necessary to satisfy this contract.

The conceptual research journey remains important:

`Bring data in -> Organise -> Code evidence -> Develop themes -> Analyse patterns -> Write findings`

The current v0.12.1 engineering line is a verified baseline, not the end of the UX programme. See `PROGRESS.md` and `docs/v0121-checklist-status.md` for the exact engineering and installer evidence.

---

# TRACE UX FOUNDATION MASTER CONTRACT

The following 240 items define the overall UX/UI target for Trace. Do not call the UX overhaul complete merely because individual pages look better or automated tests are green. The installed application must satisfy the whole researcher journey and the central product rules at the end of this list.

1. **The first-launch experience is fundamentally wrong.** A newly installed application should not immediately drop the researcher into an unexplained coding workspace. Trace needs a deliberate first-launch experience.
2. **Investigate why “Downloading Videos” appears immediately after installation.** If this is genuinely one of the user's previously saved projects, that is one thing. If it originated from development data, CI, a fixture, seed content or a reconstruction artefact, that is a production bug and all test data must be removed.
3. **Investigate why `P01` appears when the project reports zero participants.** The screenshot says `Participants 0` while simultaneously displaying `P01`. Application state and displayed content must never contradict each other.
4. **A fresh Trace installation should open to Trace Home.** It should not open directly to Data, Code or an arbitrary previously selected workspace unless the user explicitly chooses an auto-resume preference.
5. **Create a proper Welcome screen for genuinely new users.** It should briefly explain what Trace is for and present obvious starting actions such as `New Project`, `Open Project` and `Import Project`.
6. **Do not automatically inject a sample project.** If a sample research project exists, make `Try a sample project` an explicit optional action.
7. **Provide `Recover from backup` on Home.** Recovery should be visible from the beginning because research projects can represent months of work.
8. **Provide an optional Getting Started experience.** It should be lightweight rather than a compulsory multi-step tour.
9. **A useful Getting Started checklist could cover project creation, first import, first code, first memo and first theme.** Once completed, it should disappear permanently.
10. **Trace Home should remain useful after onboarding.** It should become the regular project launcher rather than a one-time welcome page.
11. **Home should show recent projects.** Each project can show name, last opened date, source count and perhaps last modified status.
12. **Home should offer New Project, Open Project, Import Project and Recover Project prominently.**
13. **Add a preference such as `Resume my last project on startup`.** Power users can then bypass Home without forcing that behaviour on everyone.
14. **Project creation should be short.** Do not force users through extensive methodological configuration before letting them work.
15. **The essential New Project dialog should probably require only a project name and perhaps an optional description.**
16. **Research methodology, institution, researcher name, study details and similar metadata should live in Project Settings and be editable later.**
17. **An empty project should open to Project Overview, not Code.** The researcher should first see what exists in the project and what they can meaningfully do next.
18. **Project Overview should have a purposeful empty state.** For example: `Your project is ready. Add research data to begin.`
19. **The empty-project screen should offer clear actions such as Import documents, Import survey data, Transcribe audio/video and Import an existing qualitative project.**
20. **Supported file types can appear beneath those import actions.** This helps users understand Trace's capabilities without making the interface busy.
21. **Never render participant UI when there is no participant.** No fake avatar, `P`, `P01`, participant metadata or View Profile link should appear in an empty project.
22. **Never render transcript controls when there is no transcript.** The transcript search bar should disappear or clearly disable itself until a text source is open.
23. **Never show source-specific inspector content before a source exists.**
24. **The current empty-state message `No matching sources` is incorrect when no search/filter has been performed.** It should say `No sources yet`.
25. **Empty states throughout Trace should explain the next useful action.** Empty space should teach the product rather than simply announce absence.
26. **No codes should produce guidance such as `Create your first code or code a passage to get started.`**
27. **No themes should explain how themes emerge from organised codes.**
28. **No analyses should present available analysis/query options.**
29. **No writing documents should offer Create findings document, New report or Start from coded evidence.**
30. **The application should always tell the truth about state.** Counts, selections, participant information, current source, inspector content and navigation state must all agree.
31. **The current workspace contains far too much unused white space.** Most of the screen currently communicates nothing.
32. **The main research material should dominate the application.** Once a transcript, document or PDF is open, that source should visually become the centre of Trace.
33. **Trace currently gives too much visual importance to navigation chrome and too little to research content.**
34. **The overall layout should move toward `Navigation rail | Context pane | Main workspace | Inspector`.**
35. **Replace the giant floating bottom dock.** It is visually dominant, occupies content space and feels detached from the rest of the interface.
36. **Data, Code, Themes, Analyse and Write are worth keeping as Trace's conceptual backbone.** The problem is their current presentation, not the model itself.
37. **Move those major modes into a slim permanent left navigation rail.**
38. **The navigation rail should clearly indicate the active mode.** There should never be ambiguity between something such as `Data / Sources / P01` and a separately highlighted `Code` button.
39. **Do not maintain multiple competing navigation systems.** The current left sidebar, central breadcrumb and bottom dock all communicate location differently.
40. **The second left pane should be contextual.** Its contents should change according to the selected major mode.
41. **In Data, the context pane could contain Sources, Participants, Collections/Sets, Attributes and Imports.**
42. **In Code, the context pane should become the code system/code tree.**
43. **In Themes, it should show theme structures and relationships.**
44. **In Analyse, it should show queries, analysis tools, saved analyses and results.**
45. **In Write, it should show writing documents, findings sections, exports or generated evidence tables.**
46. **The left Data panel currently feels unfinished.** Search, Sources, Import Source and Project Counts are not enough to form a mature information architecture.
47. **`Sources 0 ▼` currently looks like a small website accordion rather than a serious research-data tree.**
48. **The source tree should eventually support folders, collections, filtering, participant attributes, sorting and large-project navigation.**
49. **The Project Counts card should not permanently occupy valuable sidebar space.** Four zeroes in a box are not actionable information.
50. **Project statistics belong more naturally on Project Overview/Home or an optional dashboard.**
51. **`Import source` is currently too visually weak despite being the most important action in an empty project.**
52. **Import should become a proper workflow rather than one generic button.**
53. **The Import experience should distinguish Documents, PDFs, Spreadsheets/Surveys, Audio/Video and REFI-QDA/project imports where appropriate.**
54. **Drag and drop should be supported in the Data workspace.**
55. **After import, Trace should clearly summarise what happened.** For example: `4 sources imported`, `3 participants detected`, `1 file needs attention`.
56. **Import completion should offer meaningful next actions such as Open first source, Review participants or Begin coding.**
57. **Audio/video transcription should become a first-class import workflow.**
58. **Importing audio/video should offer `Transcribe now` and `Add without transcription`.**
59. **Transcription UX should expose useful controls such as language, model, progress and perhaps speaker workflow when those capabilities exist.**
60. **Local transcription should clearly state that processing happens locally.** That is a meaningful product advantage.
61. **The participant header is currently awkward and unfinished.** `P`, another `P`, `Participant`, missing years of experience and another dash creates visual noise.
62. **Do not render missing participant metadata as chains of em dashes.** Missing fields should usually disappear.
63. **Participant profiles should only appear when actual data links a source to a participant.**
64. **Participant information should be compact and secondary to the source being analysed.**
65. **The source/document title should be visually prominent whenever a source is open.**
66. **Trace should support a proper document-tab model.** Researchers will naturally work across several transcripts, PDFs and memos.
67. **Tabs would give the application a more natural professional desktop workflow.**
68. **Breadcrumbs should move out of the global application header and closer to the workspace they describe.**
69. **The current breadcrumb floating in the middle of the top bar feels disconnected from the content.**
70. **The right inspector is currently too narrow.**
71. **The inspector should be resizable.** A default somewhere around 320–440 px would be more realistic, depending on available screen width.
72. **The inspector should also be collapsible.** Researchers should be able to devote nearly the full window to documents when needed.
73. **The inspector tabs should never require a horizontal scrollbar.** The screenshot's INFO / CODES / NOTES / MEM… strip is unacceptable for a desktop application.
74. **Rename inspector tabs more naturally to Details, Codes, Notes and Memos.**
75. **Counts should appear as small badges rather than becoming part of long tab labels.**
76. **On narrower windows, low-priority inspector items can move into a More menu rather than creating horizontal scrolling.**
77. **Inspector content must reflect the actual currently selected source, participant, code or theme.**
78. **The global top bar currently mixes too many unrelated responsibilities.**
79. **Simplify the top bar to project identity/switcher on the left, optional global search or command palette centrally, and save/settings/account controls on the right.**
80. **The current project title block uses too much horizontal space.**
81. **`Downloading Videos / Qualitative Content Analysis` should become a more compact project switcher/header presentation.**
82. **If `Qualitative Content Analysis` is interactive, the current tiny dropdown indicator is too subtle.**
83. **Undo and redo should become contextual rather than permanently prominent when unavailable.**
84. **The save-state indicator is useful but should be cleaner.** `✓ Saved` is stronger than a tiny `Saved 9s ago`.
85. **Clicking or hovering over save state could reveal precise save time, project location and backup information.**
86. **Data confidence should become a deliberate UX feature because Trace handles valuable research projects.**
87. **Show autosave and backup status somewhere reassuring but unobtrusive.**
88. **Project Home or a Protection area could show Autosave on, last backup time and Restore backup.**
89. **Separate Project Settings from Trace/Application Settings.**
90. **Project Settings should hold project metadata, research details, participant configuration, project backup settings and project-specific export options.**
91. **Application Settings should hold theme, interface size, shortcuts, default transcription settings, update behaviour and similar global preferences.**
92. **The typography across the screenshot is too small.**
93. **This needs a complete typography system, not isolated CSS overrides.**
94. **Normal interface body text should generally live around a readable 15–16 px equivalent at standard scaling.**
95. **Secondary labels should still remain clearly readable, perhaps around 13–14 px rather than tiny dashboard microcopy.**
96. **Transcript/document reading text should be larger again, probably around 16–18 px depending on font and line height.**
97. **Add an interface density/size preference such as Compact, Comfortable and Large.**
98. **Do not make users rely solely on Windows display scaling to fix Trace's own typography.**
99. **Strengthen visual hierarchy.** At present headings, metadata, controls, labels and document content do not establish a convincing order of importance.
100. **The current interface has too many outlines.** App shell, panels, cards, search controls and other elements are all separated using pale borders.
101. **Use spacing, surface changes and typography more often than borders.**
102. **Reserve bordered cards for genuinely self-contained information.**
103. **There are too many rounded rectangles.** Rounded corners have become a default decoration instead of a structural tool.
104. **Reduce excessive corner radii and apply them only where they help hierarchy.**
105. **Remove the large rounded container surrounding almost the entire application.** Trace is already inside a native Windows window.
106. **Do not simulate another browser/dashboard window inside the Windows application.**
107. **The current visual language feels too much like a web dashboard embedded inside a desktop shell.**
108. **Move Trace toward a genuine desktop research-tool aesthetic rather than SaaS-dashboard styling.**
109. **The Windows title bar already says Trace while the app content immediately repeats the Trace brand.** Reduce unnecessary double-branding.
110. **The giant navy navigation capsule and the delicate white workspace currently look as though they belong to different design systems.**
111. **Create one coherent design system across navigation, panels, controls, tabs, menus and content surfaces.**
112. **The strange coloured blue/green lines visible across the bottom of the workspace need investigation.** If they are decorative, remove them. If they are rendering artefacts, fix the rendering bug.
113. **Nothing decorative should cross underneath or through the workspace in a professional research application.**
114. **AI currently receives disproportionate visual emphasis.**
115. **The sparkle button is more visually prominent than the core research workflow despite having no label.**
116. **Give AI a clear name such as `Trace AI` or `Assistant`.**
117. **Place AI naturally within the left navigation architecture instead of presenting it as a glowing mystery control.**
118. **AI should augment the current task rather than behave like a disconnected destination.**
119. **Inside a transcript, AI could offer contextual functions such as summarise source, suggest codes or ask questions about the current source.**
120. **Inside Themes, AI could help compare codes/themes or identify patterns.**
121. **Inside Write, AI could help organise evidence, draft structures or generate evidence tables.**
122. **AI must not dominate the qualitative-analysis workflow.** The researcher's evidence and decisions should remain visually central.
123. **Each major Trace mode needs a purposeful default screen instead of reusing a generic empty workspace.**
124. **Data should default to project/data organisation when nothing is selected.**
125. **Code should default to the code system or coding overview when there is no open document.**
126. **Themes should default to theme organisation rather than an empty document shell.**
127. **Analyse should default to analysis/query choices and saved results.**
128. **Write should default to writing documents, findings sections or create-document actions.**
129. **Trace should make the research journey legible throughout the product.**
130. **The conceptual sequence should be something like `Bring data in → Organise → Code evidence → Develop themes → Analyse patterns → Write findings`.**
131. **That research journey should act as the invisible backbone of the information architecture rather than merely appearing as five buttons.**
132. **Introduce subtle transition guidance.** After first coding activity, Trace can gently indicate what was accomplished and what may logically come next.
133. **Do not turn progression into gamification.** The purpose is orientation, not badges and confetti.
134. **Add a global command palette.** `Ctrl+K` or `Ctrl+Shift+P` could expose frequently used actions without filling toolbars with buttons.
135. **Useful command-palette actions could include Import source, Create code, Search project, New memo, Open recent project, Export and Jump to participant.**
136. **Keyboard interaction should become a serious part of Trace UX.**
137. **Common repetitive research actions should have sensible shortcuts.**
138. **Examples include Create code, Apply code, Add memo, Search, Undo, Next source, Previous source and Open command palette.**
139. **Menus and tooltips should expose those shortcuts so users can learn them naturally.**
140. **Search should be contextual.** Project-wide search, source search and code search are different activities and should be clearly distinguished.
141. **The transcript search field should not masquerade as a useful control before a transcript exists.**
142. **Processing states need stronger feedback.** Importing documents, extracting PDFs, transcribing media, running analysis and exporting reports should never feel silent or frozen.
143. **Progress messages should say what Trace is actually doing rather than use generic loading indicators.**
144. **Errors need to be human and actionable.** The installer already demonstrated how damaging raw framework errors can be.
145. **Do not expose Rust, Tauri, database or plugin terminology as the primary error message.**
146. **Provide useful plain-language recovery instructions first.**
147. **Technical information can live behind a `Technical details` disclosure for troubleshooting.**
148. **Retry should only be shown when retrying can realistically fix the problem.**
149. **Destructive actions need strong UX protection.**
150. **Deleting a coded source must explain what happens to attached coding, notes, memos and participant relationships.**
151. **Retranscribing already coded or annotated material should explicitly warn about the consequences.**
152. **Merging or deleting codes/themes should preview how relationships and coded segments will change.**
153. **The existing internal data-protection logic should be surfaced clearly in the interface.**
154. **Undo/redo should be reliable enough that users trust experimentation.**
155. **Crash recovery should have a friendly recovery screen rather than simply reopening into an uncertain state.**
156. **Accessibility needs to become part of the UX foundation.**
157. **Ensure proper keyboard focus states, tab navigation, contrast and screen-reader-compatible labels.**
158. **Do not rely solely on colour to indicate active state or status.**
159. **Resizable panes should have accessible keyboard alternatives where practical.**
160. **Trace should work sensibly on common laptop resolutions without horizontal interface breakage.**
161. **Test the real application at multiple window sizes, not only maximised on a large CI desktop.**
162. **The right-panel horizontal scrollbar already proves responsive testing is currently insufficient.**
163. **The UI should gracefully adapt rather than simply shrink fonts when space becomes constrained.**
164. **Large projects need to influence the architecture now rather than later.**
165. **Design Sources for hundreds of interviews/documents, not just four demo files.**
166. **Design Codes for hundreds or thousands of codes with hierarchy, filtering and search.**
167. **Design Participants for real attributes, cases and group comparisons.**
168. **Collections/Sets need a place in the information architecture if Trace intends to support cross-case qualitative analysis.**
169. **Long transcripts and large PDFs need performant scrolling and selection behaviour.**
170. **The main workspace should not be obstructed by persistent floating controls.**
171. **Context menus should be used where they reduce permanent clutter.**
172. **Tooltips should explain unfamiliar icons rather than forcing users to guess.**
173. **Icons should support labels rather than replacing language unnecessarily.**
174. **Use consistent terminology throughout Trace.** For example, decide carefully when something is called Source, Document, Transcript, Participant, Case, Collection, Note or Memo.
175. **Avoid internal/developer language in the researcher's interface.**
176. **The application needs stronger source identity.** A researcher should always know exactly which document, participant and project they are working in.
177. **When multiple sources are open, active-source state must be unmistakable.**
178. **Notes, Memos and Codes should clearly distinguish source-level content from project-level content.**
179. **The right inspector should follow selection context intelligently.** Selecting a passage, code, participant, theme or source should produce relevant details.
180. **Do not make researchers manually navigate somewhere else merely to inspect the thing they just selected.**
181. **Project Overview should communicate project health and progress without becoming a vanity analytics dashboard.**
182. **Useful overview information might include sources, participants, codes, themes, last activity and backup status.**
183. **Avoid displaying statistics just because numbers are available.** Every permanent UI element should help the researcher make a decision or take an action.
184. **The interface should progressively reveal complexity.** Beginners should be able to import and code quickly while advanced functionality remains discoverable.
185. **Do not expose every advanced feature simultaneously.** That creates cognitive overload.
186. **Power-user functions can appear through contextual menus, panels, command palette and keyboard shortcuts.**
187. **Trace should feel calm.** Qualitative analysis is cognitively demanding enough without the software demanding attention from every corner.
188. **Reduce decorative visual competition so evidence, annotations, coding and themes remain the focus.**
189. **Use colour deliberately.** Colour should indicate meaning, active state, coding or status rather than decorate structural lines and controls.
190. **Develop a formal Trace design system.** Define typography, spacing, radii, shadows, surface hierarchy, border use, icon sizing, interaction states and responsive rules.
191. **Build reusable UI primitives rather than fixing individual pages independently.** Buttons, tabs, inspectors, context panes, empty states, dialogs and menus should all derive from common components.
192. **Create standard empty-state components with title, explanation, primary action and optional secondary action.**
193. **Create standard error-state components with plain-language explanation and optional technical details.**
194. **Create standard loading/progress components for imports, transcription, extraction and analysis.**
195. **Create a proper desktop modal/dialog standard.** Dialogs should have consistent sizing, action placement and keyboard behaviour.
196. **Create a consistent context-menu standard.**
197. **Create a consistent table/list standard for sources, participants, codes and analyses.**
198. **Create a consistent pane-resizing and pane-collapsing behaviour.**
199. **Remember pane widths where appropriate between sessions.**
200. **Remember reasonable workspace state without blindly restoring confusing transient selections.**
201. **Differentiate `remember my layout` from `resume exactly where I was`.** Those are separate preferences.
202. **The application should gracefully handle a deleted/missing previous project instead of opening into broken placeholders.**
203. **Recent-project entries should detect unavailable project locations and offer Locate, Remove from list or Restore.**
204. **Opening a project should include clear loading/recovery feedback if the project requires migration or repair.**
205. **Version migrations should never happen invisibly if there is meaningful risk.**
206. **Project data should remain separate from application/demo/build files.** Installer updates must not contaminate user research data.
207. **Automated UI tests need to cover first launch, not just successful installation.**
208. **The release pipeline should verify what a real user sees after launching a newly installed copy.**
209. **Add a Windows first-launch smoke test.** It should verify that production builds do not expose demo/test projects or phantom participants.
210. **Add UI-state tests for zero-source projects.** They should prove that source-specific and participant-specific controls remain hidden.
211. **Add tests for real imported projects.** Confirm the correct source title, participant and inspector state appear.
212. **Add responsive screenshot or layout checks at realistic window sizes.**
213. **Specifically test the inspector tab area so horizontal-scroll regressions cannot silently return.**
214. **Specifically test typography at standard Windows scaling.**
215. **Test with 100%, 125% and 150% Windows scaling where practical.**
216. **Test maximised and non-maximised windows.**
217. **Test common laptop resolutions as well as large workstation screens.**
218. **Visual regression testing should complement functional tests.** An application can technically work while looking obviously broken, which this screenshot demonstrates perfectly.
219. **Release gates should capture at least Home, empty project, populated transcript, Codes, Themes, Analyse and Write screens.**
220. **The application's release definition therefore needs to expand beyond “installer works and functionality exists.”** It should include truthful first-launch state, usable visual hierarchy, readable typography and responsive core screens.
221. **Do not prioritise OCR, sophisticated network visualisations or other headline v0.12 features before this UX foundation is repaired.**
222. **The next development phase should be treated as `Trace UX Foundation` or equivalent.**
223. **That phase should preserve the working research engine underneath while rebuilding the application shell around it.**
224. **Phase one should address production-state hygiene, Home and first launch.**
225. **Phase two should establish navigation architecture and the context-pane/workspace/inspector shell.**
226. **Phase three should establish typography, spacing, component design and responsive behaviour.**
227. **Phase four should redesign Data/import/source/participant workflows.**
228. **Phase five should redesign Code, Themes, Analyse and Write within the shared shell.**
229. **Phase six should integrate Trace AI contextually rather than as an isolated visual attraction.**
230. **Phase seven should add keyboard productivity, command palette, accessibility and advanced interaction polish.**
231. **Phase eight should introduce visual and first-launch regression gates into the Windows release pipeline.**
232. **Do not consider the UX overhaul complete merely because screenshots look attractive.** Real workflows must be exercised with actual imported transcripts, PDFs, spreadsheets and media.
233. **Test the entire researcher journey:** create project -> import data -> organise participants -> code passages -> create notes/memos -> build themes -> analyse -> write/export -> close -> reopen -> recover/backup.
234. **Use realistic project sizes during testing rather than only empty/demo projects.**
235. **The central design rule should be: show only what is meaningful in the current state.**
236. **The central product rule should be: the research material is more important than Trace's interface.**
237. **The central navigation rule should be: the researcher should always know where they are, what they are working on and what they can do next.**
238. **The central trust rule should be: Trace should never visually contradict its own data state.**
239. **The central desktop rule should be: Trace should feel like serious Windows research software, not a web dashboard placed inside a native window.**
240. **The central first-launch rule should be: a researcher opening Trace for the first time should understand the product within seconds without already knowing how Trace works.**

---

# Required implementation sequence

Use the phase order defined by items 224–231 unless a blocking dependency requires otherwise.

## Phase 1: Production-state hygiene, Home and first launch

Focus on items 1–30, 181–183, 200–209 and related state-truth requirements.

Acceptance must prove a genuinely fresh installed copy opens to a clean Trace Home with no demo project, phantom participant, leaked fixture state, or unexplained workspace selection.

## Phase 2: Navigation architecture and desktop shell

Focus on items 31–91 and related source-identity/context rules.

The target shell is:

`Navigation rail | Context pane | Main workspace | Inspector`

The major modes remain Data, Code, Themes, Analyse and Write, but the giant floating bottom dock must be replaced by the slim permanent left navigation rail required above.

## Phase 3: Design system, typography and responsive behaviour

Focus on items 92–113, 156–163 and 187–199.

Create shared tokens and reusable primitives rather than page-specific cosmetic patches.

## Phase 4: Data, import, source and participant workflows

Focus on items 46–65, 140–153, 164–180 and the large-project requirements.

## Phase 5: Code, Themes, Analyse and Write

Rebuild these modes within the shared shell while preserving the verified research engine and existing analytical mathematics.

## Phase 6: Contextual Trace AI

Focus on items 114–122. AI must support the current research task and must never visually dominate the evidence or researcher decisions.

## Phase 7: Productivity, accessibility and interaction polish

Focus on items 134–180 and the relevant design-system requirements, including command palette, keyboard shortcuts, contextual search, accessible resizing, human errors and destructive-action safeguards.

## Phase 8: Visual, first-launch and end-to-end release gates

Focus on items 207–240.

The Windows release pipeline must verify not only that Trace installs and launches, but also that first launch is truthful and understandable and that the core researcher journey remains usable at realistic resolutions and scaling levels.

---

# Non-regression rules

The UX Foundation may rebuild the application shell, but it must not remove or weaken the proven research engine.

Preserve and retest at minimum:

- Office and survey imports
- DOCX, CSV, XLSX, PDF, image, audio and video workflows
- coding and annotations
- undo and redo
- offline/local transcription
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
- notes and memos
- themes
- project recovery
- verified backups
- research-data preservation through install, update, repair, rollback and uninstall

Never weaken an existing research or data-preservation test merely to make a UX build pass.

Research data is more important than application files.

Core research workflows remain local-first unless the user explicitly chooses a network feature.

Do not expose transcript text, participant data, codes, notes, memos or other research content in diagnostic logs.

---

# Definition of UX Foundation done

Do not mark the Trace UX Foundation complete until all of these are true:

- all 240 master-contract items have been implemented, explicitly resolved, or documented as intentionally not applicable with a defensible product reason
- the new shell and navigation architecture are present in the installed Windows app
- a genuinely fresh installed copy opens to Trace Home and contains no fixture/demo leakage
- zero-state, populated-state and contradictory-state tests are green
- realistic imports and research workflows work end to end
- the full researcher journey in item 233 has been exercised
- responsive and DPI checks cover common laptop and workstation sizes
- visual regression gates cover Home, empty project, populated source, Code, Themes, Analyse and Write
- research-feature regression contracts remain green
- installer/update/repair/rollback/data-preservation gates remain green
- real-machine physical UAT is complete
- any defects found during physical UAT are fixed and the relevant gates rerun

Passing the older v0.12.1 hardening checklist alone is not sufficient to declare this master UX contract complete.

---

# Historical v0.12.1 engineering baseline

The v0.12.1 hardening work remains valuable evidence and must not be discarded. It established a proven Windows engineering baseline including installer diagnostics, safe update/repair behaviour, rollback, version consistency, typography improvements, inspector hardening, import improvements, search behaviour, accessibility foundations, responsive/DPI contracts, research regression tests and exact Windows release verification.

Read these files for that history and exact run/artifact evidence:

- `PROGRESS.md`
- `docs/v0121-checklist-status.md`
- `docs/visuals/README.md`
- `build-status/windows-v0121-exact-final-v2.txt`

Where those historical documents conflict with this master UX contract on product direction, **this file wins**.

---

# Agent workflow and handoff

Before making material changes:

1. Read this entire file.
2. Read `PROGRESS.md`.
3. Inspect the current branch and exact source lineage.
4. Run the relevant existing regression tests before changing behaviour.
5. Work phase by phase and keep commits focused.
6. Add regression coverage for each bug class where practical.
7. Verify the installed Windows application, not only source code or browser fixtures.
8. Update `PROGRESS.md` before handoff.

Every handoff must record:

- branch and commit SHA
- master-contract items or phase being worked on
- tests run
- tests passing
- tests failing
- exact failure logs or error codes
- workflow run IDs
- artifact names
- known unresolved issues
- physical-UAT findings where relevant
- intentional deviations from this contract and the product reason

Do not claim success from source checks alone. Do not claim UX completion from attractive screenshots alone. The installed application and the real researcher journey are the deliverables.
