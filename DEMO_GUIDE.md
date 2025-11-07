# Unified NMS - Project Demonstration Guide

## Overview
This guide helps you demonstrate the complete NMS system for presentations, reports, or evaluations.

## Pre-Demo Checklist

- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Mosquitto MQTT broker installed and running
- [ ] Browser ready (Chrome/Edge/Firefox)
- [ ] Terminal windows prepared
- [ ] Understanding of key features

## Demo Flow (15-20 minutes)

### Part 1: Introduction (2 min)

**Talking Points:**
- "This is a unified NMS that monitors IoT devices using three different protocols"
- "No physical hardware needed - everything is simulated"
- "Demonstrates real-world network monitoring concepts"

**Show:**
- Project structure in file explorer
- Architecture diagram (can draw on whiteboard)

### Part 2: Starting the System (3 min)

**Execute:**
```powershell
.\start_nms.ps1
```

**Point out:**
1. Simulators starting (terminal windows)
2. Device types being simulated:
   - RESTCONF: Network switch
   - MQTT: Temperature, humidity, pressure sensors
3. Collectors gathering data from each protocol
4. Dashboard starting on port 5000

**Show terminals:**
- RESTCONF Simulator: "See the REST API responding"
- MQTT Simulator: "Publishing sensor readings"
- Main NMS: "Collectors running, normalizing data"

### Part 3: Dashboard Tour (5 min)

**Navigate to http://localhost:5000**

**Statistics Cards:**
- "Real-time device count"
- "Alarm severities: Critical vs Warning"
- "Auto-refreshes every 5 seconds"

**Device Status Table:**
- "All monitored devices listed"
- "Different protocols color-coded"
- "Last seen timestamps"
- "Active alarm counts per device"

**Active Alarms Table:**
- "Alarm lifecycle states"
- "Severity levels"
- "Occurrence counters (de-duplication)"
- "Operator action buttons"

### Part 4: Alarm Lifecycle Demo (5 min)

**Wait for alarm to appear** (simulators will generate threshold violations)

**Show the state progression:**

1. **OPEN State:**
   - "New alarm appears in red"
   - "Threshold exceeded - temperature > 40°C"
   - "Operator hasn't acted yet"

2. **Acknowledge:**
   - Click "ACK" button
   - "State changes to ACK (yellow)"
   - "Operator knows about the issue"

3. **Resolve:**
   - Click "Resolve" button
   - "State changes to RESOLVED (green)"
   - "Issue is fixed"

4. **Auto-Close:**
   - "After 5 minutes in RESOLVED, automatically closes"
   - "Or operator can close immediately"

**Demonstrate de-duplication:**
- "Same alarm occurring multiple times increments counter"
- "Prevents alarm flooding"

### Part 5: API Demonstration (3 min)

**Open new PowerShell window:**

```powershell
# Show all devices
curl http://localhost:5000/api/devices | ConvertFrom-Json

# Show alarm statistics
curl http://localhost:5000/api/alarms/stats | ConvertFrom-Json

# Show recent metrics
curl http://localhost:5000/api/metrics?limit=5 | ConvertFrom-Json
```

**Talking points:**
- "RESTful API for programmatic access"
- "Can integrate with other systems"
- "JSON responses - standard format"

### Part 6: Data Normalization Demo (2 min)

**Show in code editor:**

1. Open `normalizer/normalizer.py`
   - "Different protocols use different parameter names"
   - "Normalizer converts to standard names"
   - "Example: SNMP 'cpu_usage' → MQTT 'temp1' → unified 'temp_celsius'"

2. Open `config/devices.json`
   - "Threshold configuration"
   - "Same thresholds applied across all protocols"

### Part 7: Technical Architecture (3 min)

**Show the flow:**

```
Simulators → Collectors → Normalizer → Storage
                                         ↓
                                    Alarm Engine
                                         ↓
                                    Dashboard
```

**Key technical points:**
- "Multi-threaded collectors run concurrently"
- "SQLite for time-series storage"
- "State machine for alarm lifecycle"
- "Flask REST API with CORS"
- "Real-time web interface with auto-refresh"

## Common Questions & Answers

**Q: Does this work with real devices?**
A: Yes! Just update `config/devices.json` with real IP addresses and credentials. The collectors will work with actual SNMP agents, RESTCONF devices, and MQTT brokers.

**Q: Why these three protocols?**
A: They represent the heterogeneous nature of IoT - SNMP for traditional network devices, RESTCONF for modern programmable infrastructure, MQTT for lightweight IoT sensors.

**Q: How scalable is this?**
A: The architecture supports scaling. For production, you'd use a proper time-series DB (InfluxDB), message queue (RabbitMQ), and distributed collectors.

**Q: Can you add more protocols?**
A: Absolutely! Just create a new collector following the same pattern, and the normalizer will handle it.

## Demonstration Scenarios

### Scenario 1: Network Monitoring
- Focus on RESTCONF device
- Show interface status changes
- Demonstrate link down/up events

### Scenario 2: Environmental Monitoring
- Focus on MQTT sensors
- Watch temperature/humidity/pressure
- Show threshold violation alarms

### Scenario 3: Alarm Management
- Show multiple alarms appearing
- Demonstrate operator workflow (ACK → Resolve → Close)
- Highlight de-duplication

## Screen Recording Tips

If recording for video demonstration:

1. **Set up 4-panel layout:**
   - Top-left: Dashboard
   - Top-right: API calls
   - Bottom-left: MQTT Simulator output
   - Bottom-right: Main NMS output

2. **Zoom settings:**
   - Browser zoom: 110-125%
   - Terminal font size: 14-16pt
   - Clear terminal history before starting

3. **Narration points:**
   - Start with problem statement
   - Explain each component as you start it
   - Highlight real-time updates
   - Emphasize unified monitoring concept

## Post-Demo

**Files to highlight:**
- `README.md` - Complete documentation
- `INSTALLATION.md` - Setup guide
- `config/schemas.json` - Data model
- Database file at `storage/nms.db`

**Next steps suggestion:**
- "Can be extended with Grafana dashboards"
- "Add email/SMS notifications"
- "Integrate with ticketing systems"
- "Deploy on cloud infrastructure"

## Troubleshooting During Demo

**If simulators aren't generating alarms:**
- Wait 30-60 seconds
- Restart MQTT simulator (generates more random values)

**If dashboard is empty:**
- Check collectors are running (main.py output)
- Verify simulators are active
- Refresh browser (F5)

**If Mosquitto fails:**
- Show alternative: use public MQTT broker
- Or demonstrate with just RESTCONF

## Success Metrics

A successful demo shows:
- ✅ Multiple protocols collecting data
- ✅ Unified visualization
- ✅ Alarm lifecycle working
- ✅ Real-time updates
- ✅ Operator actions functional
- ✅ API responses correct
- ✅ Clean, professional interface

---

**Remember:** This demonstrates production NMS concepts in a educational/proof-of-concept format. Emphasize the architecture and workflows rather than focusing on performance benchmarks.
