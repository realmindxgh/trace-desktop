$ErrorActionPreference='Stop'

if (Test-Path work) { Remove-Item work -Recurse -Force }

# Verified Trace base.
$parts=Get-ChildItem bootstrap/v2/part* | Sort-Object Name
if ($parts.Count -ne 8) { throw "Incomplete Trace base bootstrap. Expected 8 parts, found $($parts.Count)." }
$b64=($parts | ForEach-Object { Get-Content $_.FullName -Raw }) -join ''
if ($b64.Length -ne 101964) { throw "Trace base bootstrap length mismatch: $($b64.Length)" }
$archive=Join-Path $env:RUNNER_TEMP 'trace-base.tar.xz'
[IO.File]::WriteAllBytes($archive,[Convert]::FromBase64String($b64))
$hash=(Get-FileHash $archive -Algorithm SHA256).Hash.ToLowerInvariant()
if ($hash -ne '6a444acb5b8a25a673c39ccc02374998628c36d6ad4af7e82b32564ab965c074') { throw "Trace base SHA-256 mismatch: $hash" }
New-Item -ItemType Directory -Force -Path work | Out-Null
python -c "import tarfile; tarfile.open(r'$archive','r:xz').extractall('work')"
if ($LASTEXITCODE -ne 0 -or !(Test-Path work/src-tauri/Cargo.toml)) { throw 'Trace base reconstruction failed.' }

# Verified v0.10 functional overlay.
$parts=Get-ChildItem bootstrap/v010/part* | Sort-Object Name
if ($parts.Count -ne 4) { throw "Incomplete v0.10 overlay. Expected 4 parts, found $($parts.Count)." }
$b64=($parts | ForEach-Object { Get-Content $_.FullName -Raw }) -join ''
if ($b64.Length -ne 43260) { throw "v0.10 overlay length mismatch: $($b64.Length)" }
$compressed=Join-Path $env:RUNNER_TEMP 'trace-v010.patch.xz'
[IO.File]::WriteAllBytes($compressed,[Convert]::FromBase64String($b64))
$hash=(Get-FileHash $compressed -Algorithm SHA256).Hash.ToLowerInvariant()
if ($hash -ne 'fb595dd3bbf9d23b10d4aaacd8a907119eb495448418d88bb33eb52c045633da') { throw "v0.10 overlay hash mismatch: $hash" }
$patch=Join-Path $env:RUNNER_TEMP 'trace-v010.patch'
python -c "import lzma,pathlib; pathlib.Path(r'$patch').write_bytes(lzma.decompress(pathlib.Path(r'$compressed').read_bytes()))"
if ($LASTEXITCODE -ne 0) { throw 'Could not decompress v0.10 overlay.' }
git apply --check --directory=work --exclude=tests/v07_installer.py --exclude=tests/v08_release.py --exclude=tests/v09_release.py $patch
if ($LASTEXITCODE -ne 0) { throw 'v0.10 overlay preflight failed.' }
git apply --directory=work --exclude=tests/v07_installer.py --exclude=tests/v08_release.py --exclude=tests/v09_release.py $patch
if ($LASTEXITCODE -ne 0) { throw 'v0.10 overlay application failed.' }
New-Item -ItemType Directory -Force -Path work/tests | Out-Null
foreach ($test in @('schema_contract.py','v07_installer.py','v08_release.py','v09_release.py')) { Copy-Item "bootstrap/v010/tests/$test" "work/tests/$test" -Force }

# Verified v0.11 imports/display overlay.
$parts=Get-ChildItem bootstrap/v011/part* | Sort-Object Name
if ($parts.Count -ne 2) { throw "Incomplete v0.11 overlay. Expected 2 parts, found $($parts.Count)." }
$b64=($parts | ForEach-Object { Get-Content $_.FullName -Raw }) -join ''
if ($b64.Length -ne 15296) { throw "v0.11 overlay length mismatch: $($b64.Length)" }
$compressed=Join-Path $env:RUNNER_TEMP 'trace-v011.patch.xz'
[IO.File]::WriteAllBytes($compressed,[Convert]::FromBase64String($b64))
$hash=(Get-FileHash $compressed -Algorithm SHA256).Hash.ToLowerInvariant()
if ($hash -ne '6cd4bdd47a095341ba6151d6addb73f47a005ad57110d3ade443449f9e9f40f2') { throw "v0.11 overlay hash mismatch: $hash" }
$patch=Join-Path $env:RUNNER_TEMP 'trace-v011.patch'
python -c "import lzma,pathlib; pathlib.Path(r'$patch').write_bytes(lzma.decompress(pathlib.Path(r'$compressed').read_bytes()))"
if ($LASTEXITCODE -ne 0) { throw 'Could not decompress v0.11 overlay.' }
git apply --check --directory=work $patch
if ($LASTEXITCODE -ne 0) { throw 'v0.11 overlay preflight failed.' }
git apply --directory=work $patch
if ($LASTEXITCODE -ne 0) { throw 'v0.11 overlay application failed.' }

