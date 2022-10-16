opts = ljinux.api.xarg()
li = opts["hw"] + opts["w"]
quiett = ljinux.based.silent or "q" in opts["o"]
jzdebug = "debug" in opts["o"]

if ("d" in opts["o"] or "decompress" in opts["o"]) and len(li) > 0:
    from jz import decompress

    zname = li[0]
    unzpath = "." if len(li) < 2 else li[1]
    if not unzpath.endswith("/"):
        unzpath += "/"
    if not sdcard_fs:
        remount("/", False)
    decompress(zname, ljinux.api.betterpath(unzpath), quiet=quiett, debug=jzdebug)
    if not sdcard_fs:
        remount("/", True)
    del decompress, zname, unzpath
    ljinux.based.user_vars["return"] = "0"
elif "c" in opts["o"] or "compress" in opts["o"]:
    print("Compression not yet supported on-board")
    ljinux.based.user_vars["return"] = "0"
else:
    ljinux.based.error(1)
    ljinux.based.user_vars["return"] = "1"

del opts, quiett, li, jzdebug
