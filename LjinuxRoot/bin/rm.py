rename_process("rm")
vr("opts", ljinux.api.xarg())
vr("fw", vr("opts")["hw"] + vr("opts")["w"])

try:
    if not pv[0]["sdcard_fs"]:
        remount("/", False)

    for pv[get_pid()]["filee"] in vr("fw"):
        try:
            remove(ljinux.api.betterpath(vr("filee")))
        except OSError as errr:
            if str(errr) == "[Errno 2] No such file/directory":
                ljinux.based.error(4, f=vr("filee"))
            elif str(errr) == "[Errno 21] EISDIR":
                ljinux.based.error(15, prefix="rm")
            else:
                ljinux.based.error(3)
            del errr

    if not pv[0]["sdcard_fs"]:
        remount("/", True)

except RuntimeError:
    ljinux.based.error(7)
