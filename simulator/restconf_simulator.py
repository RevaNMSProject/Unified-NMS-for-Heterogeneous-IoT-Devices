"""
RESTCONF Device Simulator
Mock REST API server simulating RESTCONF-enabled network devices
"""
from flask import Flask, jsonify, request
import random
import time
from datetime import datetime

app = Flask(__name__)

# Simulated device state
device_state = {
    'interfaces': {
        'interface': [
            {
                'name': 'GigabitEthernet0/0',
                'status': 'up',
                'admin_status': 'up',
                'speed': '1000Mbps',
                'mtu': 1500,
                'mac_address': '00:1A:2B:3C:4D:5E',
                'ip_address': '192.168.1.1',
                'tx_packets': 0,
                'rx_packets': 0
            },
            {
                'name': 'GigabitEthernet0/1',
                'status': 'up',
                'admin_status': 'up',
                'speed': '1000Mbps',
                'mtu': 1500,
                'mac_address': '00:1A:2B:3C:4D:5F',
                'ip_address': '192.168.2.1',
                'tx_packets': 0,
                'rx_packets': 0
            },
            {
                'name': 'GigabitEthernet0/2',
                'status': 'down',
                'admin_status': 'down',
                'speed': '1000Mbps',
                'mtu': 1500,
                'mac_address': '00:1A:2B:3C:4D:60',
                'ip_address': None,
                'tx_packets': 0,
                'rx_packets': 0
            }
        ]
    },
    'system': {
        'hostname': 'nms-switch-001',
        'version': '16.9.5',
        'uptime': 0,
        'cpu_usage': 0,
        'memory_total': 4096,
        'memory_used': 0,
        'temperature': 0
    }
}

start_time = time.time()

def update_dynamic_values():
    """Update dynamic values like counters and metrics"""
    uptime = int(time.time() - start_time)
    device_state['system']['uptime'] = uptime
    device_state['system']['cpu_usage'] = random.randint(15, 85)
    device_state['system']['memory_used'] = random.randint(1024, 3072)
    device_state['system']['temperature'] = random.randint(35, 65)
    
    # Update interface counters
    for iface in device_state['interfaces']['interface']:
        if iface['status'] == 'up':
            iface['tx_packets'] += random.randint(100, 1000)
            iface['rx_packets'] += random.randint(100, 1000)
            # Randomly change interface status
            if random.random() < 0.05:  # 5% chance
                iface['status'] = 'down' if iface['status'] == 'up' else 'up'

@app.route('/restconf/data/interfaces', methods=['GET'])
def get_interfaces():
    """Get all interface data"""
    update_dynamic_values()
    return jsonify(device_state['interfaces'])

@app.route('/restconf/data/interfaces/<interface_name>', methods=['GET'])
def get_interface(interface_name):
    """Get specific interface data"""
    update_dynamic_values()
    for iface in device_state['interfaces']['interface']:
        if iface['name'] == interface_name:
            return jsonify({'interface': iface})
    return jsonify({'error': 'Interface not found'}), 404

@app.route('/restconf/data/system', methods=['GET'])
def get_system():
    """Get system information"""
    update_dynamic_values()
    return jsonify(device_state['system'])

@app.route('/restconf/data/system/<parameter>', methods=['GET'])
def get_system_parameter(parameter):
    """Get specific system parameter"""
    update_dynamic_values()
    if parameter in device_state['system']:
        return jsonify({parameter: device_state['system'][parameter]})
    return jsonify({'error': 'Parameter not found'}), 404

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'uptime': int(time.time() - start_time)
    })

if __name__ == '__main__':
    print("[RESTCONF Simulator] Starting on http://127.0.0.1:8080")
    print("[RESTCONF Simulator] Available endpoints:")
    print("  - GET /restconf/data/interfaces")
    print("  - GET /restconf/data/system")
    print("  - GET /health")
    app.run(host='127.0.0.1', port=8080, debug=False)
