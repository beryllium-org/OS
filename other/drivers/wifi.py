from ipaddress import ip_address
import wifi
from socketpool import SocketPool
from ssl import create_default_context
from adafruit_requests import Session
from gc import collect


class driver_wifi:
    """
    Ljinux network driver for the built in wifi module
    Usage: modprobe driver_wifi as network
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
        self.interface_type = "wifi"
        self.mode = "station"

    def connect(self, ssid, passwd=None, retries=3):
        """
        Connect to a wifi access point
        """

        if retries < 1:
            retries = 1
        fails = 0
        while fails is not retries:
            self.disconnect()

            try:
                if passwd is not None:
                    wifi.radio.connect(ssid=ssid, password=passwd)
                else:
                    wifi.radio.connect(ssid=ssid)
                break
            except ConnectionError:
                fails += 1
        if fails is retries:
            self.disconnect()
            return 1
        del fails, ssid, passwd
        self._pool = SocketPool(wifi.radio)
        self._session = Session(self._pool, create_default_context())
        self.connected = True
        return 0

    def hostname(self, name=None):
        if name is not None:
            wifi.radio.hostname = name
        return wifi.radio.hostname

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
        if host.startswith("https://"):
            host = host[8:]
        elif host.startswith("http://"):
            host = host[7:]
        try:
            return ip_address(self._pool.getaddrinfo(host, 0)[0][4][0])
        except OSError:
            raise ConnectionError

    def scan(self):
        """
        scan and store all nearby networks
        """
        if wifi.radio.enabled:
            net = dict()
            for network in wifi.radio.start_scanning_networks():
                sec = None
                if len(network.authmode) is 3:
                    sec = str(network.authmode[0])
                    sec = sec[sec.rfind(".") + 1 :]
                else:
                    sec = "Unknown"
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

    def reset(self):
        self.disconnect()

    def disconnect(self):
        """
        Disconnect from the wifi
        """
        wifi.radio.stop_station()
        wifi.radio.stop_scanning_networks()
        try:
            wifi.radio.enabled = False
        except:
            pass

        from time import sleep

        sleep(0.5)
        del sleep
        collect()

        try:
            wifi.radio.enabled = True
        except:
            pass

        del self._pool, self._session
        self._pool = None
        self._session = None
        self.connected = False

    def start(self):
        """
        Power on the wifi
        """
        try:
            wifi.radio.enabled = True
        except:
            pass
        self.disconnect()

    def stop(self):
        """
        Stop all wifi transactions
        Disconnect
        Power it off
        """
        self.disconnect()
        try:
            wifi.radio.enabled = False
        except:
            pass

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

    def enter(self, args=None):
        print("This driver holds no executable")
        return 0