# Verified v0.11 usability overlay.
$parts=Get-ChildItem bootstrap/v011plus/part* | Sort-Object Name
if ($parts.Count -ne 2) { throw "Incomplete v0.11 usability overlay. Expected 2 parts, found $($parts.Count)." }
$b64=($parts | ForEach-Object { Get-Content $_.FullName -Raw }) -join ''
if ($b64.Length -ne 13960) { throw "v0.11 usability overlay length mismatch: $($b64.Length)" }
$compressed=Join-Path $env:RUNNER_TEMP 'trace-v011plus.patch.xz'
[IO.File]::WriteAllBytes($compressed,[Convert]::FromBase64String($b64))
$hash=(Get-FileHash $compressed -Algorithm SHA256).Hash.ToLowerInvariant()
if ($hash -ne '60dccf75689c9f46a8e76ecee0356ecaf2e69713c6e624bbacaaa6e7b358ef5a') { throw "v0.11 usability overlay hash mismatch: $hash" }
$patch=Join-Path $env:RUNNER_TEMP 'trace-v011plus.patch'
python -c "import lzma,pathlib; pathlib.Path(r'$patch').write_bytes(lzma.decompress(pathlib.Path(r'$compressed').read_bytes()))"
if ($LASTEXITCODE -ne 0) { throw 'Could not decompress v0.11 usability overlay.' }
git apply --check --directory=work $patch
if ($LASTEXITCODE -ne 0) { throw 'v0.11 usability overlay preflight failed.' }
git apply --directory=work $patch
if ($LASTEXITCODE -ne 0) { throw 'v0.11 usability overlay application failed.' }

# Verified v0.11 local transcription overlay.
$parts=Get-ChildItem bootstrap/v011transcribe/part* | Sort-Object Name
if ($parts.Count -ne 2) { throw "Incomplete v0.11 transcription overlay. Expected 2 parts, found $($parts.Count)." }
$b64=($parts | ForEach-Object { Get-Content $_.FullName -Raw }) -join ''
if ($b64.Length -ne 17960) { throw "v0.11 transcription overlay length mismatch: $($b64.Length)" }
$compressed=Join-Path $env:RUNNER_TEMP 'trace-v011transcribe.patch.xz'
[IO.File]::WriteAllBytes($compressed,[Convert]::FromBase64String($b64))
$hash=(Get-FileHash $compressed -Algorithm SHA256).Hash.ToLowerInvariant()
if ($hash -ne '8ae71006df954e47040b79fda535b6212bc2949ce4efa7613ab90bbd0204515a') { throw "v0.11 transcription overlay hash mismatch: $hash" }
$patch=Join-Path $env:RUNNER_TEMP 'trace-v011transcribe.patch'
python -c "import lzma,pathlib; pathlib.Path(r'$patch').write_bytes(lzma.decompress(pathlib.Path(r'$compressed').read_bytes()))"
if ($LASTEXITCODE -ne 0) { throw 'Could not decompress v0.11 transcription overlay.' }
git apply --check --directory=work $patch
if ($LASTEXITCODE -ne 0) { throw 'v0.11 transcription overlay preflight failed.' }
git apply --directory=work $patch
if ($LASTEXITCODE -ne 0) { throw 'v0.11 transcription overlay application failed.' }

if (!(Test-Path work/src-tauri/src/transcription.rs) -or !(Test-Path work/tests/v11_transcription.py)) { throw 'Transcription source reconstruction is incomplete.' }
Write-Host 'Trace v0.11 transcription source reconstructed with verified Windows commands.'
