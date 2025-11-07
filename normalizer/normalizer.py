"""
Data Normalizer
Converts raw protocol data into unified metric and event format
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from config.config import Config

class Normalizer:
    def __init__(self):
        self.thresholds = Config.get_thresholds()
        
    def normalize_metric(self, raw_metric):
        """Convert raw metric to unified format"""
        
        # Extract common fields
        normalized = {
            'device_id': raw_metric.get('device_id'),
            'device_type': raw_metric.get('device_type'),
            'protocol': raw_metric.get('protocol'),
            'location': raw_metric.get('location'),
            'parameter': self._normalize_parameter_name(raw_metric.get('parameter')),
            'value': self._normalize_value(raw_metric.get('parameter'), raw_metric.get('value')),
            'unit': self._get_unit(raw_metric.get('parameter')),
            'timestamp': raw_metric.get('timestamp', datetime.utcnow().isoformat() + 'Z')
        }
        
        return normalized
    
    def _normalize_parameter_name(self, param):
        """Standardize parameter names across protocols"""
        # Map protocol-specific names to standard names
        mappings = {
            # SNMP OID parameters
            'cpu_usage': 'cpu_usage',
            'memory_usage': 'memory_usage',
            'uptime': 'uptime',
            
            # RESTCONF parameters
            'system_cpu_usage': 'cpu_usage',
            'system_memory_used': 'memory_used',
            'system_temperature': 'temp_celsius',
            'system_uptime': 'uptime',
            
            # MQTT parameters
            'temp1': 'temp_celsius',
            'humidity1': 'humidity_percent',
            'pressure1': 'pressure_kpa',
        }
        
        return mappings.get(param, param)
    
    def _normalize_value(self, param, value):
        """Convert value to appropriate type and scale"""
        try:
            # Try to convert to number
            if isinstance(value, str):
                # Remove any non-numeric characters (except decimal point and minus)
                cleaned = ''.join(c for c in value if c.isdigit() or c in ['.', '-'])
                if cleaned:
                    value = float(cleaned) if '.' in cleaned else int(cleaned)
            
            return value
        except:
            return value
    
    def _get_unit(self, param):
        """Determine unit for parameter"""
        unit_mappings = {
            'cpu_usage': 'percent',
            'memory_usage': 'MB',
            'memory_used': 'MB',
            'temp_celsius': 'celsius',
            'humidity_percent': 'percent',
            'pressure_kpa': 'kPa',
            'uptime': 'seconds',
            'tx_packets': 'count',
            'rx_packets': 'count',
        }
        
        return unit_mappings.get(param, '')
    
    def check_thresholds(self, metric):
        """Check if metric exceeds thresholds and generate events"""
        events = []
        
        param = metric['parameter']
        value = metric['value']
        
        # Check if we have thresholds for this parameter
        if param not in self.thresholds:
            return events
        
        threshold_config = self.thresholds[param]
        
        try:
            value_num = float(value)
            
            # Check critical threshold
            if 'critical' in threshold_config and value_num >= threshold_config['critical']:
                event = self._create_event(
                    metric,
                    'threshold_exceeded',
                    'CRITICAL',
                    f"{param} exceeded critical threshold: {value} {metric['unit']} >= {threshold_config['critical']}"
                )
                events.append(event)
            
            # Check warning threshold
            elif 'warning' in threshold_config and value_num >= threshold_config['warning']:
                event = self._create_event(
                    metric,
                    'threshold_exceeded',
                    'WARNING',
                    f"{param} exceeded warning threshold: {value} {metric['unit']} >= {threshold_config['warning']}"
                )
                events.append(event)
            
        except (ValueError, TypeError):
            pass  # Value not numeric, skip threshold check
        
        return events
    
    def _create_event(self, metric, event_type, severity, message):
        """Create event from metric"""
        return {
            'device_id': metric['device_id'],
            'device_type': metric.get('device_type', 'unknown'),
            'protocol': metric.get('protocol', 'unknown'),
            'location': metric.get('location', 'unknown'),
            'type': event_type,
            'category': metric['parameter'],
            'severity': severity,
            'state': 'OPEN',
            'message': message,
            'timestamp': metric['timestamp']
        }
    
    def process(self, raw_metrics):
        """Process raw metrics - normalize and check thresholds"""
        normalized_metrics = []
        events = []
        
        for raw_metric in raw_metrics:
            # Normalize metric
            normalized = self.normalize_metric(raw_metric)
            normalized_metrics.append(normalized)
            
            # Check for threshold violations
            threshold_events = self.check_thresholds(normalized)
            events.extend(threshold_events)
        
        return normalized_metrics, events

# Global normalizer instance
normalizer = Normalizer()

def normalize_and_enrich(raw_metrics):
    """Convenience function for normalizing metrics"""
    return normalizer.process(raw_metrics)
