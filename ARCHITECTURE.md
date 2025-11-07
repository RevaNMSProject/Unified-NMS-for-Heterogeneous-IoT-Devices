# Unified NMS System Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    UNIFIED NMS FOR HETEROGENEOUS IOT                     │
│                   Network Management System Platform                     │
└─────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────── PRESENTATION LAYER ─────────────────────────┐
│                                                                           │
│  ┌─────────────────────┐              ┌──────────────────────┐          │
│  │   Web Dashboard     │              │    REST API          │          │
│  │   (index.html)      │◄────────────►│  (dashboard.py)      │          │
│  │                     │              │                      │          │
│  │ • Device Status     │              │ • /api/devices       │          │
│  │ • Alarm Wall        │              │ • /api/metrics       │          │
│  │ • Real-time Stats   │              │ • /api/alarms        │          │
│  │ • Operator Actions  │              │ • /api/alarms/stats  │          │
│  └─────────────────────┘              └──────────────────────┘          │
│           ▲                                      ▲                        │
│           │                                      │                        │
│           └──────────────┬───────────────────────┘                        │
│                          │ HTTP/JSON                                      │
└──────────────────────────┼────────────────────────────────────────────────┘
                           │
┌──────────────────────────┼───────── BUSINESS LOGIC LAYER ────────────────┐
│                          ▼                                                │
│  ┌─────────────────────────────────────────────────────────┐            │
│  │            Alarm Lifecycle Engine                        │            │
│  │           (alarm_engine.py)                              │            │
│  │                                                           │            │
│  │  State Machine: OPEN → ACK → RESOLVED → CLOSED          │            │
│  │                                                           │            │
│  │  • Threshold Detection                                   │            │
│  │  • De-duplication (occurrence counting)                  │            │
│  │  • Auto-resolution (when metrics normalize)              │            │
│  │  • Auto-close (after timeout)                            │            │
│  │  • Operator actions (ACK/Resolve/Close)                  │            │
│  └─────────────────────────────────────────────────────────┘            │
│                          ▲                                                │
│                          │                                                │
│  ┌─────────────────────────────────────────────────────────┐            │
│  │         Data Normalizer & Enrichment                     │            │
│  │              (normalizer.py)                             │            │
│  │                                                           │            │
│  │  Input:  Protocol-specific raw data                      │            │
│  │  Output: Unified JSON schema                             │            │
│  │                                                           │            │
│  │  • Parameter name standardization                        │            │
│  │  • Value type conversion                                 │            │
│  │  • Unit mapping                                          │            │
│  │  • Metadata enrichment                                   │            │
│  │  • Threshold checking                                    │            │
│  │  • Event generation                                      │            │
│  └─────────────────────────────────────────────────────────┘            │
│                          ▲                                                │
└──────────────────────────┼───────────────────────────────────────────────┘
                           │
┌──────────────────────────┼──────── DATA COLLECTION LAYER ────────────────┐
│                          │                                                │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐                │
│  │    SNMP      │   │  RESTCONF    │   │     MQTT     │                │
│  │  Collector   │   │  Collector   │   │  Collector   │                │
│  │              │   │              │   │              │                │
│  │ • Poll OIDs  │   │ • GET APIs   │   │ • Subscribe  │                │
│  │ • 10s cycle  │   │ • 15s cycle  │   │ • QoS 1      │                │
│  │ • Community  │   │ • REST/JSON  │   │ • Topics     │                │
│  │   strings    │   │ • Auth       │   │              │                │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘                │
│         │                  │                  │                          │
│         │                  │                  │                          │
│         ▼                  ▼                  ▼                          │
│  ┌──────────────────────────────────────────────────────────┐          │
│  │        Main Orchestrator (main.py)                        │          │
│  │                                                            │          │
│  │  • Multi-threaded collector management                    │          │
│  │  • Data flow coordination                                 │          │
│  │  • Periodic maintenance tasks                             │          │
│  └────────────────────────────────────────────────────────────┘         │
│                          ▲                                                │
└──────────────────────────┼───────────────────────────────────────────────┘
                           │
