gc.collect()
opts = ljinux.api.xarg()
appending = False
has_checked_args = False
txbuf = list()
sps = " "
empt = ""
qu = "?"
r = "r"
w = "w"
q = "q"
sl = "/"
bsl = "\\"
selected = None

oldtr = dict()
oldtr.update(term.trigger_dict)
term.trigger_dict.clear()
term.trigger_dict.update(
    {
        "prefix": empt,
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
    term.buf[1] = empt
    term.focus = 0
    ljinux.io.ledset(1)
    gc.collect()
    if has_checked_args:
        term.program()
    else:
        term.buf[0] = 0
    ljinux.io.ledset(3)
    if term.buf[0] is 2:
        break
    elif term.buf[0] is 1:
        term.write("^C")
    elif term.buf[0] is 0:
        if has_checked_args:
            term.write()
        if appending:
            if term.buf[1] != ".":
                txbuf.append(term.buf[1])
            else:
                appending = False
        else:
            recv = term.buf[1].split(sps)
            if len(recv):
                if (recv[0] == r) or (not has_checked_args):
                    src = None
                    if not has_checked_args:
                        has_checked_args = True
                        if len(opts[w]) is not 0:
                            src = opts[w][0]
                    else:
                        if len(recv) > 1:
                            src = recv[1]
                    if src is not None and (src.isspace() or src == ""):
                        src = None
                    if src is not None:
                        if ljinux.api.isdir(src, getcwd()) is not 0:
                            src = None
                    if src is not None:
                        with ljinux.api.fopen(src) as f:
                            txbuf += f.readlines()
                            bl = 0
                            for linen in range(len(txbuf)):
                                txbuf[linen] = txbuf[linen][:-1]
                                bl += len(txbuf[linen]) + 1
                                del linen
                        term.write(str(bl))
                        del bl
                    else:
                        term.write(qu)
                    del src
                elif recv[0].isdigit():
                    d = int(recv[0])
                    if len(txbuf) >= d:
                        term.write(txbuf[d - 1])
                    selected = d
                    del d
                elif recv[0][0] == "s":
                    if recv[0][1] == sl and recv[0][-1] == sl:
                        slist = recv[0][2:-1].split(sl)
                        sfinal = list()
                        skip = 0
                        if len(slist) is not 2:
                            for itemn in range(len(slist)):
                                if not skip:
                                    cit = slist[itemn]
                                    while cit.endswith(bsl):
                                        cit += "/"
                                        if itemn < len(slist) + skip:
                                            cit += slist[itemn + 1 + skip]
                                        skip += 1
                                    sfinal.append(cit)
                                    del itemn, cit
                                else:
                                    skip -= 1
                        else:
                            sfinal = slist
                        del slist, skip
                        if (len(sfinal) is not 2) or (selected is None):
                            term.write(qu)
                        else:
                            txbuf[selected - 1] = txbuf[selected - 1].replace(
                                sfinal[0], sfinal[1]
                            )
                        del sfinal
                    else:
                        term.write(qu)
                elif recv[0] == "c":
                    txbuf.clear()
                elif recv[0] == "a":
                    appending = True
                elif recv[0] == w:
                    if len(recv) > 1:
                        with ljinux.api.fopen(recv[1], "w") as f:
                            if f is not None:
                                for line in txbuf:
                                    f.write(f"{line}\n")
                                    del line
                                    gc.collect()
                            else:
                                term.write(qu)
                    else:
                        term.write(qu)
                elif recv[0] == q:
                    if selected is not None:
                        selected = None
                        term.write(qu)
                    else:
                        break
                elif recv[0] == ",p":
                    if len(txbuf):
                        for line in txbuf:
                            term.write(line)
                            del line
                    else:
                        term.write(qu)
                else:
                    term.write(qu)
            else:
                term.write(qu)
            del recv

term.buf[1] = empt
term.trigger_dict.clear()
term.trigger_dict.update(oldtr)
del oldtr, appending, has_checked_args, txbuf, sps, empt, qu, q, r, w, selected, sl, bsl
