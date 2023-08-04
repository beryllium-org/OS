rename_process("mkdir")
try:
    vr("wd", ljinux.api.betterpath(ljinux.based.user_vars["argj"].split()[1]))
    if ljinux.api.isdir(vr("wd")) == 2:
        if not vr("sdcard_fs", pid=0):
            remount("/", False)
        if ljinux.api.isdir(vr("wd")[: vr("wd").rfind("/")]) == 2:
            vr("fpaths", vr("wd")[: vr("wd").find("/") + 1])
            vr("wd", vr("wd")[vr("wd").find("/") + 1 :])
            while vr("wd").find("/") != -1:
                pv[get_pid()]["fpaths"] += vr("wd")[: vr("wd").find("/") + 1]
                vr("wd", vr("wd")[vr("wd").find("/") + 1 :])
                if ljinux.api.isdir(vr("fpaths")) == 2:
                    mkdir(vr("fpaths"))
            vr("wd", vr("fpaths") + vr("wd"))
        mkdir(vr("wd"))
        if not vr("sdcard_fs", pid=0):
            remount("/", True)
        ljinux.api.setvar("return", "0")
    else:
        raise OSError
except OSError:
    term.write(
        "mkdir: cannot create directory ‘"
        + ljinux.based.user_vars["argj"].split()[1]
        + "’: File exists"
    )
    ljinux.api.setvar("return", "1")
except RuntimeError:
    ljinux.based.error(7)
    ljinux.api.setvar("return", "1")
except IndexError:
    ljinux.based.error(1)
    ljinux.api.setvar("return", "1")
