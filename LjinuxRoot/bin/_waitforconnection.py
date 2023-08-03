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
                term.console = pv[0]["consoles"][pv[get_pid()]["i"]]
                pv[0]["console_active"] = pv[get_pid()]["i"]
                pv[get_pid()]["cont"] = False
        else:
            # Fallback to detect_size for console detection.
            term.console = pv[0]["consoles"][pv[get_pid()]["i"]]
            for pv[get_pid()]["j"] in range(3):
                # Need to pass trice.
                vr("tmpd", term.detect_size())
                if vr("tmpd") != False:
                    pv[0]["console_active"] = pv[get_pid()]["i"]
                    term.console.reset_input_buffer()
                    pv[get_pid()]["cont"] = False
                else:
                    break
    ljinux.io.ledset(4)
    time.sleep(0.2)
time.sleep(0.2)  # Delay for the terminal to get used to it.
