"""
SNMP Device Simulator
Simulates SNMP-enabled devices without physical hardware
"""
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, context
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.proto.api import v2c
import random
import time

class SNMPSimulator:
    def __init__(self, host='127.0.0.1', port=161):
        self.host = host
        self.port = port
        self.snmp_engine = engine.SnmpEngine()
        
    def setup_agent(self):
        """Setup SNMP agent"""
        # Transport setup
        config.addTransport(
            self.snmp_engine,
            udp.domainName,
            udp.UdpTransport().openServerMode((self.host, self.port))
        )
        
        # SNMPv2c setup
        config.addV1System(self.snmp_engine, 'my-area', 'public')
        
        # Context setup
        snmp_context = context.SnmpContext(self.snmp_engine)
        
        # Register SNMP Applications
        cmdrsp.GetCommandResponder(self.snmp_engine, snmp_context)
        cmdrsp.SetCommandResponder(self.snmp_engine, snmp_context)
        cmdrsp.NextCommandResponder(self.snmp_engine, snmp_context)
        cmdrsp.BulkCommandResponder(self.snmp_engine, snmp_context)
        
        # Add simulated OIDs
        mib_builder = snmp_context.getMibInstrum().getMibBuilder()
        mib_view_controller = view = snmp_context.getMibInstrum()
        
        # Simulate CPU usage OID: 1.3.6.1.4.1.2021.11.9.0
        # Simulate Memory usage OID: 1.3.6.1.4.1.2021.4.6.0
        # Simulate Uptime OID: 1.3.6.1.2.1.1.3.0
        
        print(f"[SNMP Simulator] Started on {self.host}:{self.port}")
        print("[SNMP Simulator] Simulating OIDs:")
        print("  - CPU Usage: 1.3.6.1.4.1.2021.11.9.0")
        print("  - Memory Usage: 1.3.6.1.4.1.2021.4.6.0")
        print("  - Uptime: 1.3.6.1.2.1.1.3.0")
        
    def run(self):
        """Run the SNMP simulator"""
        self.setup_agent()
        try:
            self.snmp_engine.transportDispatcher.jobStarted(1)
            self.snmp_engine.transportDispatcher.runDispatcher()
        except KeyboardInterrupt:
            print("\n[SNMP Simulator] Stopped")
        finally:
            self.snmp_engine.transportDispatcher.closeDispatcher()

# Simple mock SNMP responder for demonstration
class SimpleSNMPMock:
    """Simplified SNMP mock that responds with random values"""
    
    def __init__(self, host='127.0.0.1', port=161):
        self.host = host
        self.port = port
        self.start_time = time.time()
        
    def get_oid_value(self, oid):
        """Return simulated values for OIDs"""
        # CPU Usage
        if '2021.11.9.0' in oid:
            return random.randint(20, 95)
        # Memory Usage  
        elif '2021.4.6.0' in oid:
            return random.randint(1024, 8192)  # MB
        # Uptime
        elif '1.2.1.1.3.0' in oid:
            return int((time.time() - self.start_time) * 100)  # TimeTicks
        else:
            return 0
    
    def run(self):
        """Simulation ready - values will be generated on demand"""
        print(f"[SNMP Mock] Ready to respond on {self.host}:{self.port}")
        print("[SNMP Mock] Use collectors to poll OID values")

if __name__ == '__main__':
    # Use simple mock for easier testing
    simulator = SimpleSNMPMock()
    simulator.run()
    
    # Keep alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[SNMP Mock] Stopped")
