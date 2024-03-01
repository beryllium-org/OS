rename_process("mkdir")
try:
    vr("wd", be.api.betterpath(be.based.user_vars["argj"].split()[1]))
    if be.api.isdir(vr("wd")) == 2:
        if not vr("sdcard_fs", pid=0):
            remount("/", False)
        if be.api.isdir(vr("wd")[: vr("wd").rfind("/")]) == 2:
            vr("fpaths", vr("wd")[: vr("wd").find("/") + 1])
            vr("wd", vr("wd")[vr("wd").find("/") + 1 :])
            while vr("wd").find("/") != -1:
                pv[get_pid()]["fpaths"] += vr("wd")[: vr("wd").find("/") + 1]
                vr("wd", vr("wd")[vr("wd").find("/") + 1 :])
                if be.api.isdir(vr("fpaths")) == 2:
                    mkdir(vr("fpaths"))
            vr("wd", vr("fpaths") + vr("wd"))
        mkdir(vr("wd"))
        if not vr("sdcard_fs", pid=0):
            remount("/", True)
        be.api.setvar("return", "0")
    else:
        raise OSError
except OSError:
    term.write(
        "mkdir: cannot create directory ‘"
        + be.based.user_vars["argj"].split()[1]
        + "’: File exists"
    )
    be.api.setvar("return", "1")
except RuntimeError:
    be.based.error(7)
    be.api.setvar("return", "1")
except IndexError:
    be.based.error(1)
    be.api.setvar("return", "1")
