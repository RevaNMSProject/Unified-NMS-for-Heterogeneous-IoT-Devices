"""
Web Dashboard for Unified NMS
Provides REST API and web interface for monitoring and control
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from storage.storage import storage
from storage.alarm_engine import alarm_engine
from config.config import Config

app = Flask(__name__, static_folder='static')
CORS(app)

# API Routes

@app.route('/api/devices', methods=['GET'])
def get_devices():
    """Get all devices summary"""
    devices = storage.get_device_summary()
    return jsonify({
        'success': True,
        'count': len(devices),
        'devices': devices
    })

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get metrics with optional filters"""
    device_id = request.args.get('device_id')
    parameter = request.args.get('parameter')
    limit = int(request.args.get('limit', 100))
    
    metrics = storage.get_metrics(
        device_id=device_id,
        parameter=parameter,
        limit=limit
    )
    
    return jsonify({
        'success': True,
        'count': len(metrics),
        'metrics': metrics
    })

@app.route('/api/alarms', methods=['GET'])
def get_alarms():
    """Get alarms with optional filters"""
    state = request.args.get('state')
    severity = request.args.get('severity')
    limit = int(request.args.get('limit', 100))
    
    alarms = storage.get_alarms(
        state=state,
        severity=severity,
        limit=limit
    )
    
    return jsonify({
        'success': True,
        'count': len(alarms),
        'alarms': alarms
    })

@app.route('/api/alarms/stats', methods=['GET'])
def get_alarm_stats():
    """Get alarm statistics"""
    stats = alarm_engine.get_alarm_statistics()
    return jsonify({
        'success': True,
        'statistics': stats
    })

@app.route('/api/alarms/<alarm_id>/acknowledge', methods=['POST'])
def acknowledge_alarm(alarm_id):
    """Acknowledge an alarm"""
    try:
        alarm_engine.acknowledge_alarm(alarm_id)
        return jsonify({
            'success': True,
            'message': f'Alarm {alarm_id} acknowledged'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/alarms/<alarm_id>/resolve', methods=['POST'])
def resolve_alarm(alarm_id):
    """Resolve an alarm"""
    try:
        alarm_engine.resolve_alarm(alarm_id)
        return jsonify({
            'success': True,
            'message': f'Alarm {alarm_id} resolved'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/alarms/<alarm_id>/close', methods=['POST'])
def close_alarm(alarm_id):
    """Close an alarm"""
    try:
        alarm_engine.close_alarm(alarm_id)
        return jsonify({
            'success': True,
            'message': f'Alarm {alarm_id} closed'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'service': 'Unified NMS Dashboard'
    })

# Static file serving
@app.route('/')
def index():
    """Serve main dashboard page"""
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('static', path)

def run_dashboard(host=None, port=None):
    """Run the dashboard server"""
    host = host or Config.DASHBOARD_HOST
    port = port or Config.DASHBOARD_PORT
    
    print(f"[Dashboard] Starting on http://{host}:{port}")
    print(f"[Dashboard] API available at http://{host}:{port}/api/")
    
    app.run(host=host, port=port, debug=False)

if __name__ == '__main__':
    run_dashboard()
