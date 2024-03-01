rename_process("rm")
vr("opts", be.api.xarg())
vr("fw", vr("opts")["hw"] + vr("opts")["w"])

try:
    if not pv[0]["sdcard_fs"]:
        remount("/", False)

    for pv[get_pid()]["filee"] in vr("fw"):
        try:
            vr("fname", be.api.betterpath(vr("filee")))
            remove(vr("fname"))
            if vr("fname") in be.code_cache:
                be.code_cache.pop(vr("fname"))
        except OSError as errr:
            if str(errr) == "[Errno 2] No such file/directory":
                be.based.error(4, f=vr("filee"))
            elif str(errr) == "[Errno 21] EISDIR":
                be.based.error(15, prefix="rm")
            else:
                be.based.error(3)
            del errr

    if not pv[0]["sdcard_fs"]:
        remount("/", True)

except RuntimeError:
    be.based.error(7)
