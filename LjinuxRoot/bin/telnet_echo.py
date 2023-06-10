term.write("Starting telnetd")

cont = True
TIMEOUT = None
BACKLOG = 2
MAXBUF = 64

# The telnet commands
IAC = 255  # Interpret as Command
DO = 253  # Do option
DONT = 254  # Dont option
WILL = 251  # Will option
WONT = 252  # Wont option
SGA = 3  # Suppress Go Ahead
TT = 24  # Terminal Type
FC = 33  # Remote flow control
LF = 34  # Lineflow
NE = 39  # New environ
ECHO = 1  # Local echo
STATUS = 5  # Status request
SB = 250  # Subnegotiation
EON = 254  # End of negotiations

# Setting up the socket
global s
s = ljinux.modules["network"]._pool.socket(
    ljinux.modules["network"]._pool.AF_INET,
    ljinux.modules["network"]._pool.SOCK_STREAM,
)
s.settimeout(TIMEOUT)
s.bind(
    (
        str(ljinux.modules["network"].get_ipconf()["ip"]),
        23,
    )
)
s.listen(BACKLOG)
conn = None
addr = None

# Setup the buffers
rx_buf = bytearray(MAXBUF)  # Receive buffer
ps_buf = bytearray()  # Parse buffer
tx_buf = bytearray()  # Send buffer
ps = 0

term.write(
    "Listening on "
    + str(ljinux.modules["network"].get_ipconf()["ip"])
    + ":23 for telnet connections"
)

# Main loop
try:  # Bug
    try:
        while cont:
            term.write("Accepting connections")
            conn, addr = s.accept()
            conn.settimeout(TIMEOUT)
            term.write(f"Accepted connection from: {addr[0]}:{addr[1]}")
            while cont:
                size = conn.recv_into(rx_buf, MAXBUF)
                if len(rx_buf):
                    while ps < size:
                        mb = rx_buf[ps]
                        ps += 1
                        if mb == IAC:  # We begin parsing
                            mb = rx_buf[ps]
                            ps += 1
                            if mb == WILL:
                                mb = rx_buf[ps]
                                ps += 1
                                if mb == TT:
                                    term.write(
                                        "DEBUG IN WILL: Agree to negotiate terminal type."
                                    )
                                    tx_buf.append(IAC)
                                    tx_buf.append(WILL)
                                    tx_buf.append(TT)
                                elif mb == ECHO:
                                    term.write("DEBUG IN WILL: Client should not echo.")
                                    tx_buf.append(IAC)
                                    tx_buf.append(WONT)
                                    tx_buf.append(ECHO)
                                elif mb == FC:
                                    term.write(
                                        "DEBUG IN WILL: Refuse remote flow control."
                                    )
                                    tx_buf.append(IAC)
                                    tx_buf.append(WONT)
                                    tx_buf.append(FC)
                                elif mb == NE:
                                    term.write("DEBUG IN WILL: Refuse new environ.")
                                    tx_buf.append(IAC)
                                    tx_buf.append(WONT)
                                    tx_buf.append(NE)
                                elif mb == LF:
                                    term.write("DEBUG IN WILL: Refuse lineflow.")
                                    tx_buf.append(IAC)
                                    tx_buf.append(WONT)
                                    tx_buf.append(LF)
                                else:
                                    term.write(
                                        "DEBUG IN WILL: Refused option: " + str(mb)
                                    )
                                    tx_buf.append(IAC)
                                    tx_buf.append(DONT)
                                    tx_buf.append(mb)
                            elif mb == DO:
                                mb = rx_buf[ps]
                                ps += 1
                                if mb == TT:
                                    term.write(
                                        "DEBUG IN DO  : Agree to negotiate terminal type."
                                    )
                                    tx_buf.append(IAC)
                                    tx_buf.append(DO)
                                    tx_buf.append(TT)
                                elif mb == STATUS:
                                    term.write(
                                        "DEBUG IN DO  : Agree to negotiate status."
                                    )
                                elif mb == SGA:
                                    term.write(
                                        "DEBUG IN DO  : Agree to ignore 'go ahead'."
                                    )
                                    tx_buf.append(IAC)
                                    tx_buf.append(WILL)
                                    tx_buf.append(SGA)
                                else:
                                    term.write(
                                        "DEBUG IN DO  : Refused option: " + str(mb)
                                    )
                                    tx_buf.append(IAC)
                                    tx_buf.append(DONT)
                                    tx_buf.append(mb)
                            elif mb == EON:
                                term.write("DEBUG IN IAC: Negotiations end.")
                                ps += 1
                                # tx_buf.append(IAC)
                                # tx_buf.append(WILL)
                                # tx_buf.append(EON)
                            else:
                                term.write("DEBUG IN IAC: Refuse option: " + str(mb))
                                tx_buf.append(IAC)
                                tx_buf.append(DONT)
                                tx_buf.append(mb)
                        else:  # We stash it as text
                            ps_buf.append(mb)
                        del mb
                    ps = 0
                    if len(tx_buf):
                        conn.send(tx_buf)
                        term.write("Sent: " + str(bytes(tx_buf)))
                        tx_buf = bytearray()
                    if len(ps_buf):
                        term.write("Got: " + str(bytes(ps_buf)))
                        cont = not (b"\x04" in ps_buf)
                        ps_buf = bytearray()
            conn.close()
            conn = None
            gc.collect()
    except KeyboardInterrupt:  # I have to
        raise KeyboardInterrupt  # This somehow works
except KeyboardInterrupt:
    term.write("Cleaning up..")

if conn is not None:
    conn.close()
del (
    conn,
    addr,
    rx_buf,
    ps_buf,
    tx_buf,
    s,
    BACKLOG,
    TIMEOUT,
    MAXBUF,
    ps,
    IAC,
    DO,
    DONT,
    WILL,
    WONT,
    SGA,
    TT,
    FC,
    LF,
    NE,
    ECHO,
    STATUS,
    SB,
    EON,
)
