rename_process("rmdir")
vr("opts", ljinux.api.xarg())
if ("help" in vr("opts")["o"]) or ("h" in vr("opts")["o"]):
    ljinux.api.setvar("argj", "a /usr/share/help/rmdir.txt")
    ljinux.based.command.fpexec("/bin/cat.py")
    ljinux.api.setvar("return", "1")
else:
    if len(vr("opts")["w"]) > 0:
        for pv[get_pid()]["i"] in vr("opts")["w"]:
            if ljinux.api.isdir(vr("i")) == 1:
                vr("pr", ljinux.api.betterpath(vr("i")))
                if not len(listdir(vr("pr"))):
                    try:
                        if not vr("sdcard_fs", pid=0):
                            remount("/", False)
                        try:
                            rmdir(ljinux.api.betterpath(vr("pr")))
                        except OSError:
                            ljinux.based.error(4, vr("pr"), prefix="rmdir")
                        if not vr("sdcard_fs", pid=0):
                            remount("/", True)
                    except RuntimeError:
                        ljinux.based.error(7, prefix="rmdir")
                else:
                    ljinux.based.error(16, prefix="rmdir")
            else:
                ljinux.based.error(17, prefix="rmdir")
