"""
Configuration Manager for Unified NMS
"""
import json
import os

class Config:
    # Base directories
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CONFIG_DIR = os.path.join(BASE_DIR, 'config')
    STORAGE_DIR = os.path.join(BASE_DIR, 'storage')
    
    # Collector settings
    SNMP_POLL_INTERVAL = 10  # seconds
    RESTCONF_POLL_INTERVAL = 10  # seconds (reduced from 15 for more frequent checks)
    MQTT_QOS = 1
    
    # Alarm settings
    ALARM_AUTO_CLOSE_TIMEOUT = 300  # 5 minutes
    ALARM_DEDUP_WINDOW = 60  # 1 minute
    
    # Database
    DB_PATH = os.path.join(STORAGE_DIR, 'nms.db')
    
    # Dashboard
    DASHBOARD_PORT = 5000
    DASHBOARD_HOST = '0.0.0.0'
    
    @staticmethod
    def load_devices():
        """Load device configuration"""
        path = os.path.join(Config.CONFIG_DIR, 'devices.json')
        with open(path, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def load_schemas():
        """Load data schemas"""
        path = os.path.join(Config.CONFIG_DIR, 'schemas.json')
        with open(path, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def get_thresholds():
        """Get alarm thresholds"""
        devices = Config.load_devices()
        return devices.get('thresholds', {})
