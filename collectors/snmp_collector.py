"""
SNMP Data Collector
Polls SNMP devices and collects metrics
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pysnmp.hlapi import *
import time
import json
from datetime import datetime
from config.config import Config

class SNMPCollector:
    def __init__(self, device_config):
        self.device_id = device_config['device_id']
        self.device_type = device_config['device_type']
        self.protocol = device_config['protocol']
        self.location = device_config['location']
        self.ip = device_config['ip']
        self.port = device_config['port']
        self.community = device_config['community']
        self.oids = device_config['oids']
        self.poll_interval = Config.SNMP_POLL_INTERVAL
        
    def get_snmp_value(self, oid):
        """Get value for a specific OID"""
        try:
            iterator = getCmd(
                SnmpEngine(),
                CommunityData(self.community),
                UdpTransportTarget((self.ip, self.port), timeout=2, retries=1),
                ContextData(),
                ObjectType(ObjectIdentity(oid))
            )
            
            error_indication, error_status, error_index, var_binds = next(iterator)
            
            if error_indication:
                print(f"[SNMP Collector] Error: {error_indication}")
                return None
            elif error_status:
                print(f"[SNMP Collector] Error: {error_status.prettyPrint()}")
                return None
            else:
                for var_bind in var_binds:
                    return var_bind[1].prettyPrint()
        except Exception as e:
            print(f"[SNMP Collector] Exception: {e}")
            return None
    
    def collect(self):
        """Collect all OID values and return raw metrics"""
        metrics = []
        timestamp = datetime.utcnow().isoformat() + 'Z'
        
        for param_name, oid in self.oids.items():
            value = self.get_snmp_value(oid)
            
            if value is not None:
                metric = {
                    'device_id': self.device_id,
                    'device_type': self.device_type,
                    'protocol': self.protocol,
                    'location': self.location,
                    'parameter': param_name,
                    'value': value,
                    'oid': oid,
                    'timestamp': timestamp
                }
                metrics.append(metric)
                print(f"[SNMP Collector] {self.device_id} - {param_name}: {value}")
        
        return metrics
    
    def run(self, callback=None):
        """Continuously poll device"""
        print(f"[SNMP Collector] Starting for {self.device_id} (interval: {self.poll_interval}s)")
        
        while True:
            try:
                metrics = self.collect()
                if callback and metrics:
                    callback(metrics)
                time.sleep(self.poll_interval)
            except KeyboardInterrupt:
                print(f"\n[SNMP Collector] Stopped {self.device_id}")
                break
            except Exception as e:
                print(f"[SNMP Collector] Error in {self.device_id}: {e}")
                time.sleep(self.poll_interval)

def main():
    """Test SNMP collector"""
    config = Config.load_devices()
    snmp_devices = [d for d in config['devices'] if d['protocol'] == 'SNMP']
    
    if not snmp_devices:
        print("[SNMP Collector] No SNMP devices configured")
        return
    
    # Collect from first SNMP device
    collector = SNMPCollector(snmp_devices[0])
    
    def print_metrics(metrics):
        print(f"Collected {len(metrics)} metrics")
    
    collector.run(callback=print_metrics)

if __name__ == '__main__':
    main()
