ljinux.based.user_vars["return"] = "0"
args = ljinux.based.user_vars["argj"].split()[1:]
argl = len(args)

device_n = (
    ljinux.modules["network"].hw_name
    if (
        "network" in ljinux.modules
        and ljinux.modules["network"].interface_type == "wifi"
    )
    else None
)

if argl is 0:
    # interactive interface
    term_old = term.trigger_dict
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
    networks = dict()

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
            data = term.buf[1].split()
            term.buf[1] = ""
            term.focus = 0
            datal = len(data)
            if datal > 0:
                if data[0] == "exit":
                    term.write()
                    break
                elif datal > 1 and data[0] == "device" and data[1] == "list":
                    ljinux.based.user_vars["return"] = "0"
                    term.write("\n" + 26 * " " + "devices")
                    term.write(60 * "-")
                    term.write("Name" + " " * 5 + "Mac address" + " " * 6 + "Power")
                    term.write(60 * "-")
                    if device_n is not None:
                        info = ljinux.modules["network"].get_ipconf()
                        term.write(
                            device_n
                            + " " * 5
                            + info["mac_pretty"]
                            + " " * 3
                            + info["power"]
                        )
                        del info
                elif (
                    data[0] == "station"
                    and datal > 2
                    and device_n is not None
                    and device_n == data[1]
                ):
                    if data[2] == "scan":
                        dmtex(f"Wifi: Scanning")
                        networks = ljinux.modules["network"].scan()
                        ljinux.based.user_vars["return"] = "0"
                    elif data[2] == "get-networks":
                        ljinux.based.user_vars["return"] = "0"
                        namesl = []  # net names list
                        secl = []  # net security list
                        ranl = []  # net range list
                        maxn = lent = 0  # max len name and no of items

                        term.write("\n" + 21 * " " + "Available networks")
                        term.write(60 * "-")

                        for i in networks:
                            namesl.append(i)
                            maxn = max(len(i), maxn)
                            secl.append(networks[i][0])

                            # signal range
                            if networks[i][1] > -30:
                                ranl.append("****")
                            elif networks[i][1] > -50:
                                ranl.append("***")
                            elif networks[i][1] > -70:
                                ranl.append("**")
                            elif networks[i][1] > -80:
                                ranl.append("*")
                            else:
                                ranl.append("bad")
                            lent += 1

                        term.write(
                            "Name" + (maxn - 3) * " " + "Security" + 5 * " " + "Signal"
                        )
                        for i in range(0, lent):
                            term.write(
                                namesl[i]
                                + " " * (maxn - len(namesl[i]) + 1)
                                + secl[i]
                                + " " * (13 - len(secl[i]))
                                + ranl[i]
                            )
                        del namesl, ranl, secl, maxn, lent
                    elif datal > 3 and data[2] == "connect":
                        dmtex(f"Wifi: Scanning")
                        networks = ljinux.modules["network"].scan()
                        if data[3] in networks:
                            res = 1
                            if networks[data[3]][0] != "OPEN":
                                ljinux.io.ledset(1)
                                passwd = None
                                try:
                                    passwd = input(f"\nEnter password for {data[3]}: ")
                                except KeyboardInterrupt:
                                    pass
                                ljinux.io.ledset(3)

                                if passwd is not None:
                                    ljinux.modules["network"].disconnect()
                                    dmtex(f'IWD: Connecting to: "{data[3]}"')
                                    res = ljinux.modules["network"].connect(
                                        data[3], passwd
                                    )
                                    if (not res) and (
                                        data[3] not in cptoml.keys("IWD")
                                        or cptoml.fetch(data[3], subtable="IWD")
                                        != passwd
                                    ):
                                        # Store this network
                                        cptoml.put(data[3], passwd, subtable="IWD")
                                        term.write(
                                            "\nConnection stored in `&/settings.toml`."
                                        )
                                del passwd
                            else:
                                dmtex(f'IWD: Connecting to: "{data[3]}"')
                                res = ljinux.modules["network"].connect(data[3])
                            if not res:
                                dmtex("IWD: Connected to network successfully.")
                                term.write("\nConnected successfully.")
                            else:
                                dmtex("IWD: Connection to network failed.")
                                term.write("\nConnection failed.")
                            ljinux.based.user_vars["return"] = str(res)
                            del res
                        else:
                            term.write("\nNetwork not found")
                    elif datal > 3 and data[2] == "ap_mode":
                        if hasattr(ljinux.modules["network"], "connect_ap"):
                            passwd = None
                            try:
                                passwd = input(
                                    f"\nEnter password for AP {data[3]}, or press CTRL+C: "
                                )
                            except KeyboardInterrupt:
                                pass
                            res = ljinux.modules["network"].connect_ap(data[3], passwd)
                            if not res:
                                dmtex("IWD: AP started successfully.")
                                term.write("\nIWD: AP started successfully.")
                            else:
                                dmtex("IWD: AP creation failed.")
                                term.write("\nIWD: AP creation failed.")
                            ljinux.based.user_vars["return"] = str(res)
                            del passwd, res
                        else:
                            dmtex("IWD: This interface does not support AP.")
                            term.write("\nIWD: This interface does not support AP.")

                    elif datal > 2 and data[2] == "disconnect":
                        ljinux.modules["network"].disconnect()
                        dmtex("Wifi: Disconnected.")
                        ljinux.based.user_vars["return"] = "0"
                    else:
                        term.write()
                        ljinux.based.error(1)
                        ljinux.based.user_vars["return"] = "1"
                else:
                    term.write()
                    ljinux.based.error(1)
                    ljinux.based.user_vars["return"] = "1"
            del data, datal
        term.buf[1] = ""
        term.write()
    term.trigger_dict = term_old
    del term_old, networks
