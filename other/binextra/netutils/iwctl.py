ljinux.api.setvar("return", "0")
vr("args", ljinux.based.user_vars["argj"].split()[1:])
vr("argl", len(vr("args")))

vr(
    "device_n",
    (
        ljinux.modules["network"].hw_name
        if (
            "network" in ljinux.modules
            and ljinux.modules["network"].interface_type == "wifi"
        )
        else None
    ),
)

if vr("argl") is 0:
    # interactive interface
    term.trigger_dict = {
        "ctrlD": 1,
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
        ljinux.io.ledset(1)
        try:
            term.program()
        except KeyboardInterrupt:
            continue
        ljinux.io.ledset(3)
        if term.buf[0] == 1:
            term.write("^D")
            term.buf[1] = ""
            term.focus = 0
            break
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
                    ljinux.api.setvar("return", "0")
                    term.write("\n" + 26 * " " + "devices")
                    term.write(60 * "-")
                    term.write("Name" + " " * 5 + "Mac address" + " " * 6 + "Power")
                    term.write(60 * "-")
                    if vr("device_n") is not None:
                        vr("info", ljinux.modules["network"].get_ipconf())
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
                        vr("networks", ljinux.modules["network"].scan())
                        ljinux.api.setvar("return", "0")
                    elif vr("data")[2] == "get-networks":
                        ljinux.api.setvar("return", "0")
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
                    elif datal > 3 and data[2] == "connect":
                        dmtex(f"Wifi: Scanning")
                        vr("networks", ljinux.modules["network"].scan())
                        if vr("data")[3] in networks:
                            vr("res", 1)
                            ljinux.io.ledset(1)
                            if vr("networks")[vr("data")[3]][0] != "OPEN":
                                vr(
                                    "passwd",
                                    cptoml.fetch(vr("data")[3], subtable="IWD"),
                                )
                                if vr("passwd") is not None:
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
                                ljinux.io.ledset(3)

                                if vr("passwd") is not None:
                                    ljinux.modules["network"].disconnect()
                                    dmtex(
                                        'IWD: Connecting to: "{}"'.format(vr("data")[3])
                                    )
                                    res = ljinux.modules["network"].connect(
                                        vr("data")[3], vr("passwd")
                                    )
                                    if (
                                        (not vr("res"))
                                        and vr("passwd") is not None
                                        and (
                                            vr("data")[3] not in cptoml.keys("IWD")
                                            or cptoml.fetch(
                                                vr("data")[3], subtable="IWD"
                                            )
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
                                    ljinux.modules["network"].connect(vr("data")[3]),
                                )
                            if not res:
                                dmtex("IWD: Connected to network successfully.")
                                term.write("\nConnected successfully.")
                            else:
                                dmtex("IWD: Connection to network failed.")
                                term.write("\nConnection failed.")
                            ljinux.api.setvar("return", str(vr("res")))
                        else:
                            term.write("\nNetwork not found")
                    elif vr("datal") > 3 and vr("data")[2] == "ap_mode":
                        if hasattr(ljinux.modules["network"], "connect_ap"):
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
                                ljinux.modules["network"].connect_ap(
                                    vr("data")[3], vr("passwd")
                                ),
                            )
                            if not vr("res"):
                                dmtex("IWD: AP started successfully.")
                                term.write("\nIWD: AP started successfully.")
                            else:
                                dmtex("IWD: AP creation failed.")
                                term.write("\nIWD: AP creation failed.")
                            ljinux.api.setvar("return", str(vr("res")))
                        else:
                            dmtex("IWD: This interface does not support AP.")
                            term.write("\nIWD: This interface does not support AP.")

                    elif vr("datal") > 2 and vr("data")[2] == "disconnect":
                        ljinux.modules["network"].disconnect()
                        dmtex("Wifi: Disconnected.")
                        ljinux.api.setvar("return", "0")
                    else:
                        term.write()
                        ljinux.based.error(1)
                        ljinux.api.setvar("return", "1")
                else:
                    term.write()
                    ljinux.based.error(1)
                    ljinux.api.setvar("return", "1")
        term.buf[1] = ""
        term.write()
else:
    vr("passwd", None)
    vr("inc", 1)
    if vr("args")[0] == "--passphrase":
        if vr("args")[1].startswith('"'):
            while True:
                if vr("args")[vr("inc")].endswith('"'):
                    break
                elif vr("inc") < vr("argl"):
                    vrp("inc")
                else:
                    ljinux.based.error(1)
                    vrm("inc")
            if vr("inc") is not -1:
                vr("passwd", vr("args")[1] + " ")
                for pv[get_pid()]["i"] in range(2, vr("inc") + 1):
                    vrp("passwd", vr("args")[vr("i")] + " ")
                vr("passwd", vr("passwd")[1:-2])
        else:
            vr("passwd", vr("args")[1])
    else:
        vr("inc", None)
    if vr("inc") is not None:
        vrp("inc")
        vr("args", vr("args")[vr("inc") :])
        vrm("argl", vr("inc"))

    if (
        vr("argl") > 2
        and vr("args")[0] == "station"
        and vr("args")[1] == vr("device_n")
    ):
        if vr("argl") > 3 and vr("args")[2] == "connect":
            vr("networks", ljinux.modules["network"].scan())
            if vr("args")[3] in vr("networks"):
                vr("res", 1)
                if vr("networks")[vr("args")[3]][0] != "OPEN":
                    vr("tpd", cptoml.fetch(vr("args")[3], subtable="IWD"))
                    if vr("passwd") is not None:
                        ljinux.modules["network"].disconnect()
                        dmtex('IWD: Connecting to: "{}"'.format(vr("args")[3]))
                        vr(
                            "res",
                            ljinux.modules["network"].connect(
                                vr("args")[3], vr("passwd")
                            ),
                        )
                    elif vr("tpd") is not None:
                        ljinux.modules["network"].disconnect()
                        dmtex(
                            'IWD: Connecting to: "{}" with stored password.'.format(
                                vr("args")[3]
                            )
                        )
                        vr(
                            "res",
                            ljinux.modules["network"].connect(vr("args")[3], vr("tpd")),
                        )
                    else:
                        term.write("Error: No password specified")
                else:
                    ljinux.modules["network"].disconnect()
                    dmtex('IWD: Connecting to: "{}"'.format(vr("args")[3]))
                    vr("res", ljinux.modules["network"].connect(vr("args")[3]))
                if vr("res") is not 0:
                    term.write("Connection failed.")
                    dmtex("IWD: Connection to network failed.")
                else:
                    dmtex("IWD: Connected to network successfully.")
                    if (
                        vr("args")[3] not in cptoml.keys("IWD")
                        or cptoml.fetch(vr("args")[3], subtable="IWD") != vr("passwd")
                    ) and vr("passwd") is not None:
                        # Store this network
                        cptoml.put(vr("args")[3], vr("passwd"), subtable="IWD")
                ljinux.api.setvar("return", str(vr("res")))
            else:
                term.write("Network not found")
                ljinux.api.setvar("return", "1")
        elif vr("args")[2] == "ap_mode" and vr("argl") > 3:
            if hasattr(ljinux.modules["network"], "connect_ap"):
                vr(
                    "res",
                    ljinux.modules["network"].connect_ap(vr("args")[3], vr("passwd")),
                )
                if not vr("res"):
                    dmtex("IWD: AP started successfully.")
                else:
                    dmtex("IWD: AP creation failed.")
                ljinux.api.setvar("return", str(vr("res")))
            else:
                dmtex("IWD: This interface does not support AP.")
        elif vr("args")[2] == "auto":
            if not ljinux.modules["network"].connected:
                # We don't need to run on an already connected interface
                vr("stored_networks", cptoml.keys("IWD"))
                if len(vr("stored_networks")):
                    vr("scanned_networks", ljinux.modules["network"].scan())
                    vr("best", None)  # The best network to connect to
                    vr("best_alt", None)  # An alternative, just in case.
                    vr("best_index", None)  # Rating
                    vr("best_alt_index", None)  # Rating for alt
                    for pv[get_pid()]["i"] in vr("scanned_networks"):
                        if vr("i") in vr("stored_networks"):
                            if vr("best") is None:  # We have no alternative
                                vr("best", vr("i"))
                                vr("best_index", vr("stored_networks").index(vr("i")))
                            else:  # We already have a network we can use
                                vr(
                                    "cind", vr("stored_networks").index(vr("i"))
                                )  # To test if it's better
                                if vr("best_index") > vr("cind"):
                                    # It's a better network
                                    vr("best_alt", vr("best"))
                                    vr("best_alt_index", vr("best_index"))
                                    vr("best", vr("i"))
                                    vr("best_index", vr("cind"))
                                elif vr("best_alt") is None or vr(
                                    "best_alt_index"
                                ) > vr("cind"):
                                    vr("best_alt", vr("i"))
                                    vr("best_alt_index", vr("cind"))
                    if vr("best") is not None:  # We can connect
                        vr(
                            "res",
                            ljinux.modules["network"].connect(
                                vr("best"), cptoml.fetch(vr("best"), subtable="IWD")
                            ),
                        )
                        if not vr("res"):
                            dmtex(
                                "IWD-AUTO: Connected to network {} successfully.".format(
                                    vr("best")
                                )
                            )
                        else:
                            dmtex(
                                "IWD-AUTO: Connection to network {} failed.".format(
                                    vr("best")
                                )
                            )
                            if vr("best_alt") is not None:
                                vr(
                                    "res",
                                    ljinux.modules["network"].connect(
                                        vr("best_alt"),
                                        cptoml.fetch(vr("best_alt"), subtable="IWD"),
                                    ),
                                )
                                if not vr("res"):
                                    dmtex(
                                        "IWD-AUTO: Connected to network {} successfully.".format(
                                            vr("best_alt")
                                        )
                                    )
                                else:
                                    dmtex(
                                        "IWD-AUTO: Connection to network {} failed.".format(
                                            vr("best_alt")
                                        )
                                    )
                            else:
                                dmtex(
                                    f"IWD-AUTO: No available alternative networks. ABORT."
                                )
                                vr("best", None)
                    # Workaround after failure.
                    if (
                        vr("best") is None
                    ):  # We have to create a hotspot based on toml settings.
                        vr("apssid", cptoml.fetch("SSID", subtable="IWD-AP"))
                        vr("appasswd", cptoml.fetch("PASSWD", subtable="IWD-AP"))
                        if vr("apssid") is not None:
                            vr(
                                "res",
                                ljinux.modules["network"].connect_ap(
                                    vr("apssid"), vr("appasswd")
                                ),
                            )
                            if not vr("res"):
                                dmtex("IWD-AUTO: AP started successfully.")
                            else:
                                dmtex("IWD-AUTO: AP creation failed.")
        elif vr("args")[2] == "disconnect":
            ljinux.modules["network"].disconnect()
            ljinux.api.setvar("return", "0")
        else:
            ljinux.based.error(1)
    else:
        ljinux.based.error(1)
