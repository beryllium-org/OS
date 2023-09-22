IAC = 255  # Interpret as Command
DO = 253  # Do option
DONT = 254  # Dont option
WILL = 251  # Will option
WONT = 252  # Wont option
TT = 24  # Terminal Type
ECHO = 1  # Local echo
EON = 254  # End of negotiations


class telnet_console:  # The actual class you need to use
    def __init__(self, socket, ip, maxbuf=64, backlog=2, timeout=0) -> None:
        """
        Socket object
        IP to bind to (str)
        max buffer length
        backlog of connections
        timeout is the time to wait for possible connections & recv
        """

        # Private
        self._in_buf = str()  # stored internally as str
        self._socket = socket
        self._socket.settimeout(timeout)
        """
        0 for non-blocking
        We do need the connection attempts to be blocking
        """
        self._socket.bind((ip, 23))  # Telnet port
        self._socket.listen(backlog)
        self._conn = None  # Connection storage
        self._client = None  # IP of client
        self._rx_buf = bytearray(maxbuf)  # Receive buffer, static allocation
        self._ps_buf = bytearray()  # Parse buffer
        self._tx_buf = bytearray()  # Send buffer
        self._timeout = timeout
        self._maxbuf = maxbuf

    def _connect(self) -> None:
        failc = 0
        if self._conn is None:
            try:
                self._conn, self._client = self._socket.accept()
                self._conn.settimeout(10)
                self._conn.setblocking(True)
                """
                Do not make the connection nonblocking now
                since the negotiation may take time.
                """
                cont = True

                while cont:
                    ps = 0
                    size = self._conn.recv_into(self._rx_buf, self._maxbuf)
                    while ps < size:
                        mb = self._rx_buf[ps]
                        ps += 1
                        if mb == IAC:
                            mb = self._rx_buf[ps]
                            ps += 1
                            if mb == WILL:
                                mb = self._rx_buf[ps]
                                ps += 1
                                if mb == TT:  # Mandatory
                                    self._tx_buf.append(IAC)
                                    self._tx_buf.append(WILL)
                                    self._tx_buf.append(TT)
                                else:
                                    self._tx_buf.append(IAC)
                                    self._tx_buf.append(DONT)
                                    self._tx_buf.append(mb)
                            elif mb == DO:
                                mb = self._rx_buf[ps]
                                ps += 1
                                if mb == ECHO:  # We accept
                                    self._tx_buf.append(IAC)
                                    self._tx_buf.append(DO)
                                    self._tx_buf.append(ECHO)
                                else:
                                    self._tx_buf.append(IAC)
                                    self._tx_buf.append(DONT)
                                    self._tx_buf.append(mb)
                            elif mb == EON:
                                """
                                Negotiations from client done.
                                Proceed to disable echo.
                                """
                                self._tx_buf.append(IAC)
                                self._tx_buf.append(WILL)
                                self._tx_buf.append(ECHO)
                                ps += 1
                            elif mb == WONT:  # Client said WONT ECHO.
                                ps += 1
                                cont = False  # We are finally done.
                            else:
                                self.disconnect()
                                raise ConnectionError("Negotiation failed")
                        else:  # Negotiation failed
                            self.disconnect()
                            raise ConnectionError("Negotiation failed")
                        self._rt()  # Transmit
                    del size, ps
                del cont
            except OSError:  # No connection took place.
                self.disconnect()

            if self._conn is not None:
                """
                Now make the connection non-blocking
                since we need to fetch text asyncronously.
                """
                self._conn.settimeout(0)
                self._conn.setblocking(False)

    def _rt(self) -> None:
        """
        The internal transmit function.
        Clears the tx bytearray.
        """
        sent = 0
        while sent != len(self._tx_buf):  # Bulk
            try:
                sent += self._conn.send(memoryview(self._tx_buf)[sent:])
            except OSError:  # EAGAIN for some reason.
                pass
            except BrokenPipeError:
                self.disconnect()
                break
        self._tx_buf = bytearray()

    def disconnect(self) -> None:
        """
        Disconnect and clear the connection.
        """
        if self._conn is not None:
            self._conn.close()
            self._conn = None
        self._reset_rx_buffer()

    @property
    def connected(self) -> bool:
        self._connect()
        return self._conn is not None

    @property
    def client(self):
        """
        Returns a tuple with the connected client's ip and port.
        If no connection, returns None.
        """
        return self._client if self.connected else None

    def _rr(self, block=False) -> None:
        """
        The internal receive function.
        Leaves the data in the internal buffer _ps_buf.
        """
        if self.connected:
            if block:
                self._conn.settimeout(10)
                self._conn.setblocking(True)
            try:
                while self.connected:  # Will get interrupted by except
                    size = self._conn.recv_into(self._rx_buf, self._maxbuf)
                    if size:
                        self._ps_buf += memoryview(self._rx_buf)[:size]
                    del size
            except OSError:
                pass
            except BrokenPipeError:
                self.disconnect()
            if block:
                self._conn.settimeout(0)
                self._conn.setblocking(False)

    @property
    def in_waiting(self) -> int:
        """
        Returns the len of bytes in the internal (incoming) buffer.
        """
        if self.connected:
            self._rr()
            return len(self._ps_buf)
        else:
            return 0

    def out_waiting(self) -> int:
        """
        Returns the len of bytes in the internal (outgoing) buffer.
        """
        return len(self._tx_buf)

    def _reset_rx_buffer(self) -> None:
        for i in range(len(self._rx_buf)):
            self._rx_buf[i] = 0

    def reset_input_buffer(self) -> None:
        for i in range(len(self._rx_buf)):
            self._rx_buf[i] = 0

    def reset_output_buffer(self) -> None:
        self._tx_buf = bytearray()

    def read(self, count=None):  # many types returned: Bytes, None.
        if self.connected:
            if count is not None:
                while len(self._ps_buf) < count:
                    self._rr()
            else:
                self._rr(block=count is None)
                count = len(self._ps_buf)
            res = bytes(memoryview(self._ps_buf)[:count])
            self._ps_buf = self._ps_buf[count:]
            return res
        else:
            return None

    def write(self, data="") -> int:
        lent = len(data)
        if hasattr(self, "_tx_buf"):
            self._tx_buf += data
            if self.connected:
                self._rt()
        return lent

    def deinit(self) -> None:
        """
        Delete the internal stuff and close any connections.
        """
        self.disconnect()
        del (
            self._in_buf,
            self._conn,
            self._client,
            self._socket,
            self._timeout,
            self._tx_buf,
        )
        del self._rx_buf, self._ps_buf, self._maxbuf, self
