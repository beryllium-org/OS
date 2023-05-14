global sdcard_fs
opts = ljinux.api.xarg()
if ("help" in opts["o"]) or ("h" in opts["o"]):
    ljinux.api.setvar("argj", "a /usr/share/help/rmdir.txt")
    ljinux.based.command.fpexec("/bin/cat.py")
    ljinux.api.setvar("return", "1")
else:
    if len(opts["w"]) > 0:
        for i in opts["w"]:
            if ljinux.api.isdir(i) == 1:
                pr = ljinux.api.betterpath(i)
                if not len(listdir(pr)):
                    try:
                        if not sdcard_fs:
                            remount("/", False)
                        try:
                            rmdir(ljinux.api.betterpath(pr))
                        except OSError:
                            ljinux.based.error(4, "not done", prefix="rmdir")
                        if not sdcard_fs:
                            remount("/", True)
                    except RuntimeError:
                        ljinux.based.error(7, prefix="rmdir")
                else:
                    ljinux.based.error(16, prefix="rmdir")
                del pr
            else:
                ljinux.based.error(17, prefix="rmdir")
            del i
del opts
