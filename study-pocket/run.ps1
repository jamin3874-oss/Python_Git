$ErrorActionPreference='Stop'
Set-Location -LiteralPath $PSScriptRoot
node scripts/build.mjs
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B server.py
