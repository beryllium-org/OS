rename_process("waitforconnection")
vr("cont", True)
while vr("cont"):
    for pv[get_pid()]["i"] in range(2):
        ljinux.io.ledset(7)
        sleep(0.1)
        ljinux.io.ledset(4)
        sleep(0.1)
    for pv[get_pid()]["i"] in pv[0]["consoles"].keys():
        if hasattr(pv[0]["consoles"][pv[get_pid()]["i"]], "connected"):
            if pv[0]["consoles"][pv[get_pid()]["i"]].connected:
                term.console = pv[0]["consoles"][vr("i")]
                vr("console_active", vr("i"))
                vr("cont", False)
        else:
            # Fallback to detect_size for console detection.
            term.console = pv[0]["consoles"][pv[get_pid()]["i"]]
            vr("tmpd", term.detect_size())
            if vr("tmpd") != False:
                vr("console_active", vr("i"), pid=0)
                term.console.reset_input_buffer()
                vr("cont", False)
    ljinux.io.ledset(4)
    time.sleep(0.2)
time.sleep(0.2)  # Delay for the terminal to get used to it.
