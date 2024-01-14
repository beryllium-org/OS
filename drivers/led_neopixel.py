from neopixel_write import neopixel_write

ledcases = {
    0: (0, 0, 0),  # off
    1: (3, 0, 0),  # Alternative idle, to indicate input
    2: (2, 0, 0),  # Idle
    3: (7, 7, 0),  # Activity
    4: (0, 0, 5),  # Waiting
    5: (0, 50, 0),  # Error
    6: (255, 255, 255),  # Your eyes are gone
    7: (0, 0, 10),  # Alternative waiting
}


class led_neopixel:
    def __init__(self):
        self._dg = None  # digitalio object
        self._c = (0, 0, 0)

    def setup(self, dg) -> None:
        if self._dg is not None:
            return
        self._dg = dg
        self._dg.switch_to_output()
        neopixel_write(self._dg, bytearray(ledcases[0]))

    @property
    def value(self):
        return (self._c[1], self._c[0], self._c[2])

    @value.setter
    def value(self, value) -> None:
        if self._dg is None:
            return
        elif isinstance(value, int):
            self._c = ledcases[value]
        elif isinstance(value, tuple):
            self._c = (value[1], value[0], value[2])
        elif value in [None, False]:
            self._c = ledcases[0]
        elif value is True:
            self._c = ledcases[3]
        else:
            raise TypeError("Invalid led value type")
        neopixel_write(self._dg, bytearray(self._c))

    def deinit(self) -> None:
        if self._dg is not None:
            self._dg.deinit()
            self._c = None
