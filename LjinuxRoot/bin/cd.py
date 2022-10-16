capdir = getcwd()
try:
    dirr = ljinux.based.user_vars["argj"].split()[1]
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
        "Error: '{}' Directory does not exist".format(
            ljinux.based.user_vars["argj"].split()[1]
        )
    )
except IndexError:
    pass
del capdir
