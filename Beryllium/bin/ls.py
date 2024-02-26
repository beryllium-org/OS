rename_process("ls")
vr("opts", be.api.xarg())
vr("li", vr("opts")["hw"] + vr("opts")["w"])
vr("co", "".join(vr("opts")["o"]))

vr("sps", "   ")
vr("path", "./")

if len(vr("li")):
    vr("path", vr("li")[0])

try:
    vr("ls", be.api.listdir(vr("path")))
    vrd("opts")
    if "l" in vr("co"):
        vr("sps", "\n")

    vr("cnt", len(vr("ls")))
    if "a" not in vr("co"):
        vr("ls2", [])
        for pv[get_pid()]["i"] in range(vr("cnt")):
            vr("fdat", vr("ls")[vr("i")])
            if vr("fdat")[0][0] != ".":
                vra("ls2", vr("fdat"))
        vrd("ls")
        vr("ls", vr("ls2"))
        vrd("ls2")
        vr("cnt", len(vr("ls")))

    if "l" in vr("co"):
        term.write("total " + str(vr("cnt") + (2 if "a" in vr("co") else 0)))
        vr(
            "pmap",
            {
                0: "---",
                1: "--x",
                2: "-w-",
                3: "-wx",
                4: "r--",
                5: "r-x",
                6: "rw-",
                7: "rwx",
            },
        )
        vr(
            "mdict",
            {
                1: "Jan",
                2: "Feb",
                3: "Mar",
                4: "Apr",
                5: "May",
                6: "Jun",
                7: "Jul",
                8: "Aug",
                9: "Sep",
                10: "Oct",
                11: "Nov",
                12: "Dec",
            },
        )

    if "a" in vr("co"):
        term.write(colors.okcyan + "." + colors.endc, end=vr("sps"))
        if not (vr("path") == "/" or (vr("path") == "./" and getcwd() == "/")):
            term.write(colors.okcyan + ".." + colors.endc, end=vr("sps"))
    vrd("path")

    for pv[get_pid()]["i"] in range(vr("cnt")):
        vr("col", "")
        vr("fdat", vr("ls")[vr("i")])
        if vr:
            if vr("fdat")[1] == "f":
                pass
            elif vr("fdat")[1] == "d":
                vr("col", colors.okcyan)
            elif vr("fdat")[1] == "c":
                vr("col", colors.yellow_t)
            else:
                vr("col", colors.red_t)
            if vr("fdat")[0][0] == "." and "a" not in vr("co"):
                continue
            else:
                if "l" in vr("co"):
                    vr("type", vr("fdat")[1])
                    if vr("type") == "f":
                        vr("type", "-")
                    term.nwrite(vr("type"))
                    for pv[get_pid()]["j"] in range(3):
                        term.nwrite(vr("pmap")[vr("fdat")[2][vr("j")]])
                    term.nwrite(
                        " "
                        + str(int(vr("type") == "d") + 1)
                        + " "
                        + vr("fdat")[5]
                        + " "
                        + vr("fdat")[6]
                        + " "
                    )
                    if "h" in vr("co"):
                        pass
                    else:
                        term.nwrite(
                            " " * (7 - len(str(vr("fdat")[3])))
                            + str(vr("fdat")[3])
                            + " "
                        )
                    vr("modtime", vr("fdat")[4])
                    term.nwrite(
                        vr("mdict")[vr("modtime").tm_mon]
                        + " "
                        + (" " if vr("modtime").tm_mday < 10 else "")
                        + str(vr("modtime")[2])
                        + " "
                        + ("0" if vr("modtime").tm_hour < 10 else "")
                        + str(vr("modtime")[3])
                        + ":"
                        + ("0" if vr("modtime").tm_min < 10 else "")
                        + str(vr("modtime")[4])
                        + " "
                    )
                term.write(
                    vr("col") + vr("fdat")[0] + colors.endc,
                    end=vr("sps"),
                )

    if (not "l" in vr("co")) and vr("cnt"):
        term.write()
    be.api.setvar("return", "0")
except OSError:
    be.based.error(17, prefix=f"{colors.blue_t}ls{colors.endc}")
    be.api.setvar("return", "1")
