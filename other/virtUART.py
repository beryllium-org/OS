from sys import stdin as _stdin
from sys import stdout as _stdout
from supervisor import runtime as _runtime


class virtUART:
    def __init__(self) -> None:
        self._in_buf = str()  # stored internally as str

    @property
    def in_waiting(self) -> int:
        """
        Reads the real stdin, stores the data in in_buf and returns the count.
        """
        self._rr()
        return len(self._in_buf)

    def _rr(self, block=False) -> None:
        """
        Reads the real stdin, fetches bytes as they come in,
        and stores them in a temporary buffer to provide `console` api.

        Use `block` to force a `.read()`.
        """
        if not block:
            while _runtime.serial_bytes_available:
                try:
                    self._in_buf += _stdin.read(1)
                except UnicodeError:
                    pass
        else:
            try:
                self._in_buf += _stdin.read()
            except UnicodeError:
                pass
        del block

    def reset_input_buffer(self):
        self._in_buf = str()

    def read(self, count=None):  # many types returned: Bytes, None.
        if count is None:
            if not self._in_buf:  # doesn't contains data
                self._rr(block=True)
            # else is handled in the end
        else:
            got = -1
            while got < count:  # not enough in buf, continue fetching
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

    def write(self, data="") -> int:
        lent = len(data)
        if data:
            _stdout.write(data.decode().replace("\n\r", "\n"))
            # `console` objects need `\n\r`, `stdout` needs `\n`.
        del data
        return lent

    def deinit(self) -> None:
        """
        Delete the internal buffer.
        """
        del self._in_buf
        del self
