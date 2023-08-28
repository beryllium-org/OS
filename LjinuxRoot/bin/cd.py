rename_process("cd")
vr("capdir", getcwd())
try:
    vr("dirr", ljinux.api.getvar("argj").split()[1])
    if vr("dirr") != "-":
        chdir(ljinux.api.betterpath(vr("dirr")))
        if vr("capdir") != getcwd():
            ljinux.based.user_vars["prevdir"] = vr("capdir")
    else:
        chdir(ljinux.based.user_vars["prevdir"])
    ljinux.based.olddir = getcwd()
except OSError:
    term.write(
        "Error: '" + ljinux.api.getvar("argj").split()[1] + "' Directory does not exist"
    )
except IndexError:
    pass
