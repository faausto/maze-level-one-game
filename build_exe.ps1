$ErrorActionPreference = "Stop"

python -m PyInstaller --clean --noconfirm MazeLevelOneGame.spec

if ($LASTEXITCODE -ne 0) {
    throw "Falló la compilación del ejecutable"
}

Get-Item "dist\MazeLevelOneGame.exe" | Select-Object FullName, @{N = 'MB'; E = { [math]::Round($_.Length / 1MB, 1) } }
