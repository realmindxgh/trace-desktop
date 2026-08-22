from __future__ import annotations

import argparse
import base64
import hashlib
import lzma
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "work"

BASE_PARTS = 8
BASE_B64_LEN = 101_964
BASE_SHA256 = "6a444acb5b8a25a673c39ccc02374998628c36d6ad4af7e82b32564ab965c074"

LAYERS = [
    ("v010", 4, 43_260, "fb595dd3bbf9d23b10d4aaacd8a907119eb495448418d88bb33eb52c045633da"),
    ("v011", 2, 15_296, "6cd4bdd47a095341ba6151d6addb73f47a005ad57110d3ade443449f9e9f40f2"),
    ("v011plus", 2, 13_960, "60dccf75689c9f46a8e76ecee0356ecaf2e69713c6e624bbacaaa6e7b358ef5a"),
    ("v011transcribe", 2, 17_960, "8ae71006df954e47040b79fda535b6212bc2949ce4efa7613ab90bbd0204515a"),
]

V010_LEGACY_TESTS = (
    "tests/v07_installer.py",
    "tests/v08_release.py",
    "tests/v09_release.py",
)


def read_parts(folder: Path, count: int, expected_len: int) -> bytes:
    parts = sorted(folder.glob("part*"))
    if len(parts) != count:
        raise SystemExit(f"{folder.name}: expected {count} parts, found {len(parts)}")
    text = "".join(p.read_text(encoding="utf-8") for p in parts).strip()
    if len(text) != expected_len:
        raise SystemExit(f"{folder.name}: base64 length {len(text)} != {expected_len}")
    return base64.b64decode(text)


def require_sha(data: bytes, expected: str, label: str) -> None:
    actual = hashlib.sha256(data).hexdigest()
    if actual != expected:
        raise SystemExit(f"{label}: SHA-256 mismatch {actual}")


def strip_diff_sections(patch_bytes: bytes, excluded: tuple[str, ...]) -> bytes:
    """Drop complete git-diff sections for paths restored from authoritative files later."""
    text = patch_bytes.decode("utf-8")
    pieces = text.split("diff --git ")
    if len(pieces) == 1:
        return patch_bytes
    kept = [pieces[0]]
    removed: set[str] = set()
    for chunk in pieces[1:]:
        header = chunk.splitlines()[0] if chunk else ""
        match = next((path for path in excluded if f"a/{path} b/{path}" in header), None)
        if match:
            removed.add(match)
            continue
        kept.append("diff --git " + chunk)
    missing = set(excluded) - removed
    if missing:
        raise SystemExit(f"v0.10 patch did not contain expected legacy test sections: {sorted(missing)}")
    return "".join(kept).encode("utf-8")


def git_apply(patch: Path) -> None:
    subprocess.run(["git", "apply", "--check", "--directory=work", str(patch)], cwd=ROOT, check=True)
    subprocess.run(["git", "apply", "--directory=work", str(patch)], cwd=ROOT, check=True)


def reconstruct(include_transcription: bool) -> None:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)

    base = read_parts(ROOT / "bootstrap" / "v2", BASE_PARTS, BASE_B64_LEN)
    require_sha(base, BASE_SHA256, "Trace base")
    with tempfile.NamedTemporaryFile(suffix=".tar.xz", delete=False) as f:
        f.write(base)
        archive = Path(f.name)
    try:
        with tarfile.open(archive, "r:xz") as tf:
            tf.extractall(WORK)
    finally:
        archive.unlink(missing_ok=True)
    if not (WORK / "src-tauri" / "Cargo.toml").is_file():
        raise SystemExit("Trace base reconstruction failed")

    layers = LAYERS if include_transcription else LAYERS[:-1]
    for name, count, expected_len, expected_sha in layers:
        compressed = read_parts(ROOT / "bootstrap" / name, count, expected_len)
        require_sha(compressed, expected_sha, name)
        patch_bytes = lzma.decompress(compressed)
        if name == "v010":
            patch_bytes = strip_diff_sections(patch_bytes, V010_LEGACY_TESTS)
        with tempfile.NamedTemporaryFile(suffix=f"-{name}.patch", delete=False) as f:
            f.write(patch_bytes)
            patch = Path(f.name)
        try:
            git_apply(patch)
        finally:
            patch.unlink(missing_ok=True)

    tests = WORK / "tests"
    tests.mkdir(exist_ok=True)
    for test in ("schema_contract.py", *V010_LEGACY_TESTS):
        name = Path(test).name
        shutil.copy2(ROOT / "bootstrap" / "v010" / "tests" / name, tests / name)

    if include_transcription:
        for required in (
            WORK / "src-tauri" / "src" / "transcription.rs",
            WORK / "tests" / "v11_transcription.py",
        ):
            if not required.is_file():
                raise SystemExit(f"Missing reconstructed transcription file: {required}")

    print("Trace v0.11 verified layers reconstructed successfully")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--without-transcription", action="store_true")
    args = parser.parse_args()
    reconstruct(not args.without_transcription)
