# PowerShell Build Script for QR Code Generator Pro Windows Executable

[CmdletBinding()]
param (
    [switch]$CleanOnly,
    [string]$Spec = "generator.spec"
)

$ErrorActionPreference = "Stop"

Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host " QR Code Generator Pro - Windows Executable Packaging" -ForegroundColor Cyan
Write-Host "========================================================`n" -ForegroundColor Cyan

# Locate Python executable (prefer project venv if available)
$pythonCmd = "python"
if (Test-Path ".\venv\Scripts\python.exe") {
    $pythonCmd = ".\venv\Scripts\python.exe"
}

try {
    $pythonVersion = & $pythonCmd --version 2>&1
    Write-Host "[OK] Using $pythonCmd ($pythonVersion)" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python was not found." -ForegroundColor Red
    Write-Host "Please install Python 3.9+ or set up the virtual environment." -ForegroundColor Yellow
    exit 1
}

# Construct arguments for build.py
$buildArgs = @("build.py", "--spec", $Spec)
if ($CleanOnly) {
    $buildArgs += "--clean-only"
}

# Run build.py
& $pythonCmd @buildArgs

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nPackaging completed successfully!`n" -ForegroundColor Green
} else {
    Write-Host "`nPackaging failed with exit code $LASTEXITCODE.`n" -ForegroundColor Red
    exit $LASTEXITCODE
}
