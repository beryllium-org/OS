try:
    f = open(ljinux.based.fn.betterpath(ljinux.based.user_vars["argj"].split()[1]), "r")
    f.close()
    ljinux.based.error(10)
except OSError:
    global sdcard_fs
    try:
        if not sdcard_fs:
            remount("/", False)
        f = open(ljinux.based.fn.betterpath(ljinux.based.user_vars["argj"].split()[1]), "w")
        f.close()
        if not sdcard_fs:
            remount("/", True)
    except RuntimeError:
        ljinux.based.error(7)
