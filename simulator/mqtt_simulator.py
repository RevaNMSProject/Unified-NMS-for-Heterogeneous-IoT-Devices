"""
MQTT Device Simulator
Publishes simulated sensor data to MQTT broker
"""
import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

class MQTTSimulator:
    def __init__(self, broker='127.0.0.1', port=1883):
        self.broker = broker
        self.port = port
        self.client = mqtt.Client(client_id='mqtt_simulator')
        self.running = False
        
    def on_connect(self, client, userdata, flags, rc):
        """Callback on connection"""
        if rc == 0:
            print(f"[MQTT Simulator] Connected to broker {self.broker}:{self.port}")
        else:
            print(f"[MQTT Simulator] Connection failed with code {rc}")
    
    def on_publish(self, client, userdata, mid):
        """Callback on message published"""
        pass  # Silent success
    
    def connect(self):
        """Connect to MQTT broker"""
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            return True
        except Exception as e:
            print(f"[MQTT Simulator] Failed to connect: {e}")
            return False
    
    def publish_temperature(self):
        """Publish temperature sensor data"""
        # Simulate realistic temperature variations
        base_temp = 25
        variation = random.uniform(-5, 20)  # Can spike to 45°C
        temp = base_temp + variation
        
        payload = {
            'sensor_id': 'temp_001',
            'value': round(temp, 2),
            'unit': 'celsius',
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        self.client.publish('iot/temp1', json.dumps(payload), qos=1)
        
        # Occasionally generate critical values
        if temp > 40:
            print(f"[MQTT Simulator] 🔥 CRITICAL temperature published: {temp:.2f}°C")
    
    def publish_humidity(self):
        """Publish humidity sensor data"""
        # Simulate humidity variations
        base_humidity = 50
        variation = random.uniform(-10, 40)  # Can reach 90%
        humidity = base_humidity + variation
        
        payload = {
            'sensor_id': 'humid_001',
            'value': round(humidity, 2),
            'unit': 'percent',
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        self.client.publish('iot/humidity1', json.dumps(payload), qos=1)
        
        if humidity > 80:
            print(f"[MQTT Simulator] 💧 HIGH humidity published: {humidity:.2f}%")
    
    def publish_pressure(self):
        """Publish pressure sensor data"""
        # Simulate pressure variations
        base_pressure = 101.3  # kPa (standard atmospheric)
        variation = random.uniform(-5, 12)  # Can reach 113 kPa
        pressure = base_pressure + variation
        
        payload = {
            'sensor_id': 'press_001',
            'value': round(pressure, 2),
            'unit': 'kPa',
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        self.client.publish('iot/pressure1', json.dumps(payload), qos=1)
        
        if pressure > 105:
            print(f"[MQTT Simulator] ⚠️ HIGH pressure published: {pressure:.2f} kPa")
    
    def run(self):
        """Run the simulator - publish data periodically"""
        if not self.connect():
            print("[MQTT Simulator] Cannot start - connection failed")
            return
        
        print("[MQTT Simulator] Publishing to topics:")
        print("  - iot/temp1 (temperature)")
        print("  - iot/humidity1 (humidity)")
        print("  - iot/pressure1 (pressure)")
        print("[MQTT Simulator] Press Ctrl+C to stop\n")
        
        self.running = True
        
        try:
            while self.running:
                # Publish temperature every 5 seconds
                self.publish_temperature()
                time.sleep(2)
                
                # Publish humidity every 7 seconds
                self.publish_humidity()
                time.sleep(2)
                
                # Publish pressure every 6 seconds
                self.publish_pressure()
                time.sleep(3)
                
        except KeyboardInterrupt:
            print("\n[MQTT Simulator] Stopping...")
            self.stop()
    
    def stop(self):
        """Stop the simulator"""
        self.running = False
        self.client.loop_stop()
        self.client.disconnect()
        print("[MQTT Simulator] Stopped")

if __name__ == '__main__':
    simulator = MQTTSimulator()
    simulator.run()
