from board import DISPLAY as _display
from sys import stdin as _stdin
from sys import stdout as _stdout
from supervisor import runtime as _runtime
import displayio
import terminalio

_palette = displayio.Palette(2)
_palette[1] = 0xFFFFFF

cl_str = b"\x1b[2J\x1b[3J\x1b[H"
lm_str = (
    cl_str
    + b" Console locked, press ENTER to unlock\n\r"
    + b"-" * 39
    + "\n\r"
    + "  ,-----------,     System active\n\r"
    + "  | 4    9.01 |     -------------\n\r"
    + "  |           |\n\r"
    + "  |           |     Battery: ???%\n\r"
    + "  | BERYLLIUM |\n\r"
    + "  '-----------'\n\r"
)


class cardputerVT:
    def __init__(self) -> None:
        self._terminal = None
        self._r = None
        self._tg = None
        self._b = False
        self._lines = None
        self._chars = None
        self._conn = False
        self.bat_sense = None
        self._bat_vstate = -1
        self._in_buf = str()
        self._r = displayio.Group()
        font_width, font_height = terminalio.FONT.get_bounding_box()
        self._lines = int(_display.height / font_height) - 1
        self._chars = int(_display.width / font_width) - 1
        tg = displayio.TileGrid(
            terminalio.FONT.bitmap,
            pixel_shader=_palette,
            width=self._chars,
            height=self._lines,
            tile_width=font_width,
            tile_height=font_height,
            x=(_display.width - (self._chars * font_width)) // 2,
            y=(_display.height - (self._lines * font_height)) // 2,
        )
        self._terminal = terminalio.Terminal(tg, terminalio.FONT)
        self._r.append(tg)
        _display.root_group = self._r
        self._terminal.write(lm_str)

    @property
    def enabled(self):
        return self._conn

    @property
    def display(self):
        return _display

    @display.setter
    def display(self, displayobj) -> None:
        raise OSError("This console does not support alternative displays")

    @property
    def terminal(self):
        return self._terminal

    @property
    def size(self) -> list:
        return [self._chars, self._lines]

    @property
    def in_waiting(self) -> int:
        self._rr()
        return len(self._in_buf)

    def _rr(self, block=False) -> None:
        if not block:
            while _runtime.serial_bytes_available:
                cb = _stdin.read(1)
                if cb == chr(8):
                    cb = chr(127)
                elif cb == chr(3):
                    continue
                self._in_buf += cb
        else:
            self._in_buf += _stdin.read()

    @property
    def connected(self) -> bool:
        if not self._conn and self.in_waiting and "\n" in self._in_buf:
            self.enable()
        if self._in_buf:
            self.reset_input_buffer()
        if self.bat_sense is not None:
            if not self._conn:
                curr = self.bat_sense.percentage
                if curr != self._bat_vstate:
                    self._bat_vstate = curr
                    if curr < 10:
                        curr = str(2 * " " + curr)
                    elif curr < 100:
                        curr = str(" " + curr)
                    else:
                        curr = str(curr)
                    self._terminal.write(lm_str.replace("???", curr))
            else:
                self._bat_vstate = -1
        return self._conn

    def disconnect(self) -> None:
        self.disable()

    def reset_input_buffer(self):
        self._in_buf = str()

    def reset_input_buffer(self) -> None:
        self._in_buf = str()

    def read(self, count=None):
        if count is None:
            if not self._in_buf:
                self._rr(block=True)
        else:
            got = -1
            while got < count:
                self._rr()
                got = len(self._in_buf)
            del got
        if count is None:
            count = len(self._in_buf)
        try:
            res = bytes(self._in_buf[:count], "")
            self._in_buf = self._in_buf[count:]
            del count
            return res
        except:
            return None

    def enable(self) -> None:
        self._terminal.write(cl_str)
        _display.root_group = self._r
        self._conn = True
        _display.brightness = 1.0

    def disable(self) -> None:
        self._conn = False
        if self.bat_sense is not None:
            self.connected
        else:
            self._terminal.write(lm_str)

    def write(self, data=bytes) -> int:
        if not self._conn:
            return 0
        res = self._terminal.write(data)
        return res

    def deinit(self) -> None:
        del self._in_buf
        del self
