rename_process("alias")
try:
    vr("inpt", ljinux.based.user_vars["argj"].split())
    vr("eqpos", vr("inpt")[1].find("=", 0))
    vr("cmd", vr("inpt")[1][: vr("eqpos")])
    vr("alcmd", vr("inpt")[1][vr("eqpos") + 1 :])
    vr("offs", 1)
    if vr("alcmd").startswith('"'):
        vr("alcmd", vr("alcmd")[1:])
        while not vr("alcmd").endswith('"'):
            pv[get_pid()]["offs"] += 1
            pv[get_pid()]["alcmd"] += " " + vr("inpt")[vr("offs")]
        vr("alcmd", vr("alcmd")[:-1])
    else:
        raise IndexError
    ljinux.based.alias_dict[vr("cmd")] = vr("alcmd")
    ljinux.api.setvar("return", "0")
except IndexError:
    ljinux.based.error(1)
    ljinux.api.setvar("return", "1")
