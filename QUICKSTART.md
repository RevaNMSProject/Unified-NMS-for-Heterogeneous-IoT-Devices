# ⚡ QUICK START - Fixed Installation

## Step 1: Install Python Dependencies

```powershell
pip install -r requirements.txt
```

**Note**: Ignore the sqlite3 error - it's built into Python!

## Step 2: Install Mosquitto (MQTT Broker) - Optional

### Option A: Download and Install Manually
1. Go to: https://mosquitto.org/download/
2. Download Windows installer
3. Run installer with default settings
4. Start Mosquitto:
```powershell
# Find where it installed (usually C:\Program Files\mosquitto)
& "C:\Program Files\mosquitto\mosquitto.exe"
```

### Option B: Skip Mosquitto for Now
The system will work with RESTCONF simulator only. MQTT features will be limited but you can still see the full workflow.

## Step 3: Start the System

### Method 1: Use the Startup Script (Recommended)
```powershell
.\start_nms.ps1
```

### Method 2: Manual Start (if script fails)

**Terminal 1 - RESTCONF Simulator:**
```powershell
python simulator\restconf_simulator.py
```

**Terminal 2 - MQTT Simulator (if Mosquitto installed):**
```powershell
python simulator\mqtt_simulator.py
```

**Terminal 3 - Main NMS:**
```powershell
python main.py
```

## Step 4: Open Dashboard

Open your browser to:
```
http://localhost:5000
```

## ✅ Verification

You should see:
- Terminal windows showing data collection
- Dashboard with device status
- Alarms appearing as thresholds are exceeded

## 🔧 Troubleshooting

### "sqlite3 not found" error
- **IGNORE IT** - SQLite3 is built into Python, no installation needed
- The requirements.txt has been fixed

### PowerShell script errors
- Use **Method 2: Manual Start** instead
- Open separate PowerShell windows for each command

### Mosquitto not available
- System works without it using RESTCONF only
- Or download from: https://mosquitto.org/download/

### No data in dashboard
- Wait 15-20 seconds for initial data collection
- Check that simulators are running (look for terminal output)
- Refresh browser (F5)

### Port 5000 already in use
Edit `config\config.py`:
```python
DASHBOARD_PORT = 5001
```

## 🎯 Minimal Working Setup

If you want the quickest demo:

```powershell
# Terminal 1
python simulator\restconf_simulator.py

# Terminal 2 (wait 3 seconds)
python main.py

# Browser
http://localhost:5000
```

This will show RESTCONF device monitoring without MQTT.

## 📊 Expected Output

### RESTCONF Simulator Terminal:
```
[RESTCONF Simulator] Starting on http://127.0.0.1:8080
[RESTCONF Simulator] Available endpoints:
  - GET /restconf/data/interfaces
  - GET /restconf/data/system
```

### Main NMS Terminal:
```
🛰️  UNIFIED NMS FOR HETEROGENEOUS IOT DEVICES
[Orchestrator] Starting collectors...
[Orchestrator] Started RESTCONF collector for restconf_device_001
✅ NMS System Running!
📊 Dashboard: http://localhost:5000
```

### Dashboard (Browser):
- Device table with 1+ devices
- Statistics showing device count
- Metrics being collected
- Alarms may appear as system runs

## 🚀 Success!

If you see the dashboard with devices and data, **you're done!** The system is working.

Watch for alarms to appear - they'll show in the Active Alarms section when thresholds are exceeded.

## 💡 Next Steps

1. Explore the dashboard
2. Wait for an alarm to appear
3. Try clicking "ACK" or "Resolve" buttons
4. Check the API: http://localhost:5000/api/devices
5. Read DEMO_GUIDE.md for presentation tips
