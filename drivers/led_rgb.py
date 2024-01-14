ledcases = {
    0: (0, 0, 0),  # off
    1: (0, 1, 0),  # Alternative idle, to indicate input
    2: (0, 1, 0),  # Idle
    3: (1, 1, 0),  # Activity
    4: (0, 0, 1),  # Waiting
    5: (1, 0, 0),  # Error
    6: (1, 1, 1),  # Your eyes are gone
    7: (0, 0, 1),  # Alternative waiting
}


class led_rgb:
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
        return (self._c[1], self._c[0], self._c[2])

    @value.setter
    def value(self, value) -> None:
        if self._c is None:
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
        self._r.value = self._c[0]
        self._g.value = self._c[1]
        self._b.value = self._c[2]

    def deinit(self) -> None:
        if self._c is not None:
            self._r.deinit()
            self._g.deinit()
            self._b.deinit()
            self._c = None
