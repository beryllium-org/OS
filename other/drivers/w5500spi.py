from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket
from adafruit_requests import Session
from digitalio import DigitalInOut
from busio import SPI


class driver_w5500spi:
    """
    Ljinux network driver for the w5500 ethernet module (spi interface)
    Usage: modprobe w5500spi as network
    """

    def __init__(self):
        # internal use only
        self._interface = None
        self._pool = None
        self._session = None
        self._tz = None
        self._ntp = None
        self._spi = None
        self._cs = None

        # public
        self.error = False
        self.connected = False
        self.hw_name = "w5500"
        self.interface_type = "ethernet"
        self.mode = "None"

    def connect(self, mosi, miso, sclk, cs, ip=None, hostname="Ljinux"):
        self._cs = DigitalInOut(cs)
        self._spi = SPI(clock=sclk, MOSI=mosi, MISO=miso)

        try:
            self._interface = WIZNET5K(self._spi, self._cs, is_dhcp=False)
            self._interface.detect_w5500()
        except ConnectionError:
            return 1
        if self._interface.link_status:
            dhcp_status = self._interface.set_dhcp(
                hostname=hostname, response_timeout=10
            )
        else:
            return 1
        self.connected = True
        return 0

    def ping(self, host):
        """
        ICMP Ping
        """
        return None

    def get(self, host):
        return None

    def resolve(self, host):
        """
        Resolve ip string, to something usable
        No domain resolves just yet
        """
        return None

    def scan(self):
        return None

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
            "ip": None,
            "power": None,
            "gateway": None,
            "mode": self.mode,
            "dns": None,
            "subnet": None,
            "mac": None,
            "mac_pretty": None,
            "hostname": None,
        }

        try:
            data["ssid"] = None
            data["bssid"] = None
            data["channel"] = None
            data["country"] = None
        except:
            pass

        return data

    def disconnect(self):
        pass

    def start(self):
        pass

    def stop(self):
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

    def resetsock(self):
        pass

    def enter(self, args=None):
        print("This driver holds no executable")
        return 0
