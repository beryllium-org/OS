rename_process("ed")
gc.collect()
pv[get_pid()]["opts"] = ljinux.api.xarg()
pv[get_pid()]["appending"] = False
pv[get_pid()]["has_checked_args"] = False
pv[get_pid()]["txbuf"] = []
pv[get_pid()]["selected"] = None

term.trigger_dict.clear()
term.trigger_dict.update(
    {
        "prefix": "",
        "enter": 0,
        "ctrlC": 1,
        "ctrlD": 2,
        "overflow": 14,
        "rest": "stack",
        "rest_a": "common",
        "echo": "common",
    }
)

while True:
    term.clear_line()
    term.buf[1] = ""
    term.focus = 0
    ljinux.io.ledset(1)
    gc.collect()
    if pv[get_pid()]["has_checked_args"]:
        term.program()
    else:
        term.buf[0] = 0
    ljinux.io.ledset(3)
    if term.buf[0] is 2:
        break
    elif term.buf[0] is 1:
        term.write("^C")
    elif term.buf[0] is 0:
        if pv[get_pid()]["has_checked_args"]:
            term.write()
        if pv[get_pid()]["appending"]:
            if term.buf[1] != ".":
                pv[get_pid()]["txbuf"].append(term.buf[1])
            else:
                pv[get_pid()]["appending"] = False
        else:
            pv[get_pid()]["recv"] = term.buf[1].split(" ")
            if len(pv[get_pid()]["recv"]):
                if (pv[get_pid()]["recv"][0] == "r") or (
                    not pv[get_pid()]["has_checked_args"]
                ):
                    pv[get_pid()]["src"] = None
                    if not pv[get_pid()]["has_checked_args"]:
                        pv[get_pid()]["has_checked_args"] = True
                        if len(pv[get_pid()]["opts"]["w"]) is not 0:
                            pv[get_pid()]["src"] = pv[get_pid()]["opts"]["w"][0]
                    else:
                        if len(pv[get_pid()]["recv"]) > 1:
                            pv[get_pid()]["src"] = pv[get_pid()]["recv"][1]
                    if pv[get_pid()]["src"] is not None and (
                        pv[get_pid()]["src"].isspace() or pv[get_pid()]["src"] == ""
                    ):
                        pv[get_pid()]["src"] = None
                    if pv[get_pid()]["src"] is not None:
                        if ljinux.api.isdir(pv[get_pid()]["src"], getcwd()) is not 0:
                            pv[get_pid()]["src"] = None
                    if pv[get_pid()]["src"] is not None:
                        with ljinux.api.fopen(pv[get_pid()]["src"]) as f:
                            pv[get_pid()]["txbuf"] += f.readlines()
                            pv[get_pid()]["bl"] = 0
                            for pv[get_pid()]["linen"] in range(
                                len(pv[get_pid()]["txbuf"])
                            ):
                                pv[get_pid()]["txbuf"][pv[get_pid()]["linen"]] = pv[
                                    get_pid()
                                ]["txbuf"][pv[get_pid()]["linen"]][:-1]
                                pv[get_pid()]["bl"] += (
                                    len(pv[get_pid()]["txbuf"][pv[get_pid()]["linen"]])
                                    + 1
                                )
                                del pv[get_pid()]["linen"]
                        term.write(str(pv[get_pid()]["bl"]))
                        del pv[get_pid()]["bl"]
                    else:
                        term.write("?")
                    del pv[get_pid()]["src"]
                elif pv[get_pid()]["recv"][0].isdigit():
                    pv[get_pid()]["d"] = int(pv[get_pid()]["recv"][0])
                    if len(pv[get_pid()]["txbuf"]) >= pv[get_pid()]["d"]:
                        term.write(pv[get_pid()]["txbuf"][pv[get_pid()]["d"] - 1])
                    pv[get_pid()]["selected"] = pv[get_pid()]["d"]
                    del pv[get_pid()]["d"]
                elif pv[get_pid()]["recv"][0][0] == "s":
                    if (
                        pv[get_pid()]["recv"][0][1] == "/"
                        and pv[get_pid()]["recv"][0][-1] == "/"
                    ):
                        pv[get_pid()]["slist"] = pv[get_pid()]["recv"][0][2:-1].split(
                            "/"
                        )
                        pv[get_pid()]["sfinal"] = []
                        pv[get_pid()]["skip"] = 0
                        if len(pv[get_pid()]["slist"]) is not 2:
                            for pv[get_pid()]["itemn"] in range(
                                len(pv[get_pid()]["slist"])
                            ):
                                if not pv[get_pid()]["skip"]:
                                    pv[get_pid()]["cit"] = pv[get_pid()]["slist"][
                                        pv[get_pid()]["itemn"]
                                    ]
                                    while pv[get_pid()]["cit"].endswith("\\"):
                                        pv[get_pid()]["cit"] += "/"
                                        if (
                                            pv[get_pid()]["itemn"]
                                            < len(pv[get_pid()]["slist"])
                                            + pv[get_pid()]["skip"]
                                        ):
                                            pv[get_pid()]["cit"] += pv[get_pid()][
                                                "slist"
                                            ][
                                                pv[get_pid()]["itemn"]
                                                + 1
                                                + pv[get_pid()]["skip"]
                                            ]
                                        pv[get_pid()]["skip"] += 1
                                    pv[get_pid()]["sfinal"].append(pv[get_pid()]["cit"])
                                else:
                                    pv[get_pid()]["skip"] -= 1
                            del pv[get_pid()]["itemn"], pv[get_pid()]["cit"]
                        else:
                            pv[get_pid()]["sfinal"] = pv[get_pid()]["slist"]
                        del pv[get_pid()]["slist"], pv[get_pid()]["skip"]
                        if (len(pv[get_pid()]["sfinal"]) is not 2) or (
                            pv[get_pid()]["selected"] is None
                        ):
                            term.write("?")
                        else:
                            pv[get_pid()]["txbuf"][pv[get_pid()]["selected"] - 1] = pv[
                                get_pid()
                            ]["txbuf"][pv[get_pid()]["selected"] - 1].replace(
                                pv[get_pid()]["sfinal"][0], pv[get_pid()]["sfinal"][1]
                            )
                        del pv[get_pid()]["sfinal"]
                    else:
                        term.write("?")
                elif pv[get_pid()]["recv"][0] == "c":
                    pv[get_pid()]["txbuf"].clear()
                elif pv[get_pid()]["recv"][0] == "a":
                    pv[get_pid()]["appending"] = True
                elif pv[get_pid()]["recv"][0] == "w":
                    if len(pv[get_pid()]["recv"]) > 1:
                        with ljinux.api.fopen(pv[get_pid()]["recv"][1], "w") as f:
                            if f is not None:
                                for pv[get_pid()]["line"] in pv[get_pid()]["txbuf"]:
                                    f.write("{}\n".format(pv[get_pid()]["line"]))
                                    gc.collect()
                                del pv[get_pid()]["line"]
                            else:
                                term.write("?")
                    else:
                        term.write("?")
                elif pv[get_pid()]["recv"][0] == "q":
                    if pv[get_pid()]["selected"] is not None:
                        pv[get_pid()]["selected"] = None
                        term.write("?")
                    else:
                        break
                elif pv[get_pid()]["recv"][0] == ",p":
                    if len(pv[get_pid()]["txbuf"]):
                        for pv[get_pid()]["line"] in pv[get_pid()]["txbuf"]:
                            term.write(pv[get_pid()]["line"])
                            del pv[get_pid()]["line"]
                    else:
                        term.write("?")
                else:
                    term.write("?")
            else:
                term.write("?")
            del pv[get_pid()]["recv"]
term.buf[1] = ""
