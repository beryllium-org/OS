args = ljinux.based.user_vars["argj"].split()
if "network" in ljinux.modules and ljinux.modules["network"].connected:
    try:
        global sdcard_fs
        if not sdcard_fs:
            remount("/", False)
        try:
            with ljinux.based.fn.fopen(args[2], "wb") as filee:
                filee.write(ljinux.modules["network"].get(args[1]).content)
            ljinux.modules["network"].resetsock()
        except IndexError:
            ljinux.based.error(9)
        if not sdcard_fs:
            remount("/", True)
    except RuntimeError:
        ljinux.based.error(7)
else:
    ljinux.based.error(5)
del args
