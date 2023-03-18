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
            print("^D")
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
                    print()
                    break
                elif datal > 1 and data[0] == "device" and data[1] == "list":
                    ljinux.based.user_vars["return"] = "0"
                    print("\n" + 26 * " " + "devices")
                    print(60 * "-")
                    print("Name" + " " * 5 + "Mac address" + " " * 6 + "Power")
                    print(60 * "-")
                    if device_n is not None:
                        info = ljinux.modules["network"].get_ipconf()
                        print(
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

                        print("\n" + 21 * " " + "Available networks")
                        print(60 * "-")

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

                        print(
                            "Name" + (maxn - 3) * " " + "Security" + 5 * " " + "Signal"
                        )
                        for i in range(0, lent):
                            print(
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
                                del passwd
                            else:
                                dmtex(f'IWD: Connecting to: "{data[3]}"')
                                res = ljinux.modules["network"].connect(data[3])
                            if res is 0:
                                dmtex("IWD: Connected to network successfully.")
                                print("\nConnected successfully.")
                            else:
                                dmtex("IWD: Connection to network failed.")
                                print("\nConnection failed.")
                            ljinux.based.user_vars["return"] = str(res)
                            del res
                        else:
                            print("\nNetwork not found")
                    elif datal > 2 and data[2] == "disconnect":
                        ljinux.modules["network"].disconnect()
                        dmtex("Wifi: Disconnected.")
                        ljinux.based.user_vars["return"] = "0"
                    else:
                        print()
                        ljinux.based.error(1)
                        ljinux.based.user_vars["return"] = "1"
                else:
                    print()
                    ljinux.based.error(1)
                    ljinux.based.user_vars["return"] = "1"
            del data, datal
        term.buf[1] = ""
        print()
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
                        print("Error: No password specified")
                else:
                    ljinux.modules["network"].disconnect()
                    dmtex(f'IWD: Connecting to: "{args[3]}"')
                    res = ljinux.modules["network"].connect(args[3])
                if res is not 0:
                    print("Connection failed.")
                    dmtex("IWD: Connection to network failed.")
                else:
                    dmtex("IWD: Connected to network successfully.")
                ljinux.based.user_vars["return"] = str(res)
                del res
            else:
                print("Network not found")
                ljinux.based.user_vars["return"] = "1"
            del networks
        elif args[2] == "disconnect":
            ljinux.modules["network"].disconnect()
            ljinux.based.user_vars["return"] = "0"
        else:
            ljinux.based.error(1)
    else:
        ljinux.based.error(1)

    del passwd
del args, argl, device_n
