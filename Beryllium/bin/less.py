rename_process("less")
vr("opts", be.api.xarg())
be.api.setvar("return", "1")
if len(vr("opts")["w"]):
    with be.api.fopen(vr("opts")["w"][0]) as pv[get_pid()]["f"]:
        if vr("f") is not None:
            vr("lines_tmp", vr("f").readlines())

            vr("lines", [])
            for pv[get_pid()]["i"] in vr("lines_tmp"):
                vra(
                    "lines",
                    pv[get_pid()]["i"].replace("\n", "")
                    if pv[get_pid()]["i"] != "\n"
                    else pv[get_pid()]["i"],
                )
            vrd("lines_tmp")
            be.based.command.fpexec(
                pv[0]["root"] + "/bin/stringproccessing/line_wrap.py"
            )
            # Now our lines have been formatted

            vr("sizee", term.detect_size())

            term.trigger_dict = {
                "ctrlC": 1,
                "q": 1,
                "up": 2,
                "down": 3,
                "pgup": 4,
                "pgdw": 5,
                "home": 6,
                "end": 7,
                "rest": "ignore",
                "echo": "none",
            }

            vr("lc", len(vr("lines")))
            vr(
                "target",
                (vr("sizee")[0] - 1) if (vr("lc") > vr("sizee")[0] - 1) else vr("lc"),
            )  # no of lines per screen
            vr("pos", 0)  # scroll offset
            vr("ctl", [0, None])
            vr("endt", " (END)")
            vr("carry", "\n")

            term.clear()
            while vr("ctl")[0] != 1:
                term.trigger_dict["prefix"] = "{}lines {}-{}/{} {}%{}{}".format(
                    colors.white_bg_black_bg,
                    vr("pos"),
                    vr("target") + vr("pos"),
                    vr("lc"),
                    int(float(vr("target") + vr("pos")) * 100 / float(vr("lc"))),
                    vr("endt") if vr("pos") == vr("lc") - vr("target") else "",
                    colors.endc,
                )
                for pv[get_pid()]["i"] in range(0, vr("target")):
                    vr("l", vr("lines")[vr("i") + vr("pos")])
                    term.nwrite(
                        vr("l") + (vr("carry") if vr("l") != vr("carry") else "")
                    )
                vr("ctl", term.program())
                if vr("ctl")[0] == 2:
                    if vr("pos"):
                        pv[get_pid()]["pos"] -= 1
                elif vr("ctl")[0] == 3:
                    if vr("pos") < vr("lc") - vr("target"):
                        pv[get_pid()]["pos"] += 1
                elif vr("ctl")[0] == 4:
                    if vr("pos") > vr("target"):
                        pv[get_pid()]["pos"] -= vr("target")
                    else:
                        vr("pos", 0)
                elif vr("ctl")[0] == 5:
                    if vr("pos") < vr("lc") - 2 * vr("target"):
                        pv[get_pid()]["pos"] += vr("target")
                    else:
                        vr("pos", vr("lc") - vr("target"))
                elif vr("ctl")[0] == 6:
                    vr("pos", 0)  # ez -- blade 2020
                elif vr("ctl")[0] == 7:
                    vr("pos", vr("lc") - vr("target"))
                term.clear()
                be.api.setvar("return", "0")
        else:
            be.based.error(4, be.based.user_vars["argj"].split()[1])
else:
    be.based.error(1)
