rename_process("rmdir")
pv[get_pid()]["opts"] = ljinux.api.xarg()
if ("help" in pv[get_pid()]["opts"]["o"]) or ("h" in pv[get_pid()]["opts"]["o"]):
    ljinux.api.setvar("argj", "a /usr/share/help/rmdir.txt")
    ljinux.based.command.fpexec("/bin/cat.py")
    ljinux.api.setvar("return", "1")
else:
    if len(pv[get_pid()]["opts"]["w"]) > 0:
        for pv[get_pid()]["i"] in pv[get_pid()]["opts"]["w"]:
            if ljinux.api.isdir(pv[get_pid()]["i"]) == 1:
                pv[get_pid()]["pr"] = ljinux.api.betterpath(pv[get_pid()]["i"])
                if not len(listdir(pv[get_pid()]["pr"])):
                    try:
                        if not pv[0]["sdcard_fs"]:
                            remount("/", False)
                        try:
                            rmdir(ljinux.api.betterpath(pv[get_pid()]["pr"]))
                        except OSError:
                            ljinux.based.error(4, "not done", prefix="rmdir")
                        if not pv[0]["sdcard_fs"]:
                            remount("/", True)
                    except RuntimeError:
                        ljinux.based.error(7, prefix="rmdir")
                else:
                    ljinux.based.error(16, prefix="rmdir")
            else:
                ljinux.based.error(17, prefix="rmdir")
