import displayio
import terminalio

_palette = displayio.Palette(2)
_palette.make_transparent(0)
_palette[1] = 0xFFFFFF


class displayiotty:
    def __init__(self):
        self._display = None
        self._terminal = None
        self._r = None
        self._tg = None
        self._b = False
        self._lines = None
        self._chars = None
        self.stdio = None
        self._conn = False

    @property
    def enabled(self):
        return self._conn

    @property
    def display(self):
        return self._display

    @display.setter
    def display(self, displayobj) -> None:
        self._display = displayobj
        self._r = displayio.Group()
        font_width, font_height = terminalio.FONT.get_bounding_box()
        self._lines = int(self._display.height / font_height) - 1
        self._chars = int(self._display.width / font_width) - 1
        tg = displayio.TileGrid(
            terminalio.FONT.bitmap,
            pixel_shader=_palette,
            width=self._chars,
            height=self._lines,
            tile_width=font_width,
            tile_height=font_height,
            x=(self._display.width - (self._chars * font_width)) // 2,
            y=(self._display.height - (self._lines * font_height)) // 2,
        )
        self._terminal = terminalio.Terminal(tg, terminalio.FONT)
        self._r.append(tg)
        self.disable()

    @property
    def terminal(self):
        return self._terminal

    @property
    def size(self) -> list:
        return [self._chars, self._lines]

    @property
    def in_waiting(self) -> int:
        return self.stdio.in_waiting

    @property
    def out_waiting(self) -> int:
        return self.stdio.out_waiting if hasattr(self.stdio, "out_waiting") else 0

    @property
    def connected(self) -> bool:
        return self.stdio.connected if hasattr(self.stdio, "connected") else self._conn

    def flush(self) -> None:
        self.stdio.flush()

    def reset_input_buffer(self) -> None:
        if self.stdio is not None:
            self.stdio.reset_input_buffer()

    def reset_output_buffer(self) -> None:
        if self.stdio is not None:
            self.stdio.reset_output_buffer()

    def read(self, no=None) -> bytes:
        if self._conn and (self.stdio is not None):
            return self.stdio.read(no)

    def enable(self) -> None:
        self._initchk()
        self._display.root_group = self._r
        self._conn = True
        self._display.brightness = 1.0

    def disable(self) -> None:
        self._initchk()
        self._display.root_group = None
        self._conn = False
        self._display.brightness = 0.0

    def write(self, data: bytes) -> int:
        self._initchk()
        if not self._conn:
            return
        res = self._terminal.write(data)
        if self.stdio is not None:
            res = self.stdio.write(data)
        return res

    def _initchk(self) -> None:
        if self.display is None:
            raise RuntimeError("Display not set")
