try:
    chdir(ljinux.based.fn.betterpath(ljinux.based.user_vars["argj"].split()[1]))
    ljinux.based.olddir = getcwd()
except OSError:
    print(
        "Error: '{}' Directory does not exist".format(
            ljinux.based.user_vars["argj"].split()[1]
        )
    )
except IndexError:
    pass
