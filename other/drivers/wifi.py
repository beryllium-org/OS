from time import sleep
from ipaddress import ip_address
import wifi
from socketpool import SocketPool
from ssl import create_default_context
from adafruit_requests import Session


class driver_wifi:
    """
    Ljinux network driver for the built in wifi module
    import it as: from drivers.driver_wifi import driver_wifi
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
            wifi.radio.connect(ssid=ssid, password=passwd)
        except ConnectionError:
            return 1
        self._pool = SocketPool(wifi.radio)
        self._session = Session(self._pool, create_default_context())
        return 0

    def ping(self, host):
        return wifi.radio.ping(self.resolve(host))

    def get(self, host):
        if self._session is not None:
            if not (host.startswith("http://") or host.startswith("https://")):
                host = f"https://{host}"
            return self._session.get(host)
        else:
            return none

    def resolve(self, host):
        return ip_address(host)

    def scan(self):
        netnames = []
        if wifi.radio.enabled:
            for network in wifi.radio.start_scanning_networks():
                netnames.append(network.ssid)
            wifi.radio.stop_scanning_networks()
        return netnames

    def get_ipconf(self):
        return {
            "ssid": wifi.radio.ap_info.ssid,
            "bssid": wifi.radio.ap_info.bssid,
            "channel": wifi.radio.ap_info.channel,
            "country": wifi.radio.ap_info.country,
            "ip": wifi.radio.ipv4_address,
            "gateway": wifi.radio.ipv4_gateway,
            "dns": wifi.radio.ipv4_dns,
            "subnet": wifi.radio.ipv4_subnet,
            "mac": wifi.radio.mac_address,
            "hostname": wifi.radio.hostname,
        }

    def disconnect(self):
        wifi.radio.stop_station()
        self._pool = None
        self._session = None
        
    def start(self):
        wifi.radio.enabled = True
    
    def stop(self):
        self.disconnect()
        wifi.radio.enabled = False
    
