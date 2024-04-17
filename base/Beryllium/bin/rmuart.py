rename_process("rmuart")
vr("opts", be.api.xarg())
be.api.setvar("return", "0")
if "h" in vr("opts")["o"] or "help" in vr("opts")["o"]:
    term.write("Usage: rmuart [UART PORTS]...")
else:
    if len(vr("opts")["w"]):
        for pv[get_pid()]["i"] in vr("opts")["w"]:
            if vr("i") in pv[0]["consoles"]:
                if vr("i") != pv[0]["console_active"]:
                    if hasattr(pv[0]["consoles"], "deinit"):
                        pv[0]["consoles"].deinit()
                    pv[0]["consoles"].pop(vr("i"))
                    dmtex("/dev/" + vr("i") + " was removed")
                else:
                    term.write(
                        'Console "'
                        + vr("i")
                        + '" is the currently active console, cannot remove!'
                    )
            else:
                term.write('Console "' + vr("i") + '" does not exist!')
                be.api.setvar("return", "1")
    else:
        term.write("No consoles specified!")
        be.api.setvar("return", "1")
