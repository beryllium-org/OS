opts = ljinux.api.xarg()
fw = opts["hw"] + opts["w"]

try:
    if not sdcard_fs:
        remount("/", False)

    for filee in fw:
        try:
            remove(ljinux.api.betterpath(filee))
        except OSError as errr:
            if str(errr) == "[Errno 2] No such file/directory":
                ljinux.based.error(4, f=filee)
            elif str(errr) == "[Errno 21] EISDIR":
                ljinux.based.error(15, prefix="rm")
            else:
                ljinux.based.error(3)
            del filee

    try:
        if not sdcard_fs:
            remount("/", True)
    except RuntimeError:
        pass

except RuntimeError:
    ljinux.based.error(7)

del opts, fw
