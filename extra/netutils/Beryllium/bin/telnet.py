rename_process("telnet")
vr("opts", be.api.xarg())
vr("li", vr("opts")["w"] + vr("opts")["hw"])
if "help" in vr("opts")["o"] or "h" in vr("opts")["o"] or not len(vr("li")):
    term.write("USAGE: telnet [setup/deinit]")
elif len(vr("li")) and vr("li")[0] == "setup":
    systemprints(2, "Setup telnet")
    if "network" in be.devices and (
        be.devices["network"][0].connected or be.devices["network"][0].ap_connected
    ):
        if "ttyTELNET0" not in pv[0]["consoles"]:
            from telnet_console import telnet_console

            pv[0]["consoles"]["ttyTELNET0"] = telnet_console(
                be.devices["network"][0]._pool.socket(
                    be.devices["network"][0]._pool.AF_INET,
                    be.devices["network"][0]._pool.SOCK_STREAM,
                ),
                str(be.devices["network"][0].get_ipconf()["ip"]),
            )
            if "q" not in vr("opts")["o"]:
                term.write(
                    "Telnet configured.\n\n"
                    + "You may switch to it by running:\n\n"
                    + "terminal activate ttyTELNET0\n\n"
                    + "You can connect to the telnet server on:\n\n"
                    + str(be.devices["network"][0].get_ipconf()["ip"])
                )
            systemprints(1, "Setup telnet")
        else:
            term.write("Telnet already configured")
            systemprints(5, "Setup telnet")
    else:
        be.based.error(5)
elif len(vr("li")) and vr("li", pid=0) == "deinit":
    if "ttyTELNET0" in pv[0]["consoles"]:
        pv[0]["consoles"]["ttyTELNET0"].deinit()
        pv[0]["consoles"].pop("ttyTELNET0")
        del telnet_console
else:
    term.write("USAGE: telnet [setup/deinit]")
