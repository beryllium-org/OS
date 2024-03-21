rename_process("cat")
vr("inpt", be.based.user_vars["argj"].split())

try:
    with be.api.fs.open(vr("inpt")[1], "r") as pv[get_pid()]["f"]:
        if vr("f") is None:
            be.based.error(4, vr("inpt")[1])
            be.api.setvar("return", "1")
        else:
            for pv[get_pid()]["line"] in vr("f"):
                term.nwrite(vr("line"))
            vrd("line")
            be.api.setvar("return", "0")
except IndexError:
    be.based.error(1)
    be.api.setvar("return", "1")
