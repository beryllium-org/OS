gc.collect()
gc.collect()
ljinux.io.ledset(1)  # we don't want to pretend activity
sizee = term.detect_size()
if sizee[0] > 14 and sizee[1] > 105:
    filee = None
    exists = 2
    weltxt = "[ Welcome to nano.  For basic help, type Ctrl+G. ]"

    versionn = "1.7.3"

    try:
        filee = ljinux.based.user_vars["argj"].split()[1]
    except IndexError:
        pass

    if filee is not None:  # there is arg
        exists = ljinux.api.isdir(filee)

    if exists == 1:  # it is dir
        filee = None
        exists = 2
        weltxt = "[ {} is a directory ]".format(filee[filee.rfind("/") + 1 :])

    dataa = [""]
    lc = 0  # line count
    if exists is 0:  # is file
        with open(ljinux.api.betterpath(filee), "r") as f:
            ll = f.readlines()
            ljinux.api.setvar("input", list())
            for i in range(0, len(ll)):
                if ll[i] != "\n":
                    ljinux.based.user_vars["input"].append(ll[i].replace("\n", ""))
                else:
                    ljinux.based.user_vars["input"].append("")
            del ll

        ljinux.based.command.fpexec("/LjinuxRoot/bin/stringproccessing/line_wrap.py")
        dataa = ljinux.based.user_vars["output"]
        lc = len(dataa)
        ljinux.api.setvar("output")

    # in case of empty file
    if dataa == []:
        dataa = [""]

    term_old = term.trigger_dict
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

    target = sizee[0] - 3  # no of lines per screen
    cl = 0  # current line
    vl = 0  # 1st visible line
    term.buf = [0, None]
    fnam = "New buffer" if exists == 2 else filee[filee.rfind("/") + 1 :]
    spz = int((sizee[1] - 11 - len(versionn) - len(fnam)) / 2)
    sps1 = " " * (spz - 5)
    sps2 = " " * (spz + 6)
    del spz

    toptxt = f"{colors.white_bg_black_bg}  LNL nano {versionn}{sps1}{fnam}{sps2}{colors.endc}\n"
    del versionn, sps1, sps2, fnam

    bottxt = f"{colors.white_bg_black_bg}{weltxt}{colors.endc}\n"
    bottxt_offs = int((sizee[1] - len(weltxt)) / 2)
    del weltxt

    toolsplit = " " * int(sizee[1] / 8 - 13 - (sizee[1] % 2))

    toolbar_items = [
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
    ]

    toolbar_txt = ""

    for i in range(0, len(toolbar_items), 2):
        toolbar_txt += (
            colors.white_bg_black_bg
            + toolbar_items[i]
            + colors.endc
            + toolbar_items[i + 1]
            + toolsplit
        )
    del toolbar_items

    q = True
    inb = False  # in bottom box
    bmod = None  # 0 == saving, 1 == searching, more planned later
    savee = 0
    term.clear()
    stdout.write(toptxt)
    del toptxt  # not gonna use it again
    term.move(x=sizee[0] - 2, y=bottxt_offs)
    stdout.write(bottxt)
    del bottxt, bottxt_offs
    stdout.write(toolbar_txt)
    if len(dataa) > 1:
        sz = sizee[0] - 4
        ld = len(dataa)
        ltd = sz if sz < ld else ld
        del sz, ld
        for i in range(0, ltd):
            term.move(x=i + 2)
            stdout.write(dataa[i])
        del ltd
    while q:
        try:
            if not savee:
                term.buf[1] = dataa[cl]
                term.move(x=cl - vl + 2, y=len(term.buf[1]))
                term.clear_line()
            ljinux.io.ledset(1)
            term.program()
            if not savee:
                dataa[cl] = term.buf[1]
            ljinux.io.ledset(3)
            if term.buf[0] is 9:  # kill
                term.focus = 0
                q = False
            elif term.buf[0] is 1 and not savee:  # save
                term.buf[1] = ""
                term.focus = 0
                term.move(x=sizee[0] - 2)
                spsz = (sizee[1] - 21) * " "
                stdout.write(
                    f"{colors.white_bg_black_bg}Save modified buffer?{spsz}{colors.endc}\n"
                )
                term.clear_line()
                stdout.write(f"{colors.white_bg_black_bg} Y{colors.endc} Yes\n")
                term.clear_line()
                stdout.write(
                    f"{colors.white_bg_black_bg} N{colors.endc} No        {toolsplit}{colors.white_bg_black_bg}^C{colors.endc} Cancel"
                )
                term.move(x=sizee[0] - 2, y=23)
                stdout.write(colors.white_bg_black_bg)
                del spsz
                savee += 1

            elif term.buf[0] is 8 and not savee:  # down
                term.focus = 0
                cl += 1
                if lc - 1 <= cl:
                    dataa.append("")
                    lc += 1
                if cl - vl > sizee[0] - 5:  # we are going out of screen
                    term.clear_line()
                    vl += 1
                    for i in range(2, sizee[0] - 2):  # shift data
                        term.move(x=i)
                        term.clear_line()
                        stdout.write(dataa[vl + i - 2])

            elif term.buf[0] is 2 and not savee:  # up
                term.focus = 0

                if cl > 0:
                    cl -= 1
                    if cl - vl < 0:
                        vl -= 1
                        for i in range(2, sizee[0] - 2):  # shift data
                            term.move(x=i, y=0)
                            term.clear_line()
                            stdout.write(dataa[vl + i - 2])

            elif term.buf[0] is 10:  # insert empty line (enter)
                if not savee:
                    dataa.append(dataa[lc - 1])  # last line to new line
                    noffs = 0
                    copyover = False
                    if len(term.buf[1]) == term.focus and len(term.buf[1]) is not 0:
                        noffs -= 1
                    elif term.focus is not 0:
                        copyover = True
                    else:
                        term.focus = 0
                    for i in range(
                        lc - 1, cl + 1 + noffs, -1
                    ):  # all lines from the end to here
                        dataa[i] = dataa[i - 1]
                    lc += 1
                    cl += 1
                    if copyover:
                        dataa[cl] = dataa[cl - 1][len(dataa[cl - 1]) - term.focus :]
                        dataa[cl - 1] = dataa[cl - 1][: len(dataa[cl - 1]) - term.focus]
                        term.buf[1] = dataa[cl]
                    elif not noffs:
                        dataa[cl] = ""
                        term.buf[1] = ""
                    else:
                        dataa[cl + noffs] = ""
                    del noffs, copyover

                    # shift data
                    tf = lc if not lc >= (sizee[0] - 3) else sizee[0] - 4

                    for i in range(0, tf):
                        term.move(x=i + 2)
                        term.clear_line()
                        stdout.write(dataa[vl + i])
                    del tf
                elif savee is 1:
                    # the "save y/n" prompt
                    if term.buf[1] in ["n", "N"]:
                        q = False  # abandon all hope (, ye who enter here)
                    elif term.buf[1] in ["y", "Y"]:
                        term.buf[1] = ""
                        term.focus = 0
                        savee += 1  # 2

                        # the "choose file name" prompt
                        term.move(x=sizee[0] - 2)

                        # show the file name suggested
                        term.clear_line()
                        stdout.write("File name to write:" + (" " * (sizee[1] - 19)))
                        term.move(x=sizee[0] - 1)
                        stdout.write(colors.endc)
                        term.clear_line()
                        term.move(x=sizee[0])
                        term.clear_line()
                        stdout.write(
                            f"{colors.white_bg_black_bg}^C{colors.endc} Cancel"
                        )
                        ffname = ""
                        try:
                            ffname = ljinux.based.user_vars["argj"].split()[1]
                        except IndexError:
                            pass
                        term.move(x=sizee[0] - 2, y=21)
                        stdout.write(colors.white_bg_black_bg)
                        term.buf[1] = ffname
                        term.focus = 0
                        del ffname
                    else:
                        stdout.write(
                            "\010" * len(term.buf[1])
                            + " " * len(term.buf[1])
                            + "\010" * len(term.buf[1])
                        )
                elif savee == 2:
                    try:
                        cc = True
                        cl1 = lc - 1
                        while cc:
                            if dataa[cl1].isspace() or dataa[cl1] == "":
                                dataa.pop()
                                cl1 -= 1
                            else:
                                cc = False
                        del cc, cl1
                        if not sdcard_fs:
                            remount("/", False)
                        with open(ljinux.api.betterpath(term.buf[1]), "w") as f:
                            for i in dataa:
                                f.write(f"{i}\n")
                            f.flush()
                        if not sdcard_fs:
                            remount("/", True)
                        q = False
                    except Exception as err:  # anything
                        nbottxt = f'[ Failed to save "{err}" ]'
                        term.move(x=sizee[0] - 2)
                        term.clear_line()
                        term.move(x=sizee[0] - 2, y=int((sizee[1] - len(nbottxt)) / 2))
                        stdout.write(colors.white_bg_black_bg + nbottxt + colors.endc)
                        del nbottxt
                        savee = 0
                        term.buf[1] = ""
                        term.focus = 0
                        term.move(x=sizee[0] - 1)
                        stdout.write(toolbar_txt)

            elif term.buf[0] is 0 and savee:  # Ctrl C, abort saving
                savee = 0
                term.focus = 0
                term.move(x=sizee[0] - 2)
                stdout.write(colors.endc + (" " * sizee[1]))
                term.move(x=sizee[0] - 1)
                stdout.write(toolbar_txt)

            elif term.buf[0] is 11:  # backspace
                if len(term.buf[1]) - term.focus > 0:
                    term.backspace()
                    if not savee:
                        dataa[cl] = term.buf[1]
                    else:
                        stdout.write(
                            "\010" * len(term.buf[1])
                            + " " * len(term.buf[1])
                            + "\010" * len(term.buf[1])
                        )
                elif not savee and cl > 0:
                    # don't do it when in save mode

                    # treat last line
                    if dataa[cl] != "":
                        dataa[cl - 1] += dataa[cl]

                    # backend shift
                    for i in range(cl, lc):
                        try:
                            dataa[i] = dataa[i + 1]
                        except IndexError:
                            break

                    dataa.pop()
                    lc -= 1
                    cl -= 1

                    # shift data
                    td = False  # to delete last line
                    tf = None  # range
                    magic = sizee[0] - 4
                    if lc > magic:
                        tf = magic
                    else:
                        tf = lc
                        if lc < magic:
                            # we have at least one empty from the weltext
                            td = True  # need to clear_line after line prints
                    for i in range(0, tf):
                        term.move(x=i + 2)
                        term.clear_line()
                        stdout.write(dataa[vl + i])
                    if td:
                        term.move(x=tf + 2)
                        term.clear_line()
                    del td, tf, magic

            elif term.buf[0] is 12:  # add tab
                term.stdin = " " * 4
            elif savee:
                # counter visual bug
                stdout.write(len(term.buf[1]) * "\010")

        except KeyboardInterrupt:
            pass

    del q, cl, vl, target, toolbar_txt, inb, toolsplit, filee, exists
    term.buf[1] = ""
    stdout.write(colors.endc)
    term.clear()
    term.trigger_dict = term_old

    del savee, dataa, term_old
    ljinux.based.user_vars["return"] = "0"
else:
    ljinux.based.error(13, "15x106")  # minimum size error
    ljinux.based.user_vars["return"] = "1"
