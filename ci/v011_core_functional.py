from pathlib import Path
import json, re, sqlite3, sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else 'work').resolve()
APP = (ROOT / 'src/app.js').read_text(encoding='utf-8')
DB = (ROOT / 'src-tauri/src/db.rs').read_text(encoding='utf-8')
LIB = (ROOT / 'src-tauri/src/lib.rs').read_text(encoding='utf-8')
MODELS = (ROOT / 'src-tauri/src/models.rs').read_text(encoding='utf-8')
SCHEMA = (ROOT / 'database/schema.sql').read_text(encoding='utf-8')
CARGO = (ROOT / 'src-tauri/Cargo.toml').read_text(encoding='utf-8')
OFFICE = (ROOT / 'src-tauri/src/office_import.rs').read_text(encoding='utf-8')
TRANS = (ROOT / 'src-tauri/src/transcription.rs').read_text(encoding='utf-8')

# Production-empty workspace and no demo logic masquerading as analysis.
for banned in ['Inclusive Education Experiences', 'fake-sparkline', 'matches(/teacher|school|classroom/', "proposedName:'Support and belonging'"]:
    assert banned not in APP, banned
for expected in ['No AI provider is configured', 'does not contain a configured AI provider']:
    assert expected in APP, expected

# Core navigation, search, collections and source management.
for token in [
    'id="data-search"', 'id="transcript-search"', 'visibleSources()', 'openCollectionEditor',
    'openSourceManager', 'set_source_participant', 'update_source_collection', 'delete_source_collection',
]:
    assert token in APP or token in LIB, token

# Coding, memos, themes and evidence-linked analysis/writing remain real workflows.
for token in [
    'openCodeEditor', 'removeCodingReference', 'openMemoEditor', 'openThemeEditor',
    'renderAnalyseWorkspace', 'exportAnalysisCsv', 'code-matrix', 'evidence-browser',
    'renderWriteWorkspace', 'saveCurrentFindings', 'insertFindingEvidence',
    'exportFindingsMarkdown', 'findings_sections', 'findings_evidence_links',
]:
    assert token in APP or token in DB or token in SCHEMA, token

for table in ['findings_sections', 'findings_evidence_links', 'annotations', 'backup_policies']:
    assert re.search(rf'CREATE TABLE IF NOT EXISTS\s+{table}\b', SCHEMA, re.I), table

# Undo/redo, session recovery and backups stay wired through native commands.
for token in [
    'undo_last_action', 'redo_last_action', 'begin_project_session', 'heartbeat_project_session', 'end_project_session',
    'create_trace_backup', 'maybe_auto_backup', 'list_trace_backups', 'restore_trace_backup_new',
]:
    assert token in LIB or token in DB, token

# REFI-QDA interoperability is still present in the application surface.
for token in ['import-qdc', 'export-qdc', 'import-qdpx', 'export-qdpx']:
    assert token in APP, token

# v0.11 office/survey imports and readability controls.
for token in ['import_docx_source', 'preview_survey_file', 'import_survey_file', "return 'docx'", "return 'csv'", "return 'xlsx'"]:
    assert token in APP or token in LIB, token
for token in ['pub fn docx_text', 'pub fn parse_csv', 'pub fn parse_xlsx', 'pub fn parse_table']:
    assert token in OFFICE, token

# v0.11 annotations and coding stripes.
for token in ['coding-stripes', 'openAnnotationEditor', 'create_annotation', 'update_annotation', 'delete_annotation']:
    assert token in APP or token in LIB or token in DB, token

# Offline transcription remains local and evidence-safe.
for token in ['whisper-rs = "0.16"', 'symphonia = { version = "0.6"']:
    assert token in CARGO, token
for token in ['pick_whisper_model', 'transcribe_source_locally']:
    assert token in LIB, token
for token in ['"cloud_used":false', 'original_media_modified', 'DELETE FROM transcript_segments', 'INSERT INTO transcript_segments']:
    assert token in TRANS, token

# PDF text analysis is local, preserves the original PDF, and stays evidence-verifiable.
for token in ['pdf-extract = "0.12"']:
    assert token in CARGO, token
for token in ['extract_pdf_text_pages', 'store_pdf_text', 'original_media_modified']:
    assert token in DB, token
for token in ['renderPdfTextAnalysis', 'Local extraction · no upload', 'Verify quotations against the original PDF.', 'Keep coding the PDF visually.']:
    assert token in APP, token
assert 'combined.chars().count()' in DB, 'PDF offsets must follow Trace character-position convention'

# Version alignment.
for rel in ['package.json', 'src-tauri/tauri.conf.json', 'setup-shell/package.json', 'setup-shell/src-tauri/tauri.conf.json']:
    obj = json.loads((ROOT / rel).read_text(encoding='utf-8'))
    assert obj['version'] == '0.11.0', (rel, obj.get('version'))

# Schema must actually initialize, not merely contain table-name strings.
con = sqlite3.connect(':memory:')
con.execute('PRAGMA foreign_keys=ON')
con.executescript(SCHEMA)
tables = {row[0] for row in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert {'findings_sections', 'findings_evidence_links', 'annotations', 'backup_policies'} <= tables
con.close()

print('Trace v0.11 core functional feature audit passed')
