rename_process("cat")
vr("inpt", ljinux.based.user_vars["argj"].split())

try:
    with ljinux.api.fopen(vr("inpt")[1], "r") as pv[get_pid()]["f"]:
        for pv[get_pid()]["line"] in vr("f"):
            term.nwrite(vr("line"))
            vrd("line")
    ljinux.api.setvar("return", "0")

except OSError:
    ljinux.based.error(4, vr("inpt")[1])
    ljinux.api.setvar("return", "1")

except IndexError:
    ljinux.based.error(1)
    ljinux.api.setvar("return", "1")
