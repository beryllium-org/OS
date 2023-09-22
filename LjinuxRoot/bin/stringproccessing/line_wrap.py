rename_process("line_wrap")
vr("l", pv[get_parent_pid()]["lines"])
vr("lines", [], pid=get_parent_pid())
vr("sizee", term.detect_size(3))
for pv[get_pid()]["i"] in vr("l"):
    vr("rem", vr("i"))
    if vr("rem") != "":
        while len(vr("rem")):
            if len(vr("rem")) > vr("sizee")[1]:
                vra("lines", vr("rem")[: vr("sizee")[1]], pid=get_parent_pid())
                vr("rem", vr("rem")[vr("sizee")[1] :])
            else:
                vra("lines", vr("rem"), pid=get_parent_pid())
                vr("rem", "")
    else:
        vra("lines", vr("rem"), pid=get_parent_pid())
