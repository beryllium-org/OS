rename_process("mv")
vr("opts", be.api.xarg())
vr("verbose", "v" in vr("opts")["o"] or "verbose" in vr("opts")["o"])

if len(vr("opts")["aw"]) == 2:
    vr("src", vr("opts")["aw"][0])
    vr("dst", vr("opts")["aw"][1])
    be.based.run(
        "cp {}{} {}".format(("-v " if vr("verbose") else ""), vr("src"), vr("dst"))
    )
    if be.api.getvar("return") == "0":
        be.based.run("rm " + vr("src"))
else:
    be.based.error(1)
    be.api.setvar("return", "1")