┌──────────────────────────┼──────── DEVICE SIMULATION LAYER ──────────────┐
│                          │                                                │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐                │
│  │    SNMP      │   │  RESTCONF    │   │     MQTT     │                │
│  │  Simulator   │   │  Simulator   │   │  Simulator   │                │
│  │              │   │              │   │              │                │
│  │ • Mock OIDs  │   │ • Flask API  │   │ • Publishers │                │
│  │ • Random     │   │ • Port 8080  │   │ • Sensors    │                │
│  │   values     │   │ • Interfaces │   │ • Temp/Humid │                │
│  │              │   │ • System     │   │ • Pressure   │                │
│  └──────────────┘   └──────────────┘   └──────────────┘                │
│                                                                           │
│  Note: NO PHYSICAL HARDWARE REQUIRED                                     │
└───────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────── STORAGE LAYER ─────────────────────────────────┐
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────┐        │
│  │              SQLite Database (nms.db)                         │        │
│  │                                                                │        │
│  │  ┌────────────────────┐         ┌────────────────────┐       │        │
│  │  │  Metrics Table     │         │  Alarms Table      │       │        │
│  │  │                    │         │                    │       │        │
│  │  │ • device_id        │         │ • alarm_id (PK)    │       │        │
│  │  │ • parameter        │         │ • device_id        │       │        │
│  │  │ • value            │         │ • severity         │       │        │
│  │  │ • unit             │         │ • state            │       │        │
│  │  │ • timestamp        │         │ • first_seen       │       │        │
│  │  │ • protocol         │         │ • last_seen        │       │        │
│  │  │ • location         │         │ • occurrence_count │       │        │
│  │  │                    │         │ • resolved_at      │       │        │
│  │  │ Time-series data   │         │ • closed_at        │       │        │
│  │  └────────────────────┘         └────────────────────┘       │        │
│  │                                                                │        │
│  │  Indexes: device_id, timestamp, parameter, state              │        │
│  └──────────────────────────────────────────────────────────────┘        │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘


## Data Flow Diagram

┌─────────┐
│ Device  │  (SNMP/RESTCONF/MQTT)
└────┬────┘
     │ Raw protocol data
     ▼
┌─────────────┐
│  Collector  │  Protocol-specific polling/subscribing
└─────┬───────┘
      │ Raw metrics: {device_id, parameter, value, ...}
      ▼
┌──────────────┐
│  Normalizer  │  Standardization + Enrichment
└──────┬───────┘
       │
       ├──► Normalized Metric ──► Storage (metrics table)
       │                            ↓
       │                       (Historical data)
       │
       └──► Event (if threshold) ──► Alarm Engine
                                      ↓
                              (State management)
                                      ↓
                              Storage (alarms table)
                                      ↓
                                  Dashboard
                                      ↓
                                  Operator


## Unified Data Schema

### Metric Schema
```json
{
  "device_id": "snmp_device_001",
  "device_type": "router",
  "protocol": "SNMP",
  "location": "DataCenter-A",
  "parameter": "cpu_usage",
  "value": 75.5,
  "unit": "percent",
  "timestamp": "2025-11-06T10:30:00Z"
}
```

### Event/Alarm Schema
```json
{
  "device_id": "mqtt_sensor_001",
  "device_type": "temperature_sensor",
  "protocol": "MQTT",
  "location": "Floor-1",
  "type": "threshold_exceeded",
  "category": "temp_celsius",
  "severity": "CRITICAL",
  "state": "OPEN",
  "message": "temp_celsius exceeded critical threshold: 45.2 celsius >= 40",
  "timestamp": "2025-11-06T10:30:00Z"
}
```


## Alarm State Machine

```
        ┌──────────────────────────────────────┐
        │                                      │
        │         NEW THRESHOLD VIOLATION      │
        │                                      │
        └────────────────┬─────────────────────┘
                         │
                         ▼
                    ┌────────┐
                    │  OPEN  │  ◄─── New alarm created
                    └───┬────┘
                        │
          ┌─────────────┼─────────────┐
          │                           │
          │ Operator ACK              │ Auto-resolve
          │                           │ (value normalizes)
          ▼                           │
     ┌────────┐                       │
     │  ACK   │  ◄─── Acknowledged    │
     └───┬────┘                       │
         │                            │
         │ Operator/Auto Resolve      │
         │                            │
         └────────────┬───────────────┘
                      │
                      ▼
                 ┌──────────┐
                 │ RESOLVED │  ◄─── Issue cleared
                 └────┬─────┘
                      │
                      │ Auto-close after 5 min
                      │ OR Operator close
                      │
                      ▼
                 ┌─────────┐
                 │ CLOSED  │  ◄─── Final state
                 └─────────┘
```

