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


def git_apply(patch: Path, *, v010: bool = False) -> None:
    options = ["--directory=work"]
    if v010:
        options += [
            "--exclude=tests/v07_installer.py",
            "--exclude=tests/v08_release.py",
            "--exclude=tests/v09_release.py",
        ]
    # Match the established Windows workflows exactly. git-apply's include/exclude
    # path matching is sensitive to option parsing around --check on Windows.
    subprocess.run(["git", "apply", "--check", *options, str(patch)], cwd=ROOT, check=True)
    subprocess.run(["git", "apply", *options, str(patch)], cwd=ROOT, check=True)


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
        with tempfile.NamedTemporaryFile(suffix=f"-{name}.patch", delete=False) as f:
            f.write(patch_bytes)
            patch = Path(f.name)
        try:
            git_apply(patch, v010=(name == "v010"))
        finally:
            patch.unlink(missing_ok=True)

    tests = WORK / "tests"
    tests.mkdir(exist_ok=True)
    for test in ("schema_contract.py", "v07_installer.py", "v08_release.py", "v09_release.py"):
        shutil.copy2(ROOT / "bootstrap" / "v010" / "tests" / test, tests / test)

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
