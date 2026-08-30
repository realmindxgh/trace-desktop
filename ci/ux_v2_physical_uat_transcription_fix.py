from pathlib import Path

transcription_path = Path('src-tauri/src/transcription.rs')
transcription_test_path = Path('tests/v11_transcription.py')

transcription = transcription_path.read_text(encoding='utf-8')
transcription_test = transcription_test_path.read_text(encoding='utf-8')

old = '''    } else {
        params.set_language(None);
        params.set_detect_language(true);
    }'''
new = '''    } else {
        // A null/auto language tells whisper.cpp to auto-detect the language and then
        // continue decoding. detect_language=true is a detect-only mode that returns
        // immediately after language identification and therefore yields no transcript.
        params.set_language(None);
        params.set_detect_language(false);
    }'''

if old in transcription:
    transcription = transcription.replace(old, new, 1)
elif 'detect-only mode that returns' not in transcription:
    raise SystemExit('Whisper auto-language parameter anchor changed')

# Keep a static tripwire alongside the real spoken-audio inference test. The latter is
# authoritative, but this makes the exact regression obvious before a long native build.
tripwire = '''
# Auto language must auto-detect and continue transcription. whisper.cpp's
# detect_language=true mode intentionally exits immediately after language detection.
transcription_rs=(ROOT/'src-tauri/src/transcription.rs').read_text(encoding='utf-8')
assert 'params.set_language(None);' in transcription_rs
assert 'detect-only mode that returns' in transcription_rs
'''
if 'detect-only mode that returns' not in transcription_test:
    transcription_test = transcription_test.rstrip() + '\n' + tripwire.strip() + '\n'

transcription_path.write_text(transcription, encoding='utf-8')
transcription_test_path.write_text(transcription_test, encoding='utf-8')
print('Applied Whisper auto-language continuation fix.')
