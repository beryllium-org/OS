rename_process("cp")
vr("opts", be.api.xarg())
vr("verbose", "v" in vr("opts")["o"] or "verbose" in vr("opts")["o"])

if len(vr("opts")["aw"]) == 2:
    vr("rd", getcwd())
    vr("src", be.api.fs.resolve(vr("opts")["aw"][0]))
    vr("srcisd", be.api.fs.isdir(vr("src"), rdir=vr("rd")))
    vr("dst", be.api.fs.resolve(vr("opts")["aw"][1]))
    vr("dstisd", be.api.fs.isdir(vr("dst"), rdir=vr("rd")))
    vrd("rd")
    be.api.setvar("return", "0")

    if vr("srcisd") == 2 or (vr("dstisd") == 2 and vr("dst").endswith("/")):
        be.based.error(4, f=vr("dst"))
        be.api.setvar("return", "1")
    elif (not vr("srcisd")) and vr("dstisd") in [0, 2]:
        if vr("verbose"):
            term.write(vr("src") + " -> " + vr("dst"))
        with be.api.fs.open(vr("src"), "rb") as pv[get_pid()]["srcf"]:
            vr("srcd", vr("srcf").read())
            with be.api.fs.open(vr("dst"), "wb") as pv[get_pid()]["dstf"]:
                if vr("dstf") is None:
                    be.based.error(7)
                    be.api.setvar("return", "1")
                else:
                    vr("dstf").write(vr("srcd"))
    elif vr("srcisd") == 1 and vr("dstisd") == 2:
        be.based.run("mkdir " + vr("dst"))
        vr("ls", listdir(vr("src")))
        for pv[get_pid()]["i"] in vr("ls"):
            be.based.run(
                "cp {}{}/{} {}/{}".format(
                    ("-v " if vr("verbose") else ""),
                    vr("src"),
                    vr("i"),
                    vr("dst"),
                    vr("i"),
                )
            )
            gc.collect()
            gc.collect()
    elif vr("srcisd") is 0 and vr("dstisd") is 1:
        if vr("verbose"):
            term.write(vr("src") + " -> " + vr("dst"))
        with be.api.fs.open(vr("src"), "rb") as pv[get_pid()]["srcf"]:
            vr("srcd", vr("srcf").read())
            with be.api.fs.open(
                vr("dst") + "/" + vr("src")[vr("src").rfind("/") + 1 :], "wb"
            ) as pv[get_pid()]["dstf"]:
                if vr("dstf") is None:
                    be.based.error(7)
                    be.api.setvar("return", "1")
                else:
                    vr("dstf").write(vr("srcd"))
else:
    be.based.error(1)
    be.api.setvar("return", "1")
