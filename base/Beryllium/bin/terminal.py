rename_process("terminal")
vr("opts", be.api.xarg())
be.api.setvar("return", "1")
if "help" in vr("opts")["o"] or "-h" in vr("opts")["o"] or not vr("opts")["w"]:
    term.write("Usage: terminal [get/list/activate] [ttyXXXX]")
else:
    vr("0", vr("opts")["w"][0])
    if vr("0") == "get":
        be.api.setvar("return", pv[0]["console_active"])
    elif vr("0") == "activate":
        if len(vr("opts")["w"]) - 1:
            vr("1", vr("opts")["w"][1])
            if vr("1") in pv[0]["consoles"]:
                term.console = pv[0]["consoles"][vr("opts")["w"][1]]
                pv[0]["console_active"] = vr("opts")["w"][1]
                be.api.setvar("return", "0")
            else:
                term.write("Console not found.")
        else:
            term.write("No console specified!")
    elif vr("0") == "list":
        for pv[get_pid()]["i"] in pv[0]["consoles"].keys():
            term.nwrite(vr("i"))
            if vr("i") == pv[0]["console_active"]:
                term.write(" [ACTIVE]")
            else:
                term.write()
        be.api.setvar("return", "0")
    else:
        term.write("Unknown option specified, try running `terminal --help`")
