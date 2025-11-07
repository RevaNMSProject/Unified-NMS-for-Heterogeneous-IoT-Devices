# Unified NMS - Installation & Setup Guide

## Quick Installation

### 1. Install Python Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Install Mosquitto MQTT Broker

**Option A: Using Chocolatey (Recommended)**
```powershell
choco install mosquitto
```

**Option B: Manual Installation**
1. Download from: https://mosquitto.org/download/
2. Install with default settings
3. Start the service:
```powershell
net start mosquitto
```

### 3. Verify Installation

```powershell
# Check Python packages
pip list

# Check Mosquitto
mosquitto -h
```

## Running the System

### Method 1: Automated Start (Easiest)

```powershell
.\start_nms.ps1
```

This will:
- Start all simulators
- Launch the NMS system
- Open the dashboard in your browser

### Method 2: Manual Start (Step-by-step)

**Terminal 1 - MQTT Broker:**
```powershell
mosquitto
```

**Terminal 2 - RESTCONF Simulator:**
```powershell
python simulator\restconf_simulator.py
```

**Terminal 3 - MQTT Simulator:**
```powershell
python simulator\mqtt_simulator.py
```

**Terminal 4 - Main NMS:**
```powershell
python main.py
```

**Browser:**
```
http://localhost:5000
```

## Troubleshooting

### Issue: "Module not found" errors

**Solution:**
```powershell
pip install -r requirements.txt --upgrade
```

### Issue: Mosquitto not starting

**Solution:**
```powershell
# Check if already running
Get-Process mosquitto

# Start manually
& "C:\Program Files\mosquitto\mosquitto.exe"
```

### Issue: Port 5000 already in use

**Solution:**
Edit `config\config.py`:
```python
DASHBOARD_PORT = 5001  # Change to any available port
```

### Issue: No data appearing in dashboard

**Check:**
1. Are all simulators running? (Check terminal windows)
2. Is the main NMS running? (Check for error messages)
3. Wait 10-15 seconds for initial data collection
4. Check browser console for errors (F12)

### Issue: SNMP not working

**Note:** SNMP simulator is simplified. The system works without it using RESTCONF and MQTT.

## Testing API Endpoints

```powershell
# Get devices
curl http://localhost:5000/api/devices | ConvertFrom-Json

# Get alarms
curl http://localhost:5000/api/alarms | ConvertFrom-Json

# Get metrics
curl http://localhost:5000/api/metrics?limit=10 | ConvertFrom-Json
```

## Database Location

```
storage\nms.db
```

View with any SQLite browser:
- https://sqlitebrowser.org/

## Stopping the System

Press `Ctrl+C` in each terminal window to stop:
1. Main NMS
2. MQTT Simulator
3. RESTCONF Simulator
4. Mosquitto (optional - can keep running)

## Clean Start

To reset all data:

```powershell
# Stop all processes
# Then delete the database
Remove-Item storage\nms.db

# Restart the system
.\start_nms.ps1
```

## Next Steps

1. ✅ Install dependencies
2. ✅ Run the quick start script
3. ✅ Open dashboard at http://localhost:5000
4. ✅ Watch alarms appear as simulators generate data
5. ✅ Try operator actions (ACK, Resolve, Close alarms)
6. ✅ Explore the API endpoints

## Support

For issues:
1. Check this guide
2. Review README.md
3. Check terminal output for error messages
4. Verify all prerequisites are installed
