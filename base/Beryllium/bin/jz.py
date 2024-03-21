rename_process("jz")
vr("opts", be.api.xarg())
vr("li", vr("opts")["hw"] + vr("opts")["w"])
vr("quiett", be.based.silent or "q" in vr("opts")["o"])
vr("jzdebug", "debug" in vr("opts")["o"])

if ("d" in vr("opts")["o"] or "decompress" in vr("opts")["o"]) and len(vr("li")) > 0:
    from jz import decompress

    vr("zname", vr("li")[0])
    vr("unzpath", ("." if len(vr("li")) < 2 else vr("li")[1]))
    if not vr("unzpath").endswith("/"):
        vrp("unzpath", "/")
    if not vr("sdcard_fs", pid=0):
        remount("/", False)
    decompress(
        vr("zname"),
        be.api.fs.resolve(vr("unzpath")),
        quiet=vr("quiett"),
        debug=vr("jzdebug"),
    )
    if not vr("sdcard_fs", pid=0):
        remount("/", True)
    be.api.setvar("return", "0")
elif "c" in vr("opts")["o"] or "compress" in vr("opts")["o"]:
    term.write("Compression not yet supported on-board")
    be.api.setvar("return", "0")
else:
    be.based.error(1)
    be.api.setvar("return", "1")
