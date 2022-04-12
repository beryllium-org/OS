try:
    chdir(ljinux.based.user_vars["argj"].split()[1])
except OSError:
    print(
        "Error: '{}' Directory does not exist".format(
            ljinux.based.user_vars["argj"].split()[1]
        )
    )
except IndexError:
    pass
