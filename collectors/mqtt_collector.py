"""
MQTT Data Collector
Subscribes to MQTT topics and collects sensor data
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import paho.mqtt.client as mqtt
import json
from datetime import datetime
from config.config import Config

class MQTTCollector:
    def __init__(self, device_config, callback=None):
        self.device_id = device_config['device_id']
        self.device_type = device_config['device_type']
        self.protocol = device_config['protocol']
        self.location = device_config['location']
        self.broker = device_config['broker']
        self.port = device_config['port']
        self.topics = device_config['topics']
        self.callback = callback
        
        self.client = mqtt.Client(client_id=f"collector_{self.device_id}")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
    def on_connect(self, client, userdata, flags, rc):
        """Callback when connected to broker"""
        if rc == 0:
            print(f"[MQTT Collector] Connected to {self.broker}:{self.port}")
            # Subscribe to all configured topics
            for topic in self.topics:
                client.subscribe(topic, qos=Config.MQTT_QOS)
                print(f"[MQTT Collector] Subscribed to {topic}")
        else:
            print(f"[MQTT Collector] Connection failed with code {rc}")
    
    def on_message(self, client, userdata, msg):
        """Callback when message received"""
        try:
            # Parse MQTT payload
            payload = json.loads(msg.payload.decode())
            
            # Extract sensor data
            timestamp = datetime.utcnow().isoformat() + 'Z'
            
            # Determine parameter name from topic and payload
            topic_parts = msg.topic.split('/')
            param_base = topic_parts[-1] if len(topic_parts) > 0 else 'unknown'
            
            # Create metric
            metric = {
                'device_id': self.device_id,
                'device_type': self.device_type,
                'protocol': self.protocol,
                'location': self.location,
                'parameter': param_base,
                'value': payload.get('value'),
                'unit': payload.get('unit', ''),
                'topic': msg.topic,
                'timestamp': payload.get('timestamp', timestamp)
            }
            
            print(f"[MQTT Collector] {self.device_id} - {param_base}: {payload.get('value')} {payload.get('unit', '')}")
            
            # Call callback with metric
            if self.callback:
                self.callback([metric])
                
        except json.JSONDecodeError:
            print(f"[MQTT Collector] Invalid JSON from {msg.topic}: {msg.payload}")
        except Exception as e:
            print(f"[MQTT Collector] Error processing message: {e}")
    
    def run(self):
        """Start MQTT collector"""
        print(f"[MQTT Collector] Starting for {self.device_id}")
        
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_forever()
        except KeyboardInterrupt:
            print(f"\n[MQTT Collector] Stopped {self.device_id}")
            self.client.disconnect()
        except Exception as e:
            print(f"[MQTT Collector] Error: {e}")

def main():
    """Test MQTT collector"""
    config = Config.load_devices()
    mqtt_devices = [d for d in config['devices'] if d['protocol'] == 'MQTT']
    
    if not mqtt_devices:
        print("[MQTT Collector] No MQTT devices configured")
        return
    
    def print_metrics(metrics):
        print(f"Received {len(metrics)} metrics")
    
    # Collect from first MQTT device
    collector = MQTTCollector(mqtt_devices[0], callback=print_metrics)
    collector.run()

if __name__ == '__main__':
    main()
