import board, digitalio


class wiopad:
    def __init__(self):
        self.l = digitalio.DigitalInOut(board.SWITCH_LEFT)
        self.l.switch_to_input()
        self.r = digitalio.DigitalInOut(board.SWITCH_RIGHT)
        self.r.switch_to_input()
        self.d = digitalio.DigitalInOut(board.SWITCH_DOWN)
        self.d.switch_to_input()
        self.u = digitalio.DigitalInOut(board.SWITCH_UP)
        self.u.switch_to_input()
        self.p = digitalio.DigitalInOut(board.SWITCH_PRESS)
        self.p.switch_to_input()
        self.a = digitalio.DigitalInOut(board.BUTTON_1)
        self.a.switch_to_input()
        self.b = digitalio.DigitalInOut(board.BUTTON_2)
        self.b.switch_to_input()
        self.c = digitalio.DigitalInOut(board.BUTTON_3)
        self.c.switch_to_input()

    @property
    def in_waiting(self) -> int:
        """
        Reads the real stdin, stores the data in in_buf and returns the count.
        """
        return len(self.read())

    def reset_input_buffer(self):
        pass

    def read(self, count=None):  # many types returned: Bytes, None.
        res = b""
        if not self.l.value:
            res += b"a"
        if not self.r.value:
            res += b"d"
        if not self.u.value:
            res += b"w"
        if not self.d.value:
            res += b"s"
        if not self.p.value:
            res += b"\r"
        if not self.a.value:
            res += b"v"
        if not self.b.value:
            res += b"c"
        if not self.c.value:
            res += b"x"
        return res

    def write(self, data="") -> int:
        return len(data)

    def deinit(self) -> None:
        self.l.deinit()
        self.r.deinit()
        self.d.deinit()
        self.u.deinit()
        self.p.deinit()
        self.a.deinit()
        self.b.deinit()
        self.c.deinit()
        del self
