capdir = getcwd()
try:
    dirr = ljinux.api.getvar("argj").split()[1]
    if dirr != "-":
        chdir(ljinux.api.betterpath(dirr))
        if capdir != getcwd():
            ljinux.based.user_vars["prevdir"] = capdir
    else:
        chdir(ljinux.based.user_vars["prevdir"])
    ljinux.based.olddir = getcwd()
    del dirr
except OSError:
    print(
        "Error: '" + ljinux.api.getvar("argj").split()[1] + "' Directory does not exist"
    )
except IndexError:
    pass
del capdir
