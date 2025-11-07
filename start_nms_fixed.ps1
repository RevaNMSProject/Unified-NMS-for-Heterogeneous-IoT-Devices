# Quick Start Script for Unified NMS

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "   UNIFIED NMS QUICK START" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "This script will:" -ForegroundColor Yellow
Write-Host "  1. Start device simulators (RESTCONF + MQTT)" -ForegroundColor White
Write-Host "  2. Start the main NMS system" -ForegroundColor White
Write-Host "  3. Open the dashboard in your browser" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to continue..."

# Check Python
Write-Host ""
Write-Host "[CHECK] Verifying Python installation..." -ForegroundColor Yellow
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "ERROR: Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}
Write-Host "        OK Python found" -ForegroundColor Green

# Check dependencies
Write-Host "[CHECK] Checking dependencies..." -ForegroundColor Yellow
Write-Host "        (If this fails, run: pip install -r requirements.txt)" -ForegroundColor Gray

# Start Mosquitto
Write-Host ""
Write-Host "[STEP 1/4] Starting MQTT Broker..." -ForegroundColor Yellow
$mosquitto = Get-Process -Name mosquitto -ErrorAction SilentlyContinue
if ($mosquitto) {
    Write-Host "           OK Mosquitto already running" -ForegroundColor Green
} else {
    Write-Host "           WARNING Mosquitto not found - MQTT features will be limited" -ForegroundColor Yellow
    Write-Host "           (Optional: Install from https://mosquitto.org/download/)" -ForegroundColor Gray
}

# Start RESTCONF Simulator
Write-Host "[STEP 2/4] Starting RESTCONF Simulator..." -ForegroundColor Yellow
$scriptPath = $PSScriptRoot
$pythonExe = Join-Path $scriptPath ".venv\Scripts\python.exe"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptPath'; Write-Host 'RESTCONF Simulator' -ForegroundColor Cyan; & '$pythonExe' simulator\restconf_simulator.py"
Start-Sleep -Seconds 3
Write-Host "           OK RESTCONF Simulator running on http://127.0.0.1:8080" -ForegroundColor Green

# Start MQTT Simulator
Write-Host "[STEP 3/4] Starting MQTT Simulator..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptPath'; Write-Host 'MQTT Simulator' -ForegroundColor Magenta; & '$pythonExe' simulator\mqtt_simulator.py"
Start-Sleep -Seconds 3
Write-Host "           OK MQTT Simulator publishing data" -ForegroundColor Green

# Start Main NMS
Write-Host "[STEP 4/4] Starting NMS System..." -ForegroundColor Yellow
Start-Sleep -Seconds 2
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptPath'; Write-Host 'NMS Main System' -ForegroundColor Green; & '$pythonExe' main.py"

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "   NMS SYSTEM STARTING..." -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Waiting for dashboard to be ready..." -ForegroundColor Yellow

# Wait for dashboard
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "Opening dashboard in browser..." -ForegroundColor Cyan
Start-Process "http://localhost:5000"

Write-Host ""
Write-Host "==================================================" -ForegroundColor Green
Write-Host "   NMS IS RUNNING!" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Dashboard: http://localhost:5000" -ForegroundColor Cyan
Write-Host "API:       http://localhost:5000/api/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Check the opened terminal windows to monitor:" -ForegroundColor Yellow
Write-Host "  - RESTCONF Simulator" -ForegroundColor White
Write-Host "  - MQTT Simulator" -ForegroundColor White
Write-Host "  - NMS Main System" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C in each window to stop the system" -ForegroundColor Gray
Write-Host ""
