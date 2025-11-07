"""
Storage Layer
Handles persistence of metrics and alarms to SQLite database
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlite3
import json
from datetime import datetime
from config.config import Config

class Storage:
    def __init__(self, db_path=None):
        self.db_path = db_path or Config.DB_PATH
        self._init_database()
    
    def _init_database(self):
        """Initialize database schema"""
        # Ensure storage directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Metrics table (time-series data)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                device_type TEXT,
                protocol TEXT,
                location TEXT,
                parameter TEXT NOT NULL,
                value TEXT,
                unit TEXT,
                timestamp TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create index for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_metrics_device_time 
            ON metrics(device_id, timestamp)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_metrics_parameter 
            ON metrics(parameter, timestamp)
        ''')
        
        # Alarms table (event lifecycle)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alarms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alarm_id TEXT UNIQUE NOT NULL,
                device_id TEXT NOT NULL,
                device_type TEXT,
                protocol TEXT,
                location TEXT,
                type TEXT NOT NULL,
                category TEXT,
                severity TEXT NOT NULL,
                state TEXT NOT NULL,
                message TEXT,
                first_seen TEXT NOT NULL,
                last_seen TEXT NOT NULL,
                acknowledged_at TEXT,
                resolved_at TEXT,
                closed_at TEXT,
                occurrence_count INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_alarms_state 
            ON alarms(state, severity)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_alarms_device 
            ON alarms(device_id, state)
        ''')
        
        conn.commit()
        conn.close()
        
        print(f"[Storage] Database initialized at {self.db_path}")
    
    def store_metrics(self, metrics):
        """Store metrics to database"""
        if not metrics:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for metric in metrics:
            cursor.execute('''
                INSERT INTO metrics (device_id, device_type, protocol, location, 
                                   parameter, value, unit, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                metric['device_id'],
                metric.get('device_type'),
                metric.get('protocol'),
                metric.get('location'),
                metric['parameter'],
                str(metric['value']),
                metric.get('unit'),
                metric['timestamp']
            ))
        
        conn.commit()
        conn.close()
        
        print(f"[Storage] Stored {len(metrics)} metrics")
    
    def get_metrics(self, device_id=None, parameter=None, limit=100):
        """Retrieve metrics from database"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = 'SELECT * FROM metrics WHERE 1=1'
        params = []
        
        if device_id:
            query += ' AND device_id = ?'
            params.append(device_id)
        
        if parameter:
            query += ' AND parameter = ?'
            params.append(parameter)
        
        query += ' ORDER BY timestamp DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        metrics = [dict(row) for row in rows]
        conn.close()
        
        return metrics
    
    def store_alarm(self, alarm):
        """Store or update alarm"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Generate alarm_id for deduplication
        alarm_id = f"{alarm['device_id']}_{alarm['category']}_{alarm['type']}"
        
        # Check if alarm already exists
        cursor.execute('SELECT * FROM alarms WHERE alarm_id = ? AND state != ?', 
                      (alarm_id, 'CLOSED'))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing alarm
            cursor.execute('''
                UPDATE alarms 
                SET last_seen = ?, 
                    occurrence_count = occurrence_count + 1,
                    severity = ?,
                    message = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE alarm_id = ? AND state != ?
            ''', (
                alarm['timestamp'],
                alarm['severity'],
                alarm['message'],
                alarm_id,
                'CLOSED'
            ))
            print(f"[Storage] Updated alarm {alarm_id} (occurrence +1)")
        else:
            # Create new alarm
            cursor.execute('''
                INSERT INTO alarms (alarm_id, device_id, device_type, protocol, 
                                  location, type, category, severity, state, 
                                  message, first_seen, last_seen)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                alarm_id,
                alarm['device_id'],
                alarm.get('device_type'),
                alarm.get('protocol'),
                alarm.get('location'),
                alarm['type'],
                alarm.get('category'),
                alarm['severity'],
                alarm['state'],
                alarm['message'],
                alarm['timestamp'],
                alarm['timestamp']
            ))
            print(f"[Storage] Created new alarm {alarm_id}")
        
        conn.commit()
        conn.close()
    
    def update_alarm_state(self, alarm_id, new_state):
        """Update alarm state"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp_field = None
        if new_state == 'ACK':
            timestamp_field = 'acknowledged_at'
        elif new_state == 'RESOLVED':
            timestamp_field = 'resolved_at'
        elif new_state == 'CLOSED':
            timestamp_field = 'closed_at'
        
        query = 'UPDATE alarms SET state = ?, updated_at = CURRENT_TIMESTAMP'
        params = [new_state]
        
        if timestamp_field:
            query += f', {timestamp_field} = ?'
            params.append(datetime.utcnow().isoformat() + 'Z')
        
        query += ' WHERE alarm_id = ?'
        params.append(alarm_id)
        
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        
        print(f"[Storage] Updated alarm {alarm_id} to state {new_state}")
    
    def get_alarms(self, state=None, severity=None, limit=100):
        """Retrieve alarms from database"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = 'SELECT * FROM alarms WHERE 1=1'
        params = []
        
        if state:
            query += ' AND state = ?'
            params.append(state)
        
        if severity:
            query += ' AND severity = ?'
            params.append(severity)
        
        query += ' ORDER BY first_seen DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        alarms = [dict(row) for row in rows]
        conn.close()
        
        return alarms
    
    def get_device_summary(self):
        """Get summary of all devices"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get latest metric timestamp per device
        cursor.execute('''
            SELECT device_id, device_type, protocol, location,
                   MAX(timestamp) as last_seen,
                   COUNT(*) as metric_count
            FROM metrics
            GROUP BY device_id
            ORDER BY device_id
        ''')
        
        devices = [dict(row) for row in cursor.fetchall()]
        
        # Add alarm counts
        for device in devices:
            cursor.execute('''
                SELECT state, COUNT(*) as count
                FROM alarms
                WHERE device_id = ? AND state != 'CLOSED'
                GROUP BY state
            ''', (device['device_id'],))
            
            alarm_counts = {row['state']: row['count'] for row in cursor.fetchall()}
            device['active_alarms'] = sum(alarm_counts.values())
            device['alarm_breakdown'] = alarm_counts
        
        conn.close()
        return devices

# Global storage instance
storage = Storage()