## Component Interactions

```
Main.py (Orchestrator)
  │
  ├─► SNMPCollector (Thread 1)
  │     └─► process_metrics() callback
  │
  ├─► RESTCONFCollector (Thread 2)
  │     └─► process_metrics() callback
  │
  ├─► MQTTCollector (Thread 3)
  │     └─► process_metrics() callback
  │
  ├─► AlarmEngine Maintenance (Thread 4)
  │     └─► auto_resolve() + auto_close()
  │
  └─► Dashboard (Thread 5)
        └─► Flask web server

process_metrics():
  1. Normalizer.normalize_and_enrich()
  2. Storage.store_metrics()
  3. AlarmEngine.process_event()
  4. Storage.store_alarm()
```

## Technology Stack

```
┌─────────────────────────────────────┐
│         Frontend Layer              │
│  • HTML5 + CSS3                     │
│  • Vanilla JavaScript               │
│  • Fetch API (AJAX)                 │
│  • Auto-refresh (5s)                │
└─────────────────────────────────────┘
              │
┌─────────────────────────────────────┐
│          Backend Layer              │
│  • Flask (Web Framework)            │
│  • Flask-CORS                       │
│  • Threading (Concurrent collectors)│
└─────────────────────────────────────┘
              │
┌─────────────────────────────────────┐
│      Protocol Libraries             │
│  • PySNMP (SNMP v1/v2c/v3)         │
│  • Requests (HTTP/REST)             │
│  • Paho-MQTT (MQTT v3.1.1)         │
└─────────────────────────────────────┘
              │
┌─────────────────────────────────────┐
│       Database Layer                │
│  • SQLite3 (Embedded DB)            │
│  • Time-series storage              │
│  • Indexed queries                  │
└─────────────────────────────────────┘
```

## Deployment Architecture (Current)

```
┌──────────────────────────────────────────────┐
│         Single Host (Localhost)              │
│                                              │
│  ┌────────────────────────────────────┐     │
│  │  RESTCONF Simulator                │     │
│  │  Port: 8080                        │     │
│  └────────────────────────────────────┘     │
│                                              │
│  ┌────────────────────────────────────┐     │
│  │  Mosquitto MQTT Broker             │     │
│  │  Port: 1883                        │     │
│  └────────────────────────────────────┘     │
│                                              │
│  ┌────────────────────────────────────┐     │
│  │  MQTT Simulator                    │     │
│  │  Publishes to localhost:1883       │     │
│  └────────────────────────────────────┘     │
│                                              │
│  ┌────────────────────────────────────┐     │
│  │  NMS Main System                   │     │
│  │  • Collectors (threads)            │     │
│  │  • Normalizer                      │     │
│  │  • Alarm Engine                    │     │
│  │  • Dashboard (Port 5000)           │     │
│  │  • Database (nms.db)               │     │
│  └────────────────────────────────────┘     │
│                                              │
└──────────────────────────────────────────────┘
         ▲
         │ HTTP
         │
    ┌─────────┐
    │ Browser │  http://localhost:5000
    └─────────┘
```

## Scalable Production Architecture (Future)

```
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer                        │
└──────────────┬──────────────────────────────────────────┘
               │
      ┌────────┴────────┐
      │                 │
┌──────▼──────┐   ┌────▼──────┐
│Dashboard 1  │   │Dashboard 2│  (Horizontal scaling)
└──────┬──────┘   └────┬──────┘
       │               │
       └───────┬───────┘
               │
┌──────────────▼──────────────────┐
│    Message Queue (RabbitMQ)     │
└──────────────┬──────────────────┘
               │
      ┌────────┴────────┐
      │                 │
┌─────▼──────┐   ┌─────▼──────┐
│Collector 1 │   │Collector 2 │  (Distributed collectors)
└────────────┘   └────────────┘
      │                 │
      └────────┬────────┘
               │
┌──────────────▼──────────────────┐
│  Time-Series DB (InfluxDB)      │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│  Alarm DB (PostgreSQL)          │
└─────────────────────────────────┘
```

---

This architecture demonstrates a complete, production-ready NMS design
that can monitor heterogeneous IoT devices with unified data models,
lifecycle management, and real-time visualization.
