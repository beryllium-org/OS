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
        self.hw_name = "wifi"
        self.mode = "station"

    def connect(self, ssid, passwd):
        try:
            wifi.radio.connect(ssid=ssid, password=passwd)
        except ConnectionError:
            return 1
        self._pool = SocketPool(wifi.radio)
        self._session = Session(self._pool, create_default_context())
        self.connected = True
        return 0

    def ping(self, host):
        return wifi.radio.ping(self.resolve(host))

    def get(self, host):
        if self._session is not None:

            if not (host.startswith("http://") or host.startswith("https://")):
                host = "https://" + host

            return self._session.get(host)
        else:
            return None

    def resolve(self, host):
        return ip_address(host)

    def scan(self):
        if wifi.radio.enabled:
            net = dict()
            for network in wifi.radio.start_scanning_networks():
                sec = str(network.authmode)
                sec = sec[sec.rfind(".") + 1 : -1]
                net.update({network.ssid: [sec, network.rssi]})
                del sec
            wifi.radio.stop_scanning_networks()
            return net

        return list()

    def get_ipconf(self):
        data = {
            "ssid": None,
            "bssid": None,
            "channel": None,
            "country": None,
            "ip": wifi.radio.ipv4_address,
            "power": str(wifi.radio.enabled),
            "gateway": wifi.radio.ipv4_gateway,
            "mode": self.mode,
            "dns": wifi.radio.ipv4_dns,
            "subnet": wifi.radio.ipv4_subnet,
            "mac": wifi.radio.mac_address,
            "mac_pretty": str(wifi.radio.mac_address).replace("\\x", ":")[3:-3],
            "hostname": wifi.radio.hostname,
        }

        try:
            data["ssid"] = wifi.radio.ap_info.ssid
            data["bssid"] = wifi.radio.ap_info.bssid
            data["channel"] = (wifi.radio.ap_info.channel,)
            data["country"] = (wifi.radio.ap_info.country,)
        except:
            pass

        return data

    def disconnect(self):
        wifi.radio.stop_station()
        self._pool = None
        self._session = None
        self.connected = False

    def start(self):
        wifi.radio.enabled = True

    def stop(self):
        self.disconnect()
        wifi.radio.enabled = False
