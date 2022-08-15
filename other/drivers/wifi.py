from ipaddress import ip_address
import wifi
from socketpool import SocketPool
from ssl import create_default_context
from adafruit_requests import Session
from gc import collect


class driver_wifi:
    """
    Ljinux network driver for the built in wifi module
    import it as: from drivers.driver_wifi import driver_wifi
    """

    def __init__(self):
        # internal use only
        self._pool = None
        self._session = None
        self._tz = None
        self._ntp = None

        # public
        self.error = False
        self.connected = False
        self.hw_name = "wifi"
        self.mode = "station"

    def connect(self, ssid, passwd):
        """
        Connect to a wifi access point
        """
        try:
            wifi.radio.connect(ssid=ssid, password=passwd)
        except ConnectionError:
            return 1
        self._pool = SocketPool(wifi.radio)
        self._session = Session(self._pool, create_default_context())
        self.connected = True
        return 0

    def ping(self, host):
        """
        ICMP Ping
        """
        return wifi.radio.ping(self.resolve(host))

    def get(self, host):
        """
        HTTP Get
        """
        if self._session is not None:

            if not (host.startswith("http://") or host.startswith("https://")):
                host = "https://" + host

            return self._session.get(host)
        else:
            return None

    def resolve(self, host):
        """
        Resolve ip string, to something usable
        No domain resolves just yet
        """
        return ip_address(host)

    def scan(self):
        """
        scan and store all nearby networks
        """
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
        """
        A getter for all of the wifi data
        iwconfig will need this
        """
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
            data["channel"] = wifi.radio.ap_info.channel
            data["country"] = wifi.radio.ap_info.country
        except:
            pass

        return data

    def disconnect(self):
        """
        Disconnect from the wifi
        """
        wifi.radio.stop_station()
        del self._pool, self._session
        self._pool = None
        self._session = None
        self.connected = False

    def start(self):
        """
        Power on the wifi
        """
        wifi.radio.enabled = True

    def stop(self):
        """
        Stop all wifi transactions
        Disconnect
        Power it off
        """
        self.disconnect()
        wifi.radio.enabled = False

    def timeset(self, tz=3):
        """
        Fetch network time and set it into the current rtc object
        set timezone by passing a tz
        """
        from adafruit_ntp import NTP
        from rtc import RTC
        from time import struct_time

        self._tz = tz

        if self.connected:
            if self._ntp is None:
                self._ntp = NTP(self._pool, tz_offset=tz)
            else:
                pass
            RTC().datetime = self._ntp.datetime
        del NTP, RTC, struct_time
        collect()
        collect()

    def resetsock(self):
        del self._session
        collect()
        collect()
        self._session = Session(self._pool, create_default_context())
