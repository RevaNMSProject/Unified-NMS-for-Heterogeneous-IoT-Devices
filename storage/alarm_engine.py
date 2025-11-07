"""
Alarm Lifecycle Engine
Manages alarm state transitions and auto-close logic
State machine: OPEN → ACK → RESOLVED → CLOSED
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from datetime import datetime, timedelta
from storage.storage import storage
from config.config import Config

class AlarmEngine:
    def __init__(self):
        self.auto_close_timeout = Config.ALARM_AUTO_CLOSE_TIMEOUT
        
    def process_event(self, event):
        """Process an event and update alarm state"""
        # Store the alarm (creates new or updates existing)
        storage.store_alarm(event)
    
    def acknowledge_alarm(self, alarm_id):
        """Acknowledge an alarm (operator action)"""
        storage.update_alarm_state(alarm_id, 'ACK')
        print(f"[Alarm Engine] Alarm {alarm_id} acknowledged")
    
    def resolve_alarm(self, alarm_id):
        """Resolve an alarm (recovery detected or operator action)"""
        storage.update_alarm_state(alarm_id, 'RESOLVED')
        print(f"[Alarm Engine] Alarm {alarm_id} resolved")
    
    def close_alarm(self, alarm_id):
        """Close an alarm (operator action)"""
        storage.update_alarm_state(alarm_id, 'CLOSED')
        print(f"[Alarm Engine] Alarm {alarm_id} closed")
    
    def auto_resolve_alarms(self, current_metrics):
        """Auto-resolve alarms when conditions return to normal"""
        # Get all OPEN and ACK alarms
        open_alarms = storage.get_alarms(state='OPEN', limit=1000)
        ack_alarms = storage.get_alarms(state='ACK', limit=1000)
        
        all_active = open_alarms + ack_alarms
        
        # Build current metric state
        metric_state = {}
        for metric in current_metrics:
            key = f"{metric['device_id']}_{metric['parameter']}"
            metric_state[key] = metric
        
        # Check each alarm against current state
        thresholds = Config.get_thresholds()
        
        for alarm in all_active:
            alarm_key = f"{alarm['device_id']}_{alarm['category']}"
            
            # Check if we have current metric for this alarm
            if alarm_key in metric_state:
                metric = metric_state[alarm_key]
                param = alarm['category']
                
                # Check if condition has cleared
                if param in thresholds:
                    threshold_config = thresholds[param]
                    
                    try:
                        value = float(metric['value'])
                        
                        # If value is now below warning threshold, resolve
                        if 'warning' in threshold_config:
                            if value < threshold_config['warning']:
                                self.resolve_alarm(alarm['alarm_id'])
                                print(f"[Alarm Engine] Auto-resolved {alarm['alarm_id']} - value returned to normal")
                    except (ValueError, TypeError):
                        pass
    
    def auto_close_resolved_alarms(self):
        """Auto-close alarms that have been RESOLVED for too long"""
        resolved_alarms = storage.get_alarms(state='RESOLVED', limit=1000)
        
        current_time = datetime.utcnow()
        
        for alarm in resolved_alarms:
            if alarm['resolved_at']:
                try:
                    resolved_time = datetime.fromisoformat(alarm['resolved_at'].replace('Z', '+00:00'))
                    
                    # Calculate time in RESOLVED state
                    time_resolved = (current_time - resolved_time.replace(tzinfo=None)).total_seconds()
                    
                    if time_resolved >= self.auto_close_timeout:
                        self.close_alarm(alarm['alarm_id'])
                        print(f"[Alarm Engine] Auto-closed {alarm['alarm_id']} after {time_resolved:.0f}s")
                except:
                    pass
    
    def get_alarm_statistics(self):
        """Get alarm statistics"""
        stats = {
            'open': len(storage.get_alarms(state='OPEN', limit=10000)),
            'acknowledged': len(storage.get_alarms(state='ACK', limit=10000)),
            'resolved': len(storage.get_alarms(state='RESOLVED', limit=10000)),
            'closed': len(storage.get_alarms(state='CLOSED', limit=10000)),
        }
        
        # Get severity breakdown for active alarms
        all_alarms = storage.get_alarms(limit=10000)
        active_alarms = [a for a in all_alarms if a['state'] != 'CLOSED']
        
        stats['by_severity'] = {
            'CRITICAL': len([a for a in active_alarms if a['severity'] == 'CRITICAL']),
            'WARNING': len([a for a in active_alarms if a['severity'] == 'WARNING']),
        }
        
        stats['total_active'] = len(active_alarms)
        
        return stats
    
    def run_maintenance(self, current_metrics=None):
        """Run periodic maintenance tasks"""
        # Auto-resolve alarms based on current metrics
        if current_metrics:
            self.auto_resolve_alarms(current_metrics)
        
        # Auto-close long-resolved alarms
        self.auto_close_resolved_alarms()

# Global alarm engine instance
alarm_engine = AlarmEngine()
