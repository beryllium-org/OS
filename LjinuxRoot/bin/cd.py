rename_process("cd")
vr("capdir", getcwd())
try:
    vr("dirr", ljinux.api.getvar("argj").split()[1])
    if vr("dirr") != "-":
        vr("dr", ljinux.api.isdir(vr("dirr")))
        if vr("dr") == 1:
            chdir(ljinux.api.betterpath(vr("dirr")))
            if vr("capdir") != getcwd():
                ljinux.api.setvar("prevdir", vr("capdir"))
        elif not vr("dr"):
            ljinux.based.error(14, "cd")
        else:
            ljinux.based.error(17, "cd")
    else:
        chdir(ljinux.based.user_vars["prevdir"])
        ljinux.api.setvar("prevdir", vr("capdir"))
    ljinux.based.olddir = getcwd()
except IndexError:
    pass
