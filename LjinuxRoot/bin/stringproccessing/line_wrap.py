rename_process("line_wrap")
vr("l", pv[get_parent_pid()]["lines"])
vr("lines", [], pid=get_parent_pid())
vr("sizee", term.detect_size())
for pv[get_pid()]["i"] in vr("l"):
    vr("rem", vr("i"))
    if vr("rem") != "":
        while len(vr("rem")):
            if len(vr("rem")) > vr("sizee")[1]:
                pv[get_parent_pid()]["lines"].append(vr("rem")[: vr("sizee")[1]])
                vr("rem", vr("rem")[vr("sizee")[1] :])
            else:
                pv[get_parent_pid()]["lines"].append(vr("rem"))
                vr("rem", "")
    else:
        pv[get_parent_pid()]["lines"].append(vr("rem"))
