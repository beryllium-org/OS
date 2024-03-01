rename_process("rmdir")
vr("opts", be.api.xarg())
if ("help" in vr("opts")["o"]) or ("h" in vr("opts")["o"]):
    be.api.setvar("argj", "a /usr/share/help/rmdir.txt")
    be.based.command.fpexec("/bin/cat.py")
    be.api.setvar("return", "1")
else:
    if len(vr("opts")["w"]) > 0:
        for pv[get_pid()]["i"] in vr("opts")["w"]:
            if be.api.isdir(vr("i")) == 1:
                vr("pr", be.api.betterpath(vr("i")))
                if not len(listdir(vr("pr"))):
                    try:
                        if not vr("sdcard_fs", pid=0):
                            remount("/", False)
                        try:
                            rmdir(be.api.betterpath(vr("pr")))
                        except OSError:
                            be.based.error(4, vr("pr"), prefix="rmdir")
                        if not vr("sdcard_fs", pid=0):
                            remount("/", True)
                    except RuntimeError:
                        be.based.error(7, prefix="rmdir")
                else:
                    be.based.error(16, prefix="rmdir")
            else:
                be.based.error(17, prefix="rmdir")
