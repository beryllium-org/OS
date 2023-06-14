opts = ljinux.api.xarg()
li = opts["w"] + opts["hw"]
if "help" in opts["o"] or "h" in opts["o"] or not len(li):
    term.write("USAGE: telnet [setup/deinit]")
if len(li) and li[0] == "setup":
    if "network" in ljinux.modules and ljinux.modules["network"].connected:
        if "ttyTELNET0" not in consoles:
            from telnet_console import telnet_console

            consoles.update(
                {
                    "ttyTELNET0": telnet_console(
                        ljinux.modules["network"]._pool.socket(
                            ljinux.modules["network"]._pool.AF_INET,
                            ljinux.modules["network"]._pool.SOCK_STREAM,
                        ),
                        str(ljinux.modules["network"].get_ipconf()["ip"]),
                    ),
                }
            )
            if "q" not in opts["o"]:
                term.write(
                    "Telnet configured.\n\n"
                    + "You may switch to it by running:\n\n"
                    + "terminal activate ttyTELNET0\n\n"
                    + "You can connect to the telnet server on:\n\n"
                    + str(ljinux.modules["network"].get_ipconf()["ip"])
                )
        else:
            term.write("Telnet already configured")
    else:
        ljinux.based.error(5)
elif len(li) and li[0] == "deinit":
    if "ttyTELNET0" in consoles:
        consoles["ttyTELNET0"].deinit()
        consoles.pop("ttyTELNET0")
        del telnet_console
else:
    term.write("USAGE: telnet [setup/deinit]")
del opts, li
