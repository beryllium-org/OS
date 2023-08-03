rename_process("jz")
pv[get_pid()]["opts"] = ljinux.api.xarg()
pv[get_pid()]["li"] = pv[get_pid()]["opts"]["hw"] + pv[get_pid()]["opts"]["w"]
pv[get_pid()]["quiett"] = ljinux.based.silent or "q" in pv[get_pid()]["opts"]["o"]
pv[get_pid()]["jzdebug"] = "debug" in pv[get_pid()]["opts"]["o"]

if (
    "d" in pv[get_pid()]["opts"]["o"] or "decompress" in pv[get_pid()]["opts"]["o"]
) and len(pv[get_pid()]["li"]) > 0:
    from jz import decompress

    pv[get_pid()]["zname"] = pv[get_pid()]["li"][0]
    pv[get_pid()]["unzpath"] = (
        "." if len(pv[get_pid()]["li"]) < 2 else pv[get_pid()]["li"][1]
    )
    if not pv[get_pid()]["unzpath"].endswith("/"):
        pv[get_pid()]["unzpath"] += "/"
    if not pv[0]["sdcard_fs"]:
        remount("/", False)
    decompress(
        pv[get_pid()]["zname"],
        ljinux.api.betterpath(pv[get_pid()]["unzpath"]),
        quiet=pv[get_pid()]["quiett"],
        debug=pv[get_pid()]["jzdebug"],
    )
    if not pv[0]["sdcard_fs"]:
        remount("/", True)
    ljinux.api.setvar("return", "0")
elif "c" in pv[get_pid()]["opts"]["o"] or "compress" in pv[get_pid()]["opts"]["o"]:
    term.write("Compression not yet supported on-board")
    ljinux.api.setvar("return", "0")
else:
    ljinux.based.error(1)
    ljinux.api.setvar("return", "1")
