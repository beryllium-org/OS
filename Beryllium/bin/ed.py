rename_process("ed")
gc.collect()
vr("opts", be.api.xarg())
vr("appending", False)
vr("has_checked_args", False)
vr("txbuf", [])
vr("selected", None)

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
    be.io.ledset(1)
    gc.collect()
    if vr("has_checked_args"):
        term.program()
    else:
        term.buf[0] = 0
    be.io.ledset(3)
    if term.buf[0] is 2:
        break
    elif term.buf[0] is 1:
        term.write("^C")
    elif term.buf[0] is 0:
        if vr("has_checked_args"):
            term.write()
        if vr("appending"):
            if term.buf[1] != ".":
                vra("txbuf", term.buf[1])
            else:
                vr("appending", False)
        else:
            vr("recv", term.buf[1].split(" "))
            if len(vr("recv")):
                if (vr("recv")[0] == "r") or (not vr("has_checked_args")):
                    vr("src", None)
                    if not vr("has_checked_args"):
                        vr("has_checked_args", True)
                        if len(vr("opts")["w"]) is not 0:
                            vr("src", vr("opts")["w"][0])
                    else:
                        if len(vr("recv")) > 1:
                            vr("src", vr("recv")[1])
                    if vr("src") is not None and (
                        vr("src").isspace() or vr("src") == ""
                    ):
                        vr("src", None)
                    if vr("src") is not None:
                        term.write("loading")
                        if be.api.isdir(vr("src"), getcwd()) is not 0:
                            vr("src", None)
                    if vr("src") is not None:
                        with be.api.fopen(vr("src")) as f:
                            vrp("txbuf", f.readlines())
                            vr("bl", 0)
                            for pv[get_pid()]["linen"] in range(len(vr("txbuf"))):
                                pv[get_pid()]["txbuf"][vr("linen")] = vr("txbuf")[
                                    vr("linen")
                                ][:-1]
                                vrp("bl", len(vr("txbuf")[vr("linen")]) + 1)
                                vrd("linen")
                        term.write(str(vr("bl")))
                        vrd("bl")
                    else:
                        term.write("?")
                    vrd("src")
                elif vr("recv")[0].isdigit():
                    vr("d", int(vr("recv")[0]))
                    if len(vr("txbuf")) >= vr("d"):
                        term.write(vr("txbuf")[vr("d") - 1])
                    vr("selected", vr("d"))
                    vrd("d")
                elif vr("recv")[0][0] == "s":
                    if vr("recv")[0][1] == "/" and vr("recv")[0][-1] == "/":
                        vr("slist", vr("recv")[0][2:-1].split("/"))
                        vr("sfinal", [])
                        vr("skip", 0)
                        if len(vr("slist")) is not 2:
                            for pv[get_pid()]["itemn"] in range(len(vr("slist"))):
                                if not vr("skip"):
                                    vr("cit", vr("slist")[vr("itemn")])
                                    while pv[get_pid()]["cit"].endswith("\\"):
                                        vrp("cit", "/")
                                        if vr("itemn") < len(vr("slist")) + vr("skip"):
                                            vrp(
                                                "cit",
                                                vr("slist")[
                                                    vr("itemn") + 1 + vr("skip")
                                                ],
                                            )
                                        vrp("skip")
                                    vra("sfinal", vr("cit"))
                                else:
                                    vrm("skip")
                            vrd("itemn")
                            vrd("cit")
                        else:
                            vr("sfinal", vr("slist"))
                        vrd("slist")
                        vrd("skip")
                        if (len(vr("sfinal")) is not 2) or (vr("selected") is None):
                            term.write("?")
                        else:
                            pv[get_pid()]["txbuf"][vr("selected") - 1] = vr("txbuf")[
                                vr("selected") - 1
                            ].replace(vr("sfinal")[0], vr("sfinal")[1])
                        vrd("sfinal")
                    else:
                        term.write("?")
                elif vr("recv")[0] == "c":
                    pv[get_pid()]["txbuf"].clear()
                elif vr("recv")[0] == "a":
                    vr("appending", True)
                elif vr("recv")[0] == "w":
                    if len(vr("recv")) > 1:
                        with be.api.fopen(vr("recv")[1], "w") as pv[get_pid()]["f"]:
                            if vr("f") is not None:
                                for pv[get_pid()]["line"] in vr("txbuf"):
                                    pv[get_pid()]["f"].write("{}\n".format(vr("line")))
                                    gc.collect()
                                vrd("line")
                            else:
                                term.write("?")
                    else:
                        term.write("?")
                elif vr("recv")[0] == "q":
                    if vr("selected") is not None:
                        vr("selected", None)
                        term.write("?")
                    else:
                        break
                elif vr("recv")[0] == ",p":
                    if len(vr("txbuf")):
                        for pv[get_pid()]["line"] in vr("txbuf"):
                            term.write(vr("line"))
                            vrd("line")
                    else:
                        term.write("?")
                else:
                    term.write("?")
            else:
                term.write("?")
            vrd("recv")
term.buf[1] = ""
