rename_process("rm")
pv[get_pid()]["opts"] = ljinux.api.xarg()
pv[get_pid()]["fw"] = pv[get_pid()]["opts"]["hw"] + pv[get_pid()]["opts"]["w"]

try:
    if not pv[0]["sdcard_fs"]:
        remount("/", False)

    for pv[get_pid()]["filee"] in pv[get_pid()]["fw"]:
        try:
            remove(ljinux.api.betterpath(pv[get_pid()]["filee"]))
        except OSError as errr:
            if str(pv[get_pid()]["errr"]) == "[Errno 2] No such file/directory":
                ljinux.based.error(4, f=pv[get_pid()]["filee"])
            elif str(pv[get_pid()]["errr"]) == "[Errno 21] EISDIR":
                ljinux.based.error(15, prefix="rm")
            else:
                ljinux.based.error(3)
            del errr

    try:
        if not pv[0]["sdcard_fs"]:
            remount("/", True)
    except RuntimeError:
        pass

except RuntimeError:
    ljinux.based.error(7)
