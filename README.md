# 🛰️ Unified NMS for Heterogeneous IoT Devices

A complete Network Management System that monitors IoT devices using **SNMP**, **RESTCONF**, and **MQTT** protocols with unified data collection, normalization, alarm lifecycle management, and real-time dashboard.

## 🎯 Project Overview

This system demonstrates a production-ready NMS platform that:
- **Collects** data from multiple protocol types (SNMP, RESTCONF, MQTT)
- **Normalizes** heterogeneous data into unified JSON schemas
- **Manages** alarm lifecycle with state machine (OPEN → ACK → RESOLVED → CLOSED)
- **Visualizes** everything through a web dashboard
- **Runs completely locally** with simulated devices (no physical hardware needed)

## 📁 Project Structure

```
nms project/
├── config/                 # Configuration files
│   ├── config.py          # Main configuration
│   ├── devices.json       # Device definitions
│   └── schemas.json       # Data schemas
├── simulator/             # Device simulators (no hardware needed)
│   ├── snmp_simulator.py
│   ├── restconf_simulator.py
│   └── mqtt_simulator.py
├── collectors/            # Data collection layer
│   ├── snmp_collector.py
│   ├── restconf_collector.py
│   └── mqtt_collector.py
├── normalizer/            # Data normalization
│   └── normalizer.py
├── storage/               # Database and alarm engine
│   ├── storage.py
│   └── alarm_engine.py
├── dashboard/             # Web UI and API
│   ├── dashboard.py
│   └── static/
│       └── index.html
├── main.py               # Main orchestrator
└── requirements.txt      # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

#### Option 1: Virtual Environment (Recommended - Avoids Dependency Conflicts)

1. **Navigate to project directory:**
```powershell
cd "c:\Users\udayn\Documents\nms project"
```

2. **Setup virtual environment and install dependencies:**
```powershell
.\setup_venv.ps1
```
This creates an isolated Python environment and installs all dependencies automatically.

3. **For MQTT support, install Mosquitto broker (optional):**
   - Download from: https://mosquitto.org/download/

#### Option 2: Global Installation

1. **Navigate to project directory:**
```powershell
cd "c:\Users\udayn\Documents\nms project"
```

2. **Install dependencies:**
```powershell
pip install -r requirements.txt
```
Note: Ignore any "sqlite3" error - it's built into Python.

3. **For MQTT support, install Mosquitto broker:**
   - Download from: https://mosquitto.org/download/
   - Or use `choco install mosquitto` (if you have Chocolatey)

## 🎬 Running the System

### Option 1: With Virtual Environment (Recommended)

**One command to rule them all:**
```powershell
.\run_with_venv.ps1
```

This automatically:
- Activates the virtual environment
- Starts all simulators
- Starts the main NMS system
- Opens the dashboard in your browser

### Option 2: Manual Start (With Virtual Environment)

```powershell
# Activate virtual environment first
.\venv\Scripts\Activate.ps1

# Terminal 1: Start RESTCONF simulator
python simulator\restconf_simulator.py

# Terminal 2: Start MQTT simulator (if Mosquitto running)
python simulator\mqtt_simulator.py

# Terminal 3: Start main NMS system
python main.py
```

Then open your browser to: **http://localhost:5000**

### Option 3: Without Virtual Environment

**Start Simulators:**
```powershell
# RESTCONF simulator
python simulator\restconf_simulator.py

# MQTT simulator (requires mosquitto broker running)
python simulator\mqtt_simulator.py
```

**Start Main System:**
```powershell
python main.py
```

## 📊 Dashboard Features

Access the dashboard at `http://localhost:5000`

### Real-time Monitoring
- **Device Status**: View all monitored devices
- **Protocol Health**: SNMP, RESTCONF, MQTT statistics
- **Alarm Wall**: Active alarms by severity and state
- **Metrics**: Time-series telemetry data

### Operator Actions
- **Acknowledge** alarms (OPEN → ACK)
- **Resolve** alarms manually
- **Close** alarms
- Auto-refresh every 5 seconds

## 📡 API Endpoints

Base URL: `http://localhost:5000/api`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/devices` | GET | Get all devices summary |
| `/metrics` | GET | Get metrics (supports filters) |
| `/alarms` | GET | Get alarms (supports filters) |
| `/alarms/stats` | GET | Get alarm statistics |
| `/alarms/{id}/acknowledge` | POST | Acknowledge alarm |
| `/alarms/{id}/resolve` | POST | Resolve alarm |
| `/alarms/{id}/close` | POST | Close alarm |

**Example:**
```powershell
# Get all devices
curl http://localhost:5000/api/devices

