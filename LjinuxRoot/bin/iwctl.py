args = ljinux.based.user_vars["argj"].split()[1:]
argl = len(args)
if argl is 0:
    #interactive interface
    term_old = term.trigger_dict
    term.trigger_dict = {
        "ctrlX": 100,
        "ctrlK": 100,
        "ctrlD": 1,
        "enter": 0,
        "overflow": 0,
        "rest": "stack",
        "rest_a": "common",
        "echo": "common",
        "prefix": f"{colors.green_t}[iwd]{colors.endc}# ",
    }
    q = True
    term.buf[1] = ""
    while q:
        term.clear_line()
        term.focus = 0
        ljinux.io.ledset(1)
        try:
            term.program()
        except KeyboardInterrupt:
            continue
        ljinux.io.ledset(3)
        if term.buf[0] == 1:
            q = False
        elif term.buf[0] == 0:
            data = term.buf[1].split()
            datal = len(data)
            if datal > 0:
                if data[0] == "exit":
                    q = False
                elif data[0] == "device":
                    if datal > 1:
                        if data[1] == "list":
                            print('\n' + 26 * ' ' + "devices")
                            print(60 * "-")
                            print(
                                "Name" +
                                ' ' * 5 +
                                "Mac address" +
                                ' ' * 6 +
                                "Power"
                            )
                            print(60 * "-")
                            if "network" in ljinux.modules:
                                info = ljinux.modules["network"].get_ipconf()
                                print(
                                    ljinux.modules["network"].hw_name +
                                    ' ' * 5 +
                                    info["mac_pretty"] +
                                    ' ' * 3 +
                                    info["power"]
                                )
                                del info
                    else:
                        print()
                        ljinux.based.error(1)
            del data, datal
        term.buf[1] = ""
        print()
    term.trigger_dict = term_old
    del q, term_old
del args, argl
