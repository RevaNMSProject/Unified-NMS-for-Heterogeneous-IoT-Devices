# 🚀 QUICK REFERENCE CARD

## Unified NMS - Essential Commands & Info

---

## 🏃 Quick Start

```powershell
# Install dependencies
pip install -r requirements.txt

# Run everything (automated)
.\start_nms.ps1

# Open dashboard
http://localhost:5000
```

---

## 📁 Project Structure (at a glance)

```
nms project/
├── config/          → Settings & device definitions
├── simulator/       → Device simulators (no hardware)
├── collectors/      → Data collection (SNMP/REST/MQTT)
├── normalizer/      → Data transformation
├── storage/         → Database & alarm engine
├── dashboard/       → Web UI & API
└── main.py         → Start here
```

---

## 🔧 Manual Startup (4 terminals)

```powershell
# Terminal 1: MQTT Broker
mosquitto

# Terminal 2: RESTCONF Simulator
python simulator\restconf_simulator.py

# Terminal 3: MQTT Simulator
python simulator\mqtt_simulator.py

# Terminal 4: Main NMS
python main.py
```

---

## 🌐 URLs

| Service | URL |
|---------|-----|
| Dashboard | http://localhost:5000 |
| API Base | http://localhost:5000/api/ |
| RESTCONF Sim | http://localhost:8080 |
| MQTT Broker | localhost:1883 |

---

## 📡 API Endpoints

```powershell
# Get all devices
curl http://localhost:5000/api/devices

# Get alarms
curl http://localhost:5000/api/alarms

# Get metrics
curl http://localhost:5000/api/metrics?limit=10

# Alarm statistics
curl http://localhost:5000/api/alarms/stats

# Acknowledge alarm
curl -X POST http://localhost:5000/api/alarms/{ALARM_ID}/acknowledge

# Resolve alarm
curl -X POST http://localhost:5000/api/alarms/{ALARM_ID}/resolve

# Close alarm
curl -X POST http://localhost:5000/api/alarms/{ALARM_ID}/close
```

---

## 🔄 Alarm States

```
OPEN → ACK → RESOLVED → CLOSED
```

- **OPEN**: New alarm (red)
- **ACK**: Acknowledged by operator (yellow)
- **RESOLVED**: Issue cleared (green)
- **CLOSED**: Final state (gray)

---

## 📊 Data Flow (simplified)

```
Device Simulator → Collector → Normalizer → Storage → Dashboard
                                    ↓
                              Alarm Engine
```

---

## 🎯 Protocols Supported

| Protocol | Port | Metrics |
|----------|------|---------|
| SNMP | 161 | CPU, Memory, Uptime |
| RESTCONF | 8080 | Interfaces, System |
| MQTT | 1883 | Temp, Humidity, Pressure |

---

## ⚙️ Configuration Files

| File | Purpose |
|------|---------|
| `config/config.py` | Intervals, ports, paths |
| `config/devices.json` | Device definitions |
| `config/schemas.json` | Data model |

---

## 🗄️ Database

**Location**: `storage/nms.db`

**Tables**:
- `metrics` - Time-series telemetry
- `alarms` - Alarm lifecycle

**View with**: DB Browser for SQLite

---

## 🧪 Testing

```powershell
# Test installation
python test_installation.py

# Test individual collectors
python collectors\snmp_collector.py
python collectors\restconf_collector.py
python collectors\mqtt_collector.py
```

---

## 🛠️ Troubleshooting

### No data in dashboard?
- Wait 15-20 seconds for initial collection
- Check simulators are running
- Verify main.py is running

### Mosquitto not found?
```powershell
choco install mosquitto
# Or download from mosquitto.org
```

### Port 5000 in use?
Edit `config/config.py`:
```python
DASHBOARD_PORT = 5001
```

### Import errors?
```powershell
pip install -r requirements.txt --upgrade
```

---

## 📋 Dashboard Features

