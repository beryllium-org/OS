rename_process("nano")
gc.collect()
gc.collect()
ljinux.io.ledset(1)  # we don't want to pretend activity
vr("sizee", term.detect_size(3))
if vr("sizee") != False and (vr("sizee")[0] > 14 and vr("sizee")[1] > 105):
    vr("filee", None)
    vr("exists", 2)
    vr("weltxt", "[ Welcome to nano.  For basic help, type Ctrl+G. ]")

    vr("versionn", "1.8.0")

    try:
        vr("filee", ljinux.based.user_vars["argj"].split()[1])
    except IndexError:
        pass

    if vr("filee") is not None:  # there is arg
        vr("exists", ljinux.api.isdir(vr("filee")))

    if vr("exists") == 1:  # it is dir
        vr("filee", None)
        vr("exists", 2)
        vr(
            "weltxt",
            "[ {} is a directory ]".format(vr("filee")[vr("filee").rfind("/") + 1 :]),
        )

    vr("dataa", [""])
    vr("lc", 0)  # line count
    if vr("exists") is 0:  # is file
        with ljinux.api.fopen(vr("filee")) as pv[get_pid()]["f"]:
            vr("ll", vr("f").readlines())
            vr("lines", [])
            for pv[get_pid()]["i"] in range(0, len(vr("ll"))):
                if vr("ll")[vr("i")] != "\n":
                    vra("lines", vr("ll")[vr("i")].replace("\n", ""))
                else:
                    vra("lines", "")
            vrd("ll")
            # vrd("i")

        ljinux.based.command.fpexec("/LjinuxRoot/bin/stringproccessing/line_wrap.py")
        vr("dataa", vr("lines"))
        vr("lc", len(vr("dataa")))
        vrd("lines")

    # in case of empty file
    if vr("dataa") == []:
        vr("dataa", [""])

    term.trigger_dict = {
        "ctrlX": 1,
        "ctrlK": 100,
        "ctrlC": 0,
        "up": 2,
        "down": 8,
        "pgup": 4,
        "pgdw": 5,
        "bck": 11,
        "tab": 12,
        "enter": 10,
        "overflow": 10,
        "rest": "stack",
        "rest_a": "common",
        "echo": "common",
        "prefix": "",
    }

    vr("target", vr("sizee")[0] - 3)  # no of lines per screen
    vr("cl", 0)  # current line
    vr("vl", 0)  # 1st visible line
    term.buf = [0, None]
    if vr("exists") == 2:
        vr("fnam", "New buffer")
    else:
        vr("fnam", vr("filee")[vr("filee").rfind("/") + 1 :])
    vr("spz", int((vr("sizee")[1] - 11 - len(vr("versionn")) - len(vr("fnam"))) / 2))
    vr("sps1", " " * (vr("spz") - 5))
    vr("sps2", " " * (vr("spz") + 6))
    vrd("spz")

    vr(
        "toptxt",
        "{}  LNL nano {}{}{}{}{}\n".format(
            colors.inverse,
            vr("versionn"),
            vr("sps1"),
            vr("fnam"),
            vr("sps2"),
            colors.uninverse,
        ),
    )
    vrd("versionn")
    vrd("sps1")
    vrd("sps2")
    vrd("fnam")

    vr("bottxt", "{}{}{}\n".format(colors.inverse, vr("weltxt"), colors.uninverse))
    vr("bottxt_offs", int((vr("sizee")[1] - len(vr("weltxt"))) / 2))
    vrd("weltxt")

    vr("toolsplit", " " * int(vr("sizee")[1] / 8 - 13 - (vr("sizee")[1] % 2)))

    vr(
        "toolbar_items",
        [
            "^G",
            " Help      ",
            "^O",
            " Write Out ",
            "^W",
            " Where Is  ",
            "^K",
            " Cut       ",
            "^T",
            " Execute   ",
            "^C",
            " Location  ",
            "M-U",
            " Undo      ",
            "M-A",
            " Set Mark  ",
            "\n^X",
            " Exit      ",
            "^R",
            " Read File ",
            "^\\",
            " Replace   ",
            "^U",
            " Paste     ",
            "^J",
            " Justify   ",
            "^_",
            " Go To Line",
            "M-E",
            " Redo      ",
            "M-6",
            " Copy",
        ],
    )

    vr("toolbar_txt", "")

    for pv[get_pid()]["i"] in range(0, len(vr("toolbar_items")), 2):
        vrp(
            "toolbar_txt",
            (
                colors.inverse
                + vr("toolbar_items")[vr("i")]
                + colors.uninverse
                + vr("toolbar_items")[vr("i") + 1]
                + vr("toolsplit")
            ),
        )
    vrd("toolbar_items")
    vrd("i")

    vr("q", True)
    vr("inb", False)  # in bottom box
    vr("bmod", None)  # 0 == saving, 1 == searching, more planned later
    vr("savee", 0)
    term.hold_stdout = True
    term.clear()
    term.nwrite(vr("toptxt"))
    vrd("toptxt")  # not gonna use it again
    term.move(x=vr("sizee")[0] - 2, y=vr("bottxt_offs"))
    term.nwrite(vr("bottxt"))
    vrd("bottxt")
    vrd("bottxt_offs")
    term.nwrite(vr("toolbar_txt"))
    if len(vr("dataa")) > 1:
        vr("sz", vr("sizee")[0] - 4)
        vr("ld", len(vr("dataa")))
        vr("ltd", vr("sz") if vr("sz") < vr("ld") else vr("ld"))
        vrd("sz")
        vrd("ld")
        for pv[get_pid()]["i"] in range(0, vr("ltd")):
            term.move(x=vr("i") + 2)
            term.nwrite(vr("dataa")[vr("i")])
        vrd("ltd")
    term.hold_stdout = False
    term.flush_writes()
    while vr("q"):
        try:
            if not vr("savee"):
                term.buf[1] = vr("dataa")[vr("cl")]
                term.move(x=vr("cl") - vr("vl") + 2, y=len(term.buf[1]))
                term.clear_line()
            ljinux.io.ledset(1)
            term.hold_stdout = False
            term.flush_writes()
            term.program()
            term.hold_stdout = True
            if not vr("savee"):
                vr("dataa")[vr("cl")] = term.buf[1]
            ljinux.io.ledset(3)
            if term.buf[0] is 9:  # kill
                term.focus = 0
                vr("q", False)
            elif term.buf[0] is 1 and not vr("savee"):  # save
                term.buf[1] = ""
                term.focus = 0
                term.move(x=vr("sizee")[0] - 2)
                vr("spsz", (vr("sizee")[1] - 21) * " ")
                term.write(
                    "{}Save modified buffer?{}{}".format(
                        colors.inverse, vr("spsz"), colors.uninverse
                    )
                )
                term.clear_line()
                term.write(f"{colors.inverse} Y{colors.uninverse} Yes")
                term.clear_line()
                term.nwrite(
                    "{} N{} No        {}{}^C{} Cancel".format(
                        colors.inverse,
                        colors.uninverse,
                        vr("toolsplit"),
                        colors.inverse,
                        colors.uninverse,
                    )
                )
                term.move(x=vr("sizee")[0] - 2, y=23)
                term.nwrite(colors.inverse)
                vrd("spsz")
                vrp("savee")

            elif term.buf[0] is 8 and not vr("savee"):  # down
                term.focus = 0
                vrp("cl")
                if vr("lc") - 1 <= vr("cl"):
                    vra("dataa", "")
                    vrp("lc")
                if (
                    vr("cl") - vr("vl") > vr("sizee")[0] - 5
                ):  # we are going out of screen
                    term.clear_line()
                    vrp("vl")
                    for pv[get_pid()]["i"] in range(
                        2, vr("sizee")[0] - 2
                    ):  # shift data
                        term.move(x=vr("i"))
                        term.clear_line()
                        term.nwrite(vr("dataa")[vr("vl") + vr("i") - 2])

            elif term.buf[0] is 2 and not vr("savee"):  # up
                term.focus = 0

                if vr("cl") > 0:
                    vrm("cl")
                    if vr("cl") - vr("vl") < 0:
                        vrm("vl")
                        for pv[get_pid()]["i"] in range(
                            2, vr("sizee")[0] - 2
                        ):  # shift data
                            term.move(x=vr("i"), y=0)
                            term.clear_line()
                            term.nwrite(vr("dataa")[vr("vl") + vr("i") - 2])

            elif term.buf[0] is 10:  # insert empty line (enter)
                if not vr("savee"):
                    vra("dataa", vr("dataa")[vr("lc") - 1])  # last line to new line
                    vr("noffs", 0)
                    vr("copyover", False)
                    if len(term.buf[1]) == term.focus and len(term.buf[1]) is not 0:
                        vrm("noffs")
                    elif term.focus is not 0:
                        vr("copyover", True)
                    else:
                        term.focus = 0
                    for pv[get_pid()]["i"] in range(
                        vr("lc") - 1, vr("cl") + 1 + vr("noffs"), -1
                    ):  # all lines from the end to here
                        pv[get_pid()]["dataa"][vr("i")] = vr("dataa")[vr("i") - 1]
                    vrp("lc")  # lc++
                    vrp("cl")
                    if vr("copyover"):
                        pv[get_pid()]["dataa"][vr("cl")] = vr("dataa")[vr("cl") - 1][
                            len(vr("dataa")[vr("cl") - 1]) - term.focus :
                        ]
                        pv[get_pid()]["dataa"][vr("cl") - 1] = vr("dataa")[
                            vr("cl") - 1
                        ][: len(vr("dataa")[vr("cl") - 1]) - term.focus]
                        term.buf[1] = vr("dataa")[vr("cl")]
                    elif not vr("noffs"):
                        pv[get_pid()]["dataa"][vr("cl")] = ""
                        term.buf[1] = ""
                    else:
                        pv[get_pid()]["dataa"][vr("cl") + vr("noffs")] = ""
                    vrd("noffs")
                    vrd("copyover")

                    # shift data
                    vr(
                        "tf",
                        vr("lc")
                        if not vr("lc") >= (vr("sizee")[0] - 3)
                        else vr("sizee")[0] - 4,
                    )

                    for pv[get_pid()]["i"] in range(0, vr("tf")):
                        term.move(x=vr("i") + 2)
                        term.clear_line()
                        term.nwrite(vr("dataa")[vr("vl") + vr("i")])
                    vrd("i")
                    vrd("tf")
                elif vr("savee") is 1:
                    # the "save y/n" prompt
                    if term.buf[1] in ["n", "N"]:
                        vr("q", False)  # abandon all hope (, ye who enter here)
                    elif term.buf[1] in ["y", "Y"]:
                        term.buf[1] = ""
                        term.focus = 0
                        vrp("savee")  # 2

                        # the "choose file name" prompt
                        term.move(x=vr("sizee")[0] - 2)

                        # show the file name suggested
                        term.clear_line()
                        term.nwrite(
                            "File name to write:" + (" " * (vr("sizee")[1] - 19))
                        )
                        term.move(x=vr("sizee")[0] - 1)
                        term.nwrite(colors.endc)
                        term.clear_line()
                        term.move(x=vr("sizee")[0])
                        term.clear_line()
                        term.nwrite(f"{colors.inverse}^C{colors.uninverse} Cancel")
                        vr("ffname", "")
                        try:
                            vr("ffname", ljinux.based.user_vars["argj"].split()[1])
                        except IndexError:
                            pass
                        term.move(x=vr("sizee")[0] - 2, y=21)
                        term.nwrite(colors.inverse)
                        term.buf[1] = vr("ffname")
                        term.focus = 0
                        vrd("ffname")
                    else:
                        term.nwrite(
                            "\010" * len(term.buf[1])
                            + " " * len(term.buf[1])
                            + "\010" * len(term.buf[1])
                        )
                elif vr("savee") == 2:
                    vr("cc", True)
                    vr("cl1", vr("lc") - 1)
                    while vr("cc"):
                        if (
                            vr("dataa")[vr("cl1")].isspace()
                            or vr("dataa")[vr("cl1")] == ""
                        ):
                            pv[get_pid()]["dataa"].pop()
                            vrm("cl1")
                        else:
                            vr("cc", False)
                    vrd("cc")
                    vrd("cl1")
                    with ljinux.api.fopen(term.buf[1], "w") as pv[get_pid()]["f"]:
                        if vr("f") is not None:
                            for pv[get_pid()]["i"] in vr("dataa"):
                                vr("f").write(vr("i") + "\n")
                            vrd("i")
                            vr("q", False)
                        else:
                            vr("nbottxt", '[ Failed to save "' + term.buf[1] + '" ]')
                            term.move(x=vr("sizee")[0] - 2)
                            term.clear_line()
                            term.move(
                                x=vr("sizee")[0] - 2,
                                y=int((vr("sizee")[1] - len(vr("nbottxt"))) / 2),
                            )
                            term.nwrite(
                                colors.inverse + vr("nbottxt") + colors.uninverse
                            )
                            vrd("nbottxt")
                            vr("savee", 0)
                            term.buf[1] = ""
                            term.focus = 0
                            term.move(x=vr("sizee")[0] - 1)
                            term.nwrite(vr("toolbar_txt"))

            elif term.buf[0] is 0 and vr("savee"):  # Ctrl C, abort saving
                vr("savee", 0)
                term.focus = 0
                term.move(x=vr("sizee")[0] - 2)
                term.nwrite(colors.endc + (" " * vr("sizee")[1]))
                term.move(x=vr("sizee")[0] - 1)
                term.nwrite(vr("toolbar_txt"))

            elif term.buf[0] is 11:  # backspace
                if len(term.buf[1]) - term.focus > 0:
                    term.backspace()
                    if not vr("savee"):
                        pv[get_pid()]["dataa"][vr("cl")] = term.buf[1]
                    else:
                        term.nwrite(
                            "\010" * len(term.buf[1])
                            + " " * len(term.buf[1])
                            + "\010" * len(term.buf[1])
                        )
                elif not vr("savee") and vr("cl") > 0:
                    # don't do it when in save mode

                    # treat last line
                    if vr("dataa")[vr("cl")] != "":
                        pv[get_pid()]["dataa"][vr("cl") - 1] += vr("dataa")[vr("cl")]

                    # backend shift
                    for pv[get_pid()]["i"] in range(vr("cl"), vr("lc")):
                        try:
                            pv[get_pid()]["dataa"][vr("i")] = vr("dataa")[vr("i") + 1]
                        except IndexError:
                            break

                    pv[get_pid()]["dataa"].pop()
                    vrm("lc")
                    vrm("cl")

                    # shift data
                    vr("td", False)  # to delete last line
                    vr("tf", None)  # range
                    vr("magic", vr("sizee")[0] - 4)
                    if vr("lc") > vr("magic"):
                        vr("tf", vr("magic"))
                    else:
                        vr("tf", vr("lc"))
                        if vr("lc") < vr("magic"):
                            # we have at least one empty from the weltext
                            vr("td", True)  # need to clear_line after line prints
                    for pv[get_pid()]["i"] in range(0, vr("tf")):
                        term.move(x=vr("i") + 2)
                        term.clear_line()
                        try:
                            term.nwrite(vr("dataa")[vr("vl") + vr("i")])
                        except IndexError:  # Does not account for scroll well
                            pass
                    if vr("td"):
                        term.move(x=vr("tf") + 2)
                        term.clear_line()
                    vrd("td")
                    vrd("tf")
                    vrd("magic")

            elif term.buf[0] is 12:  # add tab
                term.nwrite(" " * 4)
                vr("insertion_pos", len(term.buf[1]) - term.focus)
                term.buf[1] = (
                    term.buf[1][: vr("insertion_pos")]
                    + " " * 4
                    + term.buf[1][vr("insertion_pos") :]
                )
                pv[get_pid()]["dataa"][vr("cl")] = term.buf[1]
                vrd("insertion_pos")

            elif vr("savee"):
                # counter visual bug
                term.nwrite(len(term.buf[1]) * "\010")

        except KeyboardInterrupt:
            pass

    term.buf[1] = ""
    term.nwrite(colors.endc)
    term.clear()

    ljinux.api.setvar("return", "0")
else:
    ljinux.based.error(13, "15x106")  # minimum size error
    ljinux.api.setvar("return", "1")
term.hold_stdout = False
term.flush_writes()
