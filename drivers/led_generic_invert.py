class led_generic_invert:
    def __init__(self):
        self._dg = None  # digitalio object

    def setup(self, dg) -> None:
        if self._dg is not None:
            return
        self._dg = dg
        self._dg.switch_to_output()
        self._dg.value = 1

    @property
    def value(self):
        if self._dg is None:
            return
        return not self._dg.value

    @value.setter
    def value(self, value) -> None:
        if self._dg is None:
            return
        if value in [None, False]:
            value = 0
        elif value is True:
            value = 1
        if isinstance(value, int) or value is None:
            self._dg.value = value in [0, 3, 4, 5]
        elif isinstance(value, tuple):
            self._dg.value = not sum(value)
        else:
            raise TypeError("Invalid led value type")

    def deinit(self) -> None:
        if self._dg is not None:
            self._dg.deinit()
