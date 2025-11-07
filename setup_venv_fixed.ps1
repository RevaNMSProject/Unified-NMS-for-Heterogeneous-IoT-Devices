# Setup Virtual Environment for NMS Project
# This script creates and activates a Python virtual environment

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "   Python Virtual Environment Setup" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
Write-Host "[1/4] Checking Python installation..." -ForegroundColor Yellow
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "      ERROR Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}
Write-Host "      OK Python found" -ForegroundColor Green

# Check if venv already exists
$venvPath = Join-Path $PSScriptRoot "venv"

if (Test-Path $venvPath) {
    Write-Host ""
    Write-Host "[2/4] Virtual environment already exists" -ForegroundColor Yellow
    $response = Read-Host "Do you want to recreate it? (y/N)"
    
    if ($response -eq 'y' -or $response -eq 'Y') {
        Write-Host "      Removing existing virtual environment..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force $venvPath
        Write-Host "      OK Removed" -ForegroundColor Green
    } else {
        Write-Host "      Using existing virtual environment" -ForegroundColor Green
        Write-Host ""
        Write-Host "To activate it manually, run:" -ForegroundColor Cyan
        Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
        Write-Host ""
        exit 0
    }
}

# Create virtual environment
Write-Host ""
Write-Host "[2/4] Creating virtual environment..." -ForegroundColor Yellow
try {
    python -m venv venv
    Write-Host "      OK Virtual environment created in ./venv/" -ForegroundColor Green
} catch {
    Write-Host "      ERROR Failed to create virtual environment" -ForegroundColor Red
    Write-Host "      Error: $_" -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host ""
Write-Host "[3/4] Activating virtual environment..." -ForegroundColor Yellow
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"

if (Test-Path $activateScript) {
    Write-Host "      OK Activation script found" -ForegroundColor Green
} else {
    Write-Host "      ERROR Activation script not found" -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host ""
Write-Host "[4/4] Installing dependencies..." -ForegroundColor Yellow
Write-Host "      This may take a few minutes..." -ForegroundColor Gray

try {
    & $activateScript
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    Write-Host "      OK Dependencies installed successfully" -ForegroundColor Green
} catch {
    Write-Host "      WARNING Some packages may have failed to install" -ForegroundColor Yellow
    Write-Host "      (sqlite3 error is normal - it is built into Python)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "==================================================" -ForegroundColor Green
Write-Host "   Virtual Environment Ready!" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Write-Host ""
Write-Host "To activate the virtual environment:" -ForegroundColor Cyan
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "To deactivate:" -ForegroundColor Cyan
Write-Host "  deactivate" -ForegroundColor White
Write-Host ""
Write-Host "To start the NMS system:" -ForegroundColor Cyan
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  .\start_nms.ps1" -ForegroundColor White
Write-Host ""
Write-Host "Or use the all-in-one script:" -ForegroundColor Cyan
Write-Host "  .\run_with_venv.ps1" -ForegroundColor White
Write-Host ""
