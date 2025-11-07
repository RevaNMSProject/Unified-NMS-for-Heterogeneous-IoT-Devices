"""
RESTCONF Data Collector
Polls RESTCONF-enabled devices via REST API
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import time
import json
from datetime import datetime
from config.config import Config

class RESTCONFCollector:
    def __init__(self, device_config):
        self.device_id = device_config['device_id']
        self.device_type = device_config['device_type']
        self.protocol = device_config['protocol']
        self.location = device_config['location']
        self.base_url = device_config['base_url']
        self.username = device_config.get('username')
        self.password = device_config.get('password')
        self.endpoints = device_config['endpoints']
        self.poll_interval = Config.RESTCONF_POLL_INTERVAL
        
    def get_data(self, endpoint):
        """Get data from RESTCONF endpoint"""
        try:
            url = f"{self.base_url}{endpoint}"
            auth = None
            if self.username and self.password:
                auth = (self.username, self.password)
            
            response = requests.get(
                url,
                auth=auth,
                headers={'Accept': 'application/json'},
                timeout=5
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"[RESTCONF Collector] HTTP {response.status_code} from {url}")
                return None
                
        except Exception as e:
            print(f"[RESTCONF Collector] Error: {e}")
            return None
    
    def collect(self):
        """Collect all endpoint data and return raw metrics"""
        metrics = []
        timestamp = datetime.utcnow().isoformat() + 'Z'
        
        # Collect system data
        if 'system' in self.endpoints:
            system_data = self.get_data(self.endpoints['system'])
            if system_data:
                for param, value in system_data.items():
                    if isinstance(value, (int, float, str)):
                        metric = {
                            'device_id': self.device_id,
                            'device_type': self.device_type,
                            'protocol': self.protocol,
                            'location': self.location,
                            'parameter': f'system_{param}',
                            'value': value,
                            'endpoint': self.endpoints['system'],
                            'timestamp': timestamp
                        }
                        metrics.append(metric)
                        print(f"[RESTCONF Collector] {self.device_id} - system_{param}: {value}")
        
        # Collect interface data
        if 'interfaces' in self.endpoints:
            iface_data = self.get_data(self.endpoints['interfaces'])
            if iface_data and 'interface' in iface_data:
                for iface in iface_data['interface']:
                    iface_name = iface.get('name', 'unknown')
                    
                    # Create metrics for important interface parameters
                    for param in ['status', 'admin_status', 'tx_packets', 'rx_packets']:
                        if param in iface:
                            metric = {
                                'device_id': self.device_id,
                                'device_type': self.device_type,
                                'protocol': self.protocol,
                                'location': self.location,
                                'parameter': f'interface_{iface_name}_{param}',
                                'value': iface[param],
                                'endpoint': self.endpoints['interfaces'],
                                'timestamp': timestamp
                            }
                            metrics.append(metric)
                    
                    print(f"[RESTCONF Collector] {self.device_id} - {iface_name}: {iface.get('status')}")
        
        return metrics
    
    def run(self, callback=None):
        """Continuously poll device"""
        print(f"[RESTCONF Collector] Starting for {self.device_id} (interval: {self.poll_interval}s)")
        
        while True:
            try:
                metrics = self.collect()
                if callback and metrics:
                    callback(metrics)
                time.sleep(self.poll_interval)
            except KeyboardInterrupt:
                print(f"\n[RESTCONF Collector] Stopped {self.device_id}")
                break
            except Exception as e:
                print(f"[RESTCONF Collector] Error in {self.device_id}: {e}")
                time.sleep(self.poll_interval)

def main():
    """Test RESTCONF collector"""
    config = Config.load_devices()
    restconf_devices = [d for d in config['devices'] if d['protocol'] == 'RESTCONF']
    
    if not restconf_devices:
        print("[RESTCONF Collector] No RESTCONF devices configured")
        return
    
    # Collect from first RESTCONF device
    collector = RESTCONFCollector(restconf_devices[0])
    
    def print_metrics(metrics):
        print(f"Collected {len(metrics)} metrics")
    
    collector.run(callback=print_metrics)

if __name__ == '__main__':
    main()