- ✅ Real-time device status
- ✅ Active alarms wall
- ✅ Statistics cards
- ✅ Auto-refresh (5s)
- ✅ Operator actions
- ✅ Color-coded severities

---

## 🎓 Demo Scenario

1. Start system → `.\start_nms.ps1`
2. Open dashboard → `http://localhost:5000`
3. Watch devices appear
4. Wait for alarm (temp > 40°C)
5. Click "ACK" button
6. Click "Resolve" button
7. Watch auto-close after 5 min

---

## 📚 Documentation

| File | Content |
|------|---------|
| README.md | Full documentation |
| INSTALLATION.md | Setup guide |
| DEMO_GUIDE.md | Presentation tips |
| ARCHITECTURE.md | System design |
| PROJECT_SUMMARY.md | Completion summary |

---

## 🔑 Key Features

✅ Multi-protocol support (SNMP, RESTCONF, MQTT)
✅ Data normalization
✅ Alarm lifecycle (4 states)
✅ De-duplication
✅ Auto-resolution
✅ Web dashboard
✅ REST API
✅ No hardware needed

---

## 💾 Data Schema (Unified)

### Metric
```json
{
  "device_id": "device_001",
  "parameter": "cpu_usage",
  "value": 75.5,
  "unit": "percent",
  "timestamp": "2025-11-06T10:30:00Z"
}
```

### Alarm
```json
{
  "device_id": "device_001",
  "severity": "CRITICAL",
  "state": "OPEN",
  "message": "CPU exceeded 85%"
}
```

---

## 🎯 Thresholds (Default)

| Parameter | Warning | Critical |
|-----------|---------|----------|
| cpu_usage | 70% | 85% |
| memory_usage | 75% | 90% |
| temp_celsius | 35°C | 40°C |
| humidity_percent | 80% | 90% |
| pressure_kpa | 105 | 110 |

**Edit**: `config/devices.json`

---

## ⏱️ Collection Intervals

- SNMP: 10 seconds
- RESTCONF: 15 seconds
- MQTT: Real-time (event-driven)

**Edit**: `config/config.py`

---

## 🔐 Default Credentials

**RESTCONF Simulator**:
- Username: `admin`
- Password: `admin`

**MQTT**: No authentication (localhost)

---

## 🎨 Dashboard Color Codes

- 🔴 **Red**: CRITICAL / OPEN
- 🟡 **Yellow**: WARNING / ACK
- 🟢 **Green**: RESOLVED
- ⚪ **Gray**: CLOSED

**Protocols**:
- 🔵 **Blue**: SNMP
- 🟣 **Purple**: RESTCONF
- 🔴 **Pink**: MQTT

---

## 📊 Statistics Displayed

- Total Devices
- Critical Alarms
- Warnings
- Resolved Alarms
- Active vs Closed

---

## 🧹 Clean Restart

```powershell
# Stop all processes (Ctrl+C in each terminal)

# Delete database
Remove-Item storage\nms.db

# Restart
.\start_nms.ps1
```

---

## 🎬 Essential Commands Summary

```powershell
# Install
pip install -r requirements.txt

# Test
python test_installation.py

# Start (auto)
.\start_nms.ps1

# Start (manual simulators)
.\start_simulators.ps1

# Start main system
python main.py

# View logs
# Check terminal windows

# Stop
# Ctrl+C in each window
```

---

## 📞 Quick Help

**Everything working?** → Open http://localhost:5000
**Installation issues?** → Run `python test_installation.py`
**No alarms?** → Wait 30-60 seconds
**API not responding?** → Check main.py is running

---

## ✅ Success Checklist

- [ ] Dependencies installed
- [ ] Mosquitto running
- [ ] Simulators started
- [ ] Main.py running
- [ ] Dashboard accessible
- [ ] Devices visible
- [ ] Alarms appearing
- [ ] Actions working

---

**🎯 Remember**: This is a complete, production-quality demonstration system. Everything is functional and ready to show!

**📖 For detailed info**: See README.md and other docs

**🚀 Ready to run**: `.\start_nms.ps1`
