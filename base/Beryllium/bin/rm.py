rename_process("rm")
vr("opts", be.api.xarg())
vr("verbose", "v" in vr("opts")["o"] or "verbose" in vr("opts")["o"])
be.api.setvar("return", "0")

try:
    remount("/", False)
    vr("rd", getcwd())
    for pv[get_pid()]["f"] in vr("opts")["aw"]:
        vr("fn", be.api.fs.resolve(vr("f")))
        vr("t", be.api.fs.isdir(vr("f"), rdir=vr("rd")))
        if not vr("t"):
            if vr("verbose"):
                term.write("Removing: " + vr("fn"))
            remove(vr("fn"))
            if vr("fn") in be.code_cache:
                be.code_cache.pop(vr("fn"))
        elif vr("t") == 1:
            vr("ls", listdir(vr("fn")))
            for pv[get_pid()]["i"] in vr("ls"):
                if vr("verbose"):
                    term.write("Removing: {}/{}".format(vr("fn"), vr("i")))
                vr("t2", be.api.fs.isdir(vr("fn") + "/" + vr("i")))
                if not vr("t2"):
                    remove(vr("fn") + "/" + vr("i"))
                else:
                    be.based.run(
                        "rm {}{}/{}".format(
                            ("-v " if vr("verbose") else ""), vr("fn"), vr("i")
                        )
                    )
                    remount("/", False)
            term.write("Removing: " + vr("fn"))
            be.based.run("rmdir " + vr("fn"))
        else:
            be.based.error(4, f=vr("f"))
            be.api.setvar("return", "1")
    remount("/", True)
except RuntimeError:
    be.based.error(7)
    be.api.setvar("return", "1")
