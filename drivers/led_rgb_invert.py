ledcases = {
    0: (1, 1, 1),  # off
    1: (1, 0, 1),  # Alternative idle, to indicate input
    2: (1, 0, 1),  # Idle
    3: (0, 0, 1),  # Activity
    4: (1, 1, 0),  # Waiting
    5: (0, 1, 1),  # Error
    6: (0, 0, 0),  # Your eyes are gone
    7: (1, 1, 0),  # Alternative waiting
}


class led_rgb_invert:
    def __init__(self):
        self._r = None  # digitalio object, r
        self._g = None  # digitalio object, g
        self._b = None  # digitalio object, b
        self._c = None

    def setup(self, r, g, b):
        if self._c is not None:
            return
        self._r = r
        self._g = g
        self._b = b
        self._r.switch_to_output()
        self._g.switch_to_output()
        self._b.switch_to_output()
        self._r.value = 0
        self._g.value = 0
        self._b.value = 0
        self._c = (0, 0, 0)

    @property
    def value(self):
        if self._c is None:
            return
        return (not self._c[1], not self._c[0], not self._c[2])

    @value.setter
    def value(self, value) -> None:
        if self._c is None:
            return
        elif isinstance(value, int):
            self._c = ledcases[value]
        elif isinstance(value, tuple):
            self._c = (not value[1], not value[0], not value[2])
        elif value in [None, False]:
            self._c = ledcases[0]
        elif value is True:
            self._c = ledcases[3]
        else:
            raise TypeError("Invalid led value type")
        self._r.value = self._c[0]
        self._g.value = self._c[1]
        self._b.value = self._c[2]

    def deinit(self) -> None:
        if self._c is not None:
            self._r.deinit()
            self._g.deinit()
            self._b.deinit()
            self._c = None
