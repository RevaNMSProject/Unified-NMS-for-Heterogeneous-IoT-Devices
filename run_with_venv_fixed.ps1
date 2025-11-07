# Run NMS with Virtual Environment
# This script automatically activates venv and runs the NMS system

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "   NMS with Virtual Environment" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

$venvPath = Join-Path $PSScriptRoot "venv"
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"

# Check if venv exists
if (-not (Test-Path $venvPath)) {
    Write-Host "Virtual environment not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Creating virtual environment first..." -ForegroundColor Yellow
    Write-Host ""
    
    & "$PSScriptRoot\setup_venv_fixed.ps1"
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

# Activate virtual environment
Write-Host "[VENV] Activating virtual environment..." -ForegroundColor Yellow

try {
    & $activateScript
    Write-Host "[VENV] OK Virtual environment activated" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "[VENV] ERROR Failed to activate virtual environment" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}

# Start RESTCONF Simulator in venv
Write-Host "[STEP 1/3] Starting RESTCONF Simulator..." -ForegroundColor Yellow
$scriptPath = $PSScriptRoot
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptPath'; .\venv\Scripts\Activate.ps1; Write-Host 'RESTCONF Simulator (venv)' -ForegroundColor Cyan; python simulator\restconf_simulator.py"
Start-Sleep -Seconds 3
Write-Host "           OK RESTCONF Simulator started" -ForegroundColor Green

# Start MQTT Simulator in venv
Write-Host "[STEP 2/3] Starting MQTT Simulator..." -ForegroundColor Yellow
$mosquitto = Get-Process -Name mosquitto -ErrorAction SilentlyContinue
if ($mosquitto) {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptPath'; .\venv\Scripts\Activate.ps1; Write-Host 'MQTT Simulator (venv)' -ForegroundColor Magenta; python simulator\mqtt_simulator.py"
    Start-Sleep -Seconds 3
    Write-Host "           OK MQTT Simulator started" -ForegroundColor Green
} else {
    Write-Host "           WARNING Mosquitto not running - skipping MQTT simulator" -ForegroundColor Yellow
    Write-Host "           (Install from https://mosquitto.org/download/)" -ForegroundColor Gray
}

# Start Main NMS in venv
Write-Host "[STEP 3/3] Starting NMS Main System..." -ForegroundColor Yellow
Start-Sleep -Seconds 2
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptPath'; .\venv\Scripts\Activate.ps1; Write-Host 'NMS Main System (venv)' -ForegroundColor Green; python main.py"

Write-Host ""
Write-Host "==================================================" -ForegroundColor Green
Write-Host "   NMS Starting with Virtual Environment!" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "Opening dashboard..." -ForegroundColor Cyan
Start-Process "http://localhost:5000"

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Dashboard: http://localhost:5000" -ForegroundColor Cyan
Write-Host "API:       http://localhost:5000/api/" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Check the terminal windows to monitor the system" -ForegroundColor Yellow
Write-Host "Press Ctrl+C in each window to stop" -ForegroundColor Gray
Write-Host ""
