vr("pr", True)
term.trigger_dict = {
    "ctrlD": 1,
    "ctrlC": 2,
    "enter": 0,
    "overflow": 0,
    "rest": "stack",
    "rest_a": "common",
    "echo": "common",
    "prefix": f"{colors.green_t}[iwd]{colors.endc}# ",
}

term.buf[1] = ""
vr("networks", {})

# main loop
while True:
    term.clear_line()
    term.focus = 0
    be.io.ledset(1)
    try:
        term.program()
    except KeyboardInterrupt:
        continue
    be.io.ledset(3)
    if term.buf[0] == 1:
        term.write("^D")
        term.buf[1] = ""
        term.focus = 0
        break
    elif term.buf[0] == 2:
        term.buf[1] = ""
        term.focus = 0
    elif term.buf[0] == 0:
        vr("data", term.buf[1].split())
        term.buf[1] = ""
        term.focus = 0
        vr("datal", len(vr("data")))
        if vr("datal") > 0:
            if vr("data")[0] == "exit":
                term.write()
                break
            elif (
                vr("datal") > 1
                and vr("data")[0] == "device"
                and vr("data")[1] == "list"
            ):
                be.api.setvar("return", "0")
                term.write("\n" + 26 * " " + "devices")
                term.write(60 * "-")
                term.write("Name" + " " * 5 + "Mac address" + " " * 6 + "Power")
                term.write(60 * "-")
                if vr("device_n") is not None:
                    vr("info", be.devices["network"][0].get_ipconf())
                    term.write(
                        device_n
                        + " " * 5
                        + info["mac_pretty"]
                        + " " * 3
                        + info["power"]
                    )
            elif (
                vr("data")[0] == "station"
                and vr("datal") > 2
                and vr("device_n") is not None
                and vr("device_n") == vr("data")[1]
            ):
                if vr("data")[2] == "scan":
                    dmtex(f"Wifi: Scanning")
                    vr("networks", be.devices["network"][0].scan())
                    be.api.setvar("return", "0")
                elif vr("data")[2] == "get-networks":
                    be.api.setvar("return", "0")
                    vr("namesl", [])  # net names list
                    vr("secl", [])  # net security list
                    vr("ranl", [])  # net range list
                    vr("maxn", 0)  # max no of items
                    vr("lent", 0)  # max len name

                    term.write("\n" + 21 * " " + "Available networks")
                    term.write(60 * "-")

                    for pv[get_pid()]["i"] in vr("networks"):
                        vra("namesl", vr("i"))
                        vr("maxn", max(len(vr("i")), vr("maxn")))
                        vra("secl", vr("networks")[vr("i")][0])

                        # signal range
                        vra("ranl", str(vr("networks")[vr("i")][1]) + " dBi")
                        vrp("lent")

                    term.write(
                        "Name"
                        + (vr("maxn") - 3) * " "
                        + "Security"
                        + 5 * " "
                        + "Signal"
                    )
                    for pv[get_pid()]["i"] in range(0, vr("lent")):
                        term.write(
                            vr("namesl")[vr("i")]
                            + " " * (vr("maxn") - len(vr("namesl")[vr("i")]) + 1)
                            + vr("secl")[vr("i")]
                            + " " * (13 - len(vr("secl")[vr("i")]))
                            + vr("ranl")[vr("i")]
                        )
                elif vr("datal") > 3 and vr("data")[2] == "connect":
                    dmtex(f"Wifi: Scanning")
                    vr("networks", be.devices["network"][0].scan())
                    if vr("data")[3] in vr("networks"):
                        vr("res", 1)
                        be.io.ledset(1)
                        if vr("networks")[vr("data")[3]][0] != "OPEN":
                            vr(
                                "passwd",
                                cptoml.fetch(vr("data")[3], subtable="IWD"),
                            )
                            if vr("passwd") is None:
                                try:
                                    vr(
                                        "passwd",
                                        input(
                                            "\nEnter password for {}: ".format(
                                                vr("data")[3]
                                            )
                                        ),
                                    )
                                except KeyboardInterrupt:
                                    pass
                            be.io.ledset(3)

                            if vr("passwd") is not None:
                                be.devices["network"][0].disconnect()
                                be.devices["network"][0].disconnect_ap()
                                dmtex('IWD: Connecting to: "{}"'.format(vr("data")[3]))
                                vr(
                                    "res",
                                    be.devices["network"][0].connect(
                                        vr("data")[3], vr("passwd")
                                    ),
                                )
                                if (
                                    (vr("res"))
                                    and vr("passwd") is not None
                                    and (
                                        vr("data")[3] not in cptoml.keys("IWD")
                                        or cptoml.fetch(vr("data")[3], subtable="IWD")
                                        != vr("passwd")
                                    )
                                ):
                                    # Store this network
                                    cptoml.put(
                                        vr("data")[3], vr("passwd"), subtable="IWD"
                                    )
                                    term.write(
                                        "\nConnection stored in `&/settings.toml`."
                                    )
                        else:
                            dmtex('IWD: Connecting to: "{}"'.format(vr("data")[3]))
                            vr(
                                "res",
                                be.devices["network"][0].connect(vr("data")[3]),
                            )
                        exec(vr("wifi_connect_msg"))
                    else:
                        term.write("\nNetwork not found")
                elif vr("datal") > 3 and vr("data")[2] == "ap_mode":
                    if hasattr(be.devices["network"][0], "connect_ap"):
                        vr("passwd", None)
                        try:
                            vr(
                                "passwd",
                                input(
                                    "\nEnter password for AP {}, or press CTRL+C: ".format(
                                        vr("data")[3]
                                    )
                                ),
                            )
                        except KeyboardInterrupt:
                            pass
                        vr(
                            "res",
                            be.devices["network"][0].connect_ap(
                                vr("data")[3], vr("passwd")
                            ),
                        )
                        exec(vr("wifi_ap_msg"))
                        be.api.setvar("return", str(int(not vr("res"))))
                    else:
                        dmtex("IWD: This interface does not support AP.")
                        term.write("\nIWD: This interface does not support AP.")

                elif vr("datal") > 2 and vr("data")[2] == "disconnect":
                    be.devices["network"][0].disconnect()
                    be.devices["network"][0].disconnect_ap()
                    dmtex("Wifi: Disconnected.")
                    be.api.setvar("return", "0")
                else:
                    term.write()
                    be.based.error(1)
                    be.api.setvar("return", "1")
            else:
                term.write()
                be.based.error(1)
                be.api.setvar("return", "1")
    term.buf[1] = ""
    term.write()
