# based off of https://github.com/afaonline/DS1302_CircuitPython

import time
import digitalio


class DS1302:
    clktim = 5e-6

    def __init__(self, clk_pin, data_pin, ce_pin):
        self._clk_pin = clk_pin
        self._data_pin = data_pin
        self._ce_pin = ce_pin
        self._clk_pin.direction = digitalio.Direction.OUTPUT
        self._ce_pin.direction = digitalio.Direction.OUTPUT

        # moar init stuff
        # no write protection
        self._start_tx()
        self._w_byte(0x8E)
        self._w_byte(0x00)
        self._end_tx()
        # disabling charge mode
        self._start_tx()
        self._w_byte(0x90)
        self._w_byte(0x00)
        self._end_tx()

    def _start_tx(self):
        # Setting pins for start of transmission
        self._clk_pin.value = False
        self._ce_pin.value = True

    def _end_tx(self):
        # Closing transmission
        self._data_pin.direction = digitalio.Direction.INPUT
        self._clk_pin.value = False
        self._ce_pin.value = False

    def _r_byte(self):
        # Read a byte
        self._data_pin.direction = digitalio.Direction.INPUT
        byte = 0
        for i in range(8):
            # High pulse on CLK pin
            self._clk_pin.value = True
            time.sleep(self.clktim)
            self._clk_pin.value = False
            time.sleep(self.clktim)
            bit = self._data_pin.value
            byte |= (2**i) * bit
        return byte

    def _w_byte(self, byte):
        self._data_pin.direction = digitalio.Direction.OUTPUT
        for _ in range(8):
            self._clk_pin.value = False
            time.sleep(self.clktim)
            self._data_pin.value = byte & 0x01
            byte >>= 1
            self._clk_pin.value = True
            time.sleep(self.clktim)

    def read_datetime(self):
        self._start_tx()
        self._w_byte(0xBF)
        byte_l = []
        for _ in range(7):
            byte_l.append(self._r_byte())
        self._end_tx()
        second = ((byte_l[0] & 0x70) >> 4) * 10 + (byte_l[0] & 0x0F)
        minute = ((byte_l[1] & 0x70) >> 4) * 10 + (byte_l[1] & 0x0F)
        hour = ((byte_l[2] & 0x30) >> 4) * 10 + (byte_l[2] & 0x0F)
        day = ((byte_l[3] & 0x30) >> 4) * 10 + (byte_l[3] & 0x0F)
        month = ((byte_l[4] & 0x10) >> 4) * 10 + (byte_l[4] & 0x0F)
        year = ((byte_l[6] & 0xF0) >> 4) * 10 + (byte_l[6] & 0x0F) + 2000
        return time.struct_time((year, month, day, hour, minute, second, 0, -1, -1))

    def write_datetime(self, dt):
        byte_l = [0] * 9
        byte_l[0] = (dt.tm_sec // 10) << 4 | dt.tm_sec % 10
        byte_l[1] = (dt.tm_min // 10) << 4 | dt.tm_min % 10
        byte_l[2] = (dt.tm_hour // 10) << 4 | dt.tm_hour % 10
        byte_l[3] = (dt.tm_mday // 10) << 4 | dt.tm_mday % 10
        byte_l[4] = (dt.tm_mon // 10) << 4 | dt.tm_mon % 10
        byte_l[5] = 0
        byte_l[6] = (((dt.tm_year - 2000) // 10) << 4) | (dt.tm_year - 2000) % 10
        self._start_tx()
        self._w_byte(0xBE)
        for byte in byte_l:
            self._w_byte(byte)
        self._end_tx()
