args = ljinux.based.user_vars["argj"].split()[1:]
argl = len(args)
if argl > 1 and args[0] == "decompress":
    from jz import decompress

    zname = args[1]
    unzpath = "." if argl is 2 else args[2]
    if not sdcard_fs:
        remount("/", False)
    decompress(zname, unzpath)
    if not sdcard_fs:
        remount("/", True)
    del decompress, zname, unzpath
elif argl > 0 and args[0] == "compress":
    print("Compression not yet supported on-board")
else:
    ljinux.based.error(1)
    ljinux.based.user_vars["return"] = "1"

del args, argl
