rename_process("telnet")
vr("opts", ljinux.api.xarg())
vr("li", vr("opts")["w"] + vr("opts")["hw"])
if "help" in vr("opts")["o"] or "h" in vr("opts")["o"] or not len(vr("li")):
    term.write("USAGE: telnet [setup/deinit]")
elif len(pv[get_pid()]["li"]) and pv[get_pid()]["li"][0] == "setup":
    systemprints(2, "Setup telnet")
    if "network" in ljinux.modules and ljinux.modules["network"].connected:
        if "ttyTELNET0" not in pv[0]["consoles"]:
            from telnet_console import telnet_console

            pv[0]["consoles"]["ttyTELNET0"] = telnet_console(
                ljinux.modules["network"]._pool.socket(
                    ljinux.modules["network"]._pool.AF_INET,
                    ljinux.modules["network"]._pool.SOCK_STREAM,
                ),
                str(ljinux.modules["network"].get_ipconf()["ip"]),
            )
            if "q" not in vr("opts")["o"]:
                term.write(
                    "Telnet configured.\n\n"
                    + "You may switch to it by running:\n\n"
                    + "terminal activate ttyTELNET0\n\n"
                    + "You can connect to the telnet server on:\n\n"
                    + str(ljinux.modules["network"].get_ipconf()["ip"])
                )
            systemprints(1, "Setup telnet")
        else:
            term.write("Telnet already configured")
            systemprints(5, "Setup telnet")
    else:
        ljinux.based.error(5)
elif len(vr("li")) and vr("li", pid=0) == "deinit":
    if "ttyTELNET0" in pv[0]["consoles"]:
        pv[0]["consoles"]["ttyTELNET0"].deinit()
        pv[0]["consoles"].pop("ttyTELNET0")
        del telnet_console
else:
    term.write("USAGE: telnet [setup/deinit]")
