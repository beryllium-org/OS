import time
import ipaddress
import wifi
import socketpool
import ssl
import adafruit_requests

class ljinux_wifi:
    """
    Ljinux network driver for the built in wifi module
    """
    
    def __init__(self):
        self.interface = None
        self.started = False
        self.error = False
        self.connected = False
        self.up = False
    
    def start(self):
        pass
    
    def deinit(self):
        pass
    
    def int_connect(self, data=None):
        pass
    
    def ping(self, host):
        pass
    
    def get(self, host):
        pass
    
    def resolve(self, host):
        pass
    
    def reset(self):
        pass
    
    def scan(self):
        pass
    