# Get critical alarms
curl http://localhost:5000/api/alarms?severity=CRITICAL

# Acknowledge an alarm
curl -X POST http://localhost:5000/api/alarms/snmp_device_001_cpu_usage_threshold_exceeded/acknowledge
```

## 🧩 Data Flow

```
┌─────────────┐
│  Simulators │  (SNMP/RESTCONF/MQTT devices)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Collectors  │  (Protocol-specific data gathering)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Normalizer  │  (Unified JSON format + threshold checking)
└──────┬──────┘
       │
       ├──────▶ Metrics ──▶ Storage (SQLite)
       │
       └──────▶ Events ───▶ Alarm Engine ──▶ Storage
                                 │
                                 ▼
                           ┌─────────────┐
                           │  Dashboard  │  (Web UI + API)
                           └─────────────┘
```

## 📋 Alarm Lifecycle

```
OPEN ──(operator)──▶ ACK ──(operator/auto)──▶ RESOLVED ──(auto after 5min)──▶ CLOSED
  │                                               ▲
  └───────────(operator/auto)────────────────────┘
```

### States:
- **OPEN**: New alarm triggered
- **ACK**: Operator acknowledged
- **RESOLVED**: Condition cleared or manually resolved
- **CLOSED**: Auto-closed after timeout or operator action

### Features:
- ✅ De-duplication (same alarm increments counter)
- ✅ Auto-resolve when metrics return to normal
- ✅ Auto-close after 5 minutes in RESOLVED state
- ✅ Operator actions via dashboard

## 🔧 Configuration

### Adding Devices

Edit `config/devices.json`:

```json
{
  "devices": [
    {
      "device_id": "my_new_device",
      "device_type": "sensor",
      "protocol": "MQTT",
      "location": "Lab-1",
      "broker": "127.0.0.1",
      "port": 1883,
      "topics": ["iot/my_sensor"]
    }
  ]
}
```

### Setting Thresholds

In `config/devices.json`:

```json
{
  "thresholds": {
    "cpu_usage": {"warning": 70, "critical": 85},
    "temp_celsius": {"warning": 35, "critical": 40}
  }
}
```

## 🧪 Testing

### Test Individual Collectors

```powershell
# Test SNMP collector
python collectors\snmp_collector.py

# Test RESTCONF collector (requires simulator running)
python collectors\restconf_collector.py

# Test MQTT collector (requires broker + simulator)
python collectors\mqtt_collector.py
```

### Generate Test Alarms

The simulators automatically generate threshold violations:
- **MQTT**: Temperature can spike to 45°C (threshold: 40°C)
- **MQTT**: Humidity can reach 90% (threshold: 80%)
- **RESTCONF**: Interfaces randomly go down

## 📈 Key Metrics Collected

| Protocol | Metrics |
|----------|---------|
| **SNMP** | CPU usage, Memory usage, Uptime |
| **RESTCONF** | Interface status, System CPU, Temperature, Packet counts |
| **MQTT** | Temperature, Humidity, Pressure |

## 🛠️ Troubleshooting

### Mosquitto not running
```powershell
# Install Mosquitto
choco install mosquitto

# Or download from https://mosquitto.org/download/
# Start the service
net start mosquitto
```

### Port 5000 already in use
Edit `config/config.py`:
```python
DASHBOARD_PORT = 5001  # Change to any free port
```

### No data in dashboard
1. Ensure simulators are running
2. Check collector output for errors
3. Verify database exists: `storage/nms.db`

## 📚 Technologies Used

- **Python 3.8+**
- **Flask** - Web framework
- **PySNMP** - SNMP protocol
- **Paho MQTT** - MQTT client
- **Requests** - HTTP/RESTCONF
- **SQLite3** - Time-series storage
- **HTML/CSS/JavaScript** - Dashboard UI

## 🎓 Learning Outcomes

This project demonstrates:
1. ✅ Protocol abstraction and normalization
2. ✅ Event-driven architecture
3. ✅ State machine implementation (alarm lifecycle)
4. ✅ RESTful API design
5. ✅ Real-time dashboard with auto-refresh
6. ✅ Multi-threaded data collection
7. ✅ Time-series data storage
8. ✅ Threshold-based alerting

## 🚧 Future Enhancements

- [ ] Add Grafana integration
- [ ] Implement notification system (email/SMS)
- [ ] Add historical trending charts
- [ ] Support NETCONF protocol
- [ ] Add user authentication
- [ ] Export reports (PDF/CSV)
- [ ] Docker containerization

## 📝 License

Educational project for NMS demonstration purposes.


---

**🎯 Result:** A fully functioning, demonstration-ready unified NMS platform running entirely on your laptop!
