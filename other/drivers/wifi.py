from time import sleep
from ipaddress import ip_address
import wifi
from socketpool import SocketPool
from ssl import create_default_context
from adafruit_requests import Session


class driver_wifi:
    """
    Ljinux network driver for the built in wifi module
    """

    def __init__(self):
        # internal use only
        self._pool = None
        self._session = None
        
        # public
        self.error = False
        self.connected = False
        self.up = False
        self.internet = False

    def connect(self, ssid, passwd):
        try:
            wifi.radio.connect(ssid=ssid,password=passwd)
        except ConnectionError:
            return 1
        self._pool = SocketPool(wifi.radio)
        self._session = Session(self._pool, create_default_context())
        return 0

    def ping(self, host):
        return wifi.radio.ping(self.resolve(host))

    def get(self, host):
        return self._session.get(host)

    def resolve(self, host):
        return ip_address(host)

    def scan(self):
        netnames = []
        for network in wifi.radio.start_scanning_networks():
            netnames.append(network.ssid)
        wifi.radio.stop_scanning_networks()
        return netnames

    def get_ipconf(self):
        pass
    
    def disconnect(self):
        wifi.radio.stop_station()