else:
    passwd = None
    inc = 1
    if args[0] == "--passphrase":
        if args[1].startswith('"'):
            while True:
                if args[inc].endswith('"'):
                    break
                elif inc < argl:
                    inc += 1
                else:
                    ljinux.based.error(1)
                    inc = -1
            if inc is not -1:
                passwd = args[1] + " "
                for i in range(2, inc + 1):
                    passwd += args[i] + " "
                passwd = passwd[1:-2]
        else:
            passwd = args[1]
    else:
        inc = None
    if inc is not None:
        inc += 1
        args = args[inc:]
        argl -= inc
    del inc

    if argl > 2 and args[0] == "station" and args[1] == device_n:
        if argl > 3 and args[2] == "connect":
            networks = ljinux.modules["network"].scan()
            if args[3] in networks:
                res = 1
                if networks[args[3]][0] != "OPEN":
                    if passwd is not None:
                        ljinux.modules["network"].disconnect()
                        dmtex(f'IWD: Connecting to: "{args[3]}"')
                        res = ljinux.modules["network"].connect(args[3], passwd)
                    else:
                        term.write("Error: No password specified")
                else:
                    ljinux.modules["network"].disconnect()
                    dmtex(f'IWD: Connecting to: "{args[3]}"')
                    res = ljinux.modules["network"].connect(args[3])
                if res is not 0:
                    term.write("Connection failed.")
                    dmtex("IWD: Connection to network failed.")
                else:
                    dmtex("IWD: Connected to network successfully.")
                    if (
                        args[3] not in cptoml.keys("IWD")
                        or cptoml.fetch(args[3], subtable="IWD") != passwd
                    ):
                        # Store this network
                        cptoml.put(args[3], passwd, subtable="IWD")
                ljinux.based.user_vars["return"] = str(res)
                del res
            else:
                term.write("Network not found")
                ljinux.based.user_vars["return"] = "1"
            del networks
        elif args[2] == "ap_mode":
            if hasattr(ljinux.modules["network"], "connect_ap"):
                res = ljinux.modules["network"].connect_ap(args[3], passwd)
                if not res:
                    dmtex("IWD: AP started successfully.")
                else:
                    dmtex("IWD: AP creation failed.")
                ljinux.based.user_vars["return"] = str(res)
                del passwd, res
            else:
                dmtex("IWD: This interface does not support AP.")
        elif args[2] == "auto":
            if not ljinux.modules["network"].connected:
                # We don't need to run on an already connected interface
                stored_networks = cptoml.keys("IWD")
                if len(stored_networks):
                    scanned_networks = ljinux.modules["network"].scan()
                    best = None
                    best_index = None
                    for i in scanned_networks:
                        if i in stored_networks:
                            if best is None:  # We have no alternative
                                best = i
                                best_index = stored_networks.index(i)
                            else:  # We already have a network we can use
                                # Test if it's better
                                if best_index > stored_networks.index(i):
                                    # It's a better network
                                    best = i
                                    best_index = stored_networks.index(i)
                    del best_index, stored_networks, scanned_networks
                    if best is not None:  # We can connect
                        res = ljinux.modules["network"].connect(
                            best, cptoml.fetch(best, subtable="IWD")
                        )
                        if not res:
                            dmtex(
                                f"IWD-AUTO: Connected to network {best} successfully."
                            )
                        else:
                            dmtex(f"IWD-AUTO: Connection to network {best} failed.")
                        del res
                    else:  # We have to create a hotspot based on toml settings.
                        apssid = cptoml.fetch("SSID", subtable="IWD-AP")
                        appasswd = cptoml.fetch("PASSWD", subtable="IWD-AP")
                        if apssid is not None:
                            res = ljinux.modules["network"].connect_ap(apssid, appasswd)
                            if not res:
                                dmtex("IWD-AUTO: AP started successfully.")
                            else:
                                dmtex("IWD-AUTO: AP creation failed.")
                            del res
                        del apssid, appasswd
                    del best
        elif args[2] == "disconnect":
            ljinux.modules["network"].disconnect()
            ljinux.based.user_vars["return"] = "0"
        else:
            ljinux.based.error(1)
    else:
        ljinux.based.error(1)

    del passwd
del args, argl, device_n
