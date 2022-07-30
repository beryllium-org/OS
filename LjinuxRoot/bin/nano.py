ljinux.io.ledset(1)  # we don't want to pretend activity
sizee = term.detect_size()
if sizee[0] > 14 and sizee[1] > 102:
    filee = None
    exists = 2
    weltxt = "[ Welcome to nano.  For basic help, type Ctrl+G. ]"

    versionn = "0.1"

    try:
        filee = ljinux.based.fn.betterpath(ljinux.based.user_vars["argj"].split()[1])
    except IndexError:
        pass

    if filee is not None:  # there is arg
        exists = ljinux.based.fn.isdir(filee, rdir=getcwd())

    if exists == 1:  # it is dir
        filee = None
        exists = 2
        weltxt = "[ {} is a directory ]".format(filee[filee.rfind("/") + 1 :])

    dataa = [""]

    lc = 0  # line count
    if exists == 0:  # is file
        with open(filee, "r") as f:
            ll = f.readlines()
            ljinux.based.user_vars["input"] = []
            for i in range(0, len(ll)):
                if ll[i] != "\n":
                    ljinux.based.user_vars["input"].append(ll[i].replace("\n", ""))
                else:
                    ljinux.based.user_vars["input"].append("")
            del ll

        ljinux.based.command.fpexecc(
            [None, "-n", "/LjinuxRoot/bin/stringproccessing/line_wrap.py"]
        )
        del ljinux.based.user_vars["input"]
        dataa = ljinux.based.user_vars["output"]
        del ljinux.based.user_vars["output"]

    term_old = term.trigger_dict
    term.trigger_dict = {
        "ctrlX": 1,
        "ctrlK": 9,
        "ctrlC": 0,
        "up": 2,
        "down": 8,
        "pgup": 4,
        "pgdw": 5,
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
    ctl = [0, None]
    fnam = "New buffer" if exists == 2 else filee[filee.rfind("/") + 1 :]
    spz = int((sizee[1] - 11 - len(versionn) - len(fnam)) / 2)
    sps1 = " " * (spz - 5)
    sps2 = " " * (spz + 6)
    del spz, filee

    toptxt = f"{colors.white_bg_black_bg}  LNL nano {versionn}{sps1}{fnam}{sps2}{colors.endc}\n"
    del versionn, sps1, sps2, fnam

    bottxt = f"{colors.white_bg_black_bg}{weltxt}{colors.endc}\n"
    bottxt_offs = int((sizee[1] - len(weltxt)) / 2)
    del weltxt

    toolsplit = " " * int(sizee[1] / 8 - 13)
    toolbar_txt = f"""{colors.white_bg_black_bg}^G{colors.endc} Help      {toolsplit}{colors.white_bg_black_bg}^O{colors.endc} Write Out {toolsplit}{colors.white_bg_black_bg}^W{colors.endc} Where Is  {toolsplit}{colors.white_bg_black_bg}^K{colors.endc} Cut       {toolsplit}{colors.white_bg_black_bg}^T{colors.endc} Execute   {toolsplit}{colors.white_bg_black_bg}^C{colors.endc} Location  {toolsplit}{colors.white_bg_black_bg}M-U{colors.endc} Undo     {toolsplit}{colors.white_bg_black_bg}M-A{colors.endc} Set Mark
{colors.white_bg_black_bg}^X{colors.endc} Exit      {toolsplit}{colors.white_bg_black_bg}^R{colors.endc} Read File {toolsplit}{colors.white_bg_black_bg}^\\{colors.endc} Replace   {toolsplit}{colors.white_bg_black_bg}^U{colors.endc} Paste     {toolsplit}{colors.white_bg_black_bg}^J{colors.endc} Justify   {toolsplit}{colors.white_bg_black_bg}^_{colors.endc} Go To Line{toolsplit}{colors.white_bg_black_bg}M-E{colors.endc} Redo     {toolsplit}{colors.white_bg_black_bg}M-6{colors.endc} Copy"""  # the big ugly static string
    del toolsplit

    # while ctl[0] != 1:
    q = True
    inb = False  # in bottom box
    bmod = None  # 0 == saving, 1 == searching, more planned later
    savee = False
    term.clear()
    stdout.write(toptxt)
    term.move(x=sizee[0] - 2, y=bottxt_offs)
    stdout.write(bottxt)
    stdout.write(toolbar_txt)
    if len(dataa) > 1:
        ltd = (sizee[0] - 4) if (sizee[0] - 4) < len(dataa) else len(dataa)
        for i in range(2, sizee[0] - 2):
            term.move(x=i, y=0)
            stdout.write(dataa[i - 2])
    while q:
        try:
            term.focus = 0
            term.buf[1] = dataa[cl]
            term.move(x=cl - vl + 2, y=len(term.buf[1]))
            term.clear_line()
            ljinux.io.ledset(1)
            ctl = term.program()
            ljinux.io.ledset(3)
            if ctl[0] == 9:  # kill
                q = False
            elif ctl[0] == 1:  # save
                pass
            elif ctl[0] == 8:  # down
                dataa[cl] = term.buf[1]
                cl += 1
                if lc < cl:
                    dataa.append("")
                    lc += 1
                if cl - vl > sizee[0] - 6:  # we are going out of screen
                    term.clear_line()
                    vl += 1
                    for i in range(2, sizee[0] - 3):  # shift data
                        term.move(x=i, y=0)
                        term.clear_line()
                        stdout.write(dataa[vl + i - 2])

            elif ctl[0] == 2:  # up
                term.focus = 0
                dataa[cl] = term.buf[1]
                if cl > 0:
                    cl -= 1
                    if cl - vl < 0:
                        vl -= 1
                        for i in range(2, sizee[0] - 2):  # shift data
                            term.move(x=i, y=0)
                            term.clear_line()
                            stdout.write(dataa[vl + i - 2])

            elif ctl[0] == 10:  # insert empty line (enter)
                term.focus = 0
                dataa[cl] = term.buf[1]
                dataa.append(lc)  # last line to new line
                for i in range(lc, cl + 1):  # all lines from the end to here
                    dataa[i] = dataa[i - 1]
                dataa[cl] = ""
                term.buf[1] = ""
        except KeyboardInterrupt:
            pass

    del q, ctl, cl, vl, target, toptxt, bottxt, bottxt_offs, toolbar_txt, inb
    term.clear()
    term.buf[1] = ""
    term.trigger_dict = term_old
    del term_old

    del savee
    ljinux.based.user_vars["return"] = "0"
else:
    ljinux.based.error(13, "15x102")  # minimum size error
    ljinux.based.user_vars["return"] = "1"
