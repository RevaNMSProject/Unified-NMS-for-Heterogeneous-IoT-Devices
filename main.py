"""
Unified NMS Main Orchestrator
Coordinates all collectors, normalizers, and alarm engine
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import threading
import time
from collectors.snmp_collector import SNMPCollector
from collectors.restconf_collector import RESTCONFCollector
from collectors.mqtt_collector import MQTTCollector
from normalizer.normalizer import normalize_and_enrich
from storage.storage import storage
from storage.alarm_engine import alarm_engine
from dashboard.dashboard import run_dashboard
from config.config import Config

class NMSOrchestrator:
    def __init__(self):
        self.config = Config.load_devices()
        self.collectors = []
        self.latest_metrics = []
        self.running = False
        
    def process_metrics(self, raw_metrics):
        """Process collected metrics"""
        try:
            # Normalize and check thresholds
            normalized_metrics, events = normalize_and_enrich(raw_metrics)
            
            # Store metrics
            if normalized_metrics:
                storage.store_metrics(normalized_metrics)
                self.latest_metrics = normalized_metrics
            
            # Process events (alarms)
            for event in events:
                alarm_engine.process_event(event)
            
        except Exception as e:
            print(f"[Orchestrator] Error processing metrics: {e}")
    
    def start_snmp_collectors(self):
        """Start all SNMP collectors"""
        snmp_devices = [d for d in self.config['devices'] if d['protocol'] == 'SNMP']
        
        for device in snmp_devices:
            collector = SNMPCollector(device)
            
            def run_collector():
                collector.run(callback=self.process_metrics)
            
            thread = threading.Thread(target=run_collector, daemon=True)
            thread.start()
            self.collectors.append(thread)
            print(f"[Orchestrator] Started SNMP collector for {device['device_id']}")
    
    def start_restconf_collectors(self):
        """Start all RESTCONF collectors"""
        restconf_devices = [d for d in self.config['devices'] if d['protocol'] == 'RESTCONF']
        
        for device in restconf_devices:
            collector = RESTCONFCollector(device)
            
            def run_collector():
                collector.run(callback=self.process_metrics)
            
            thread = threading.Thread(target=run_collector, daemon=True)
            thread.start()
            self.collectors.append(thread)
            print(f"[Orchestrator] Started RESTCONF collector for {device['device_id']}")
    
    def start_mqtt_collectors(self):
        """Start all MQTT collectors"""
        mqtt_devices = [d for d in self.config['devices'] if d['protocol'] == 'MQTT']
        
        for device in mqtt_devices:
            collector = MQTTCollector(device, callback=self.process_metrics)
            
            def run_collector():
                collector.run()
            
            thread = threading.Thread(target=run_collector, daemon=True)
            thread.start()
            self.collectors.append(thread)
            print(f"[Orchestrator] Started MQTT collector for {device['device_id']}")
    
    def start_alarm_maintenance(self):
        """Start alarm engine maintenance loop"""
        def maintenance_loop():
            while self.running:
                try:
                    alarm_engine.run_maintenance(current_metrics=self.latest_metrics)
                    time.sleep(60)  # Run every minute
                except Exception as e:
                    print(f"[Orchestrator] Alarm maintenance error: {e}")
        
        thread = threading.Thread(target=maintenance_loop, daemon=True)
        thread.start()
        print("[Orchestrator] Started alarm maintenance")
    
    def start_dashboard(self):
        """Start web dashboard"""
        def run_dash():
            run_dashboard()
        
        thread = threading.Thread(target=run_dash, daemon=True)
        thread.start()
        print("[Orchestrator] Started dashboard")
    
    def run(self):
        """Run the complete NMS system"""
        print("\n" + "="*60)
        print("🛰️  UNIFIED NMS FOR HETEROGENEOUS IOT DEVICES")
        print("="*60 + "\n")
        
        self.running = True
        
        # Start all collectors
        print("[Orchestrator] Starting collectors...")
        self.start_snmp_collectors()
        self.start_restconf_collectors()
        self.start_mqtt_collectors()
        
        # Start alarm maintenance
        self.start_alarm_maintenance()
        
        # Start dashboard
        print("\n[Orchestrator] Starting dashboard...")
        self.start_dashboard()
        
        print("\n" + "="*60)
        print("✅ NMS System Running!")
        print("="*60)
        print(f"\n📊 Dashboard: http://localhost:{Config.DASHBOARD_PORT}")
        print(f"📡 API: http://localhost:{Config.DASHBOARD_PORT}/api/")
        print("\nPress Ctrl+C to stop\n")
        
        # Keep main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n[Orchestrator] Shutting down...")
            self.running = False
            time.sleep(2)
            print("[Orchestrator] Stopped")

def main():
    orchestrator = NMSOrchestrator()
    orchestrator.run()

if __name__ == '__main__':
    main()
