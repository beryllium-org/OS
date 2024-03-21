rename_process("cp")
try:
    vr("rd", getcwd())
    vr("src", be.api.fs.resolve(be.based.user_vars["argj"].split()[1]))
    vr("srcisd", be.api.isdir(vr("src"), rdir=vr("rd")))
    vr("dst", be.api.fs.resolve(be.based.user_vars["argj"].split()[2]))
    vr("dstisd", be.api.isdir(vr("dst"), rdir=vr("rd")))
    vrd("rd")

    if vr("srcisd") is 2 or (vr("dstisd") is 2 and vr("dst").endswith("/")):
        raise OSError
    elif vr("srcisd") is 0 and vr("dstisd") in [0, 2]:
        with be.api.fopen(vr("src"), "rb") as pv[get_pid()]["srcf"]:
            vr("srcd", vr("srcf").read())
            with be.api.fopen(vr("dst"), "wb") as pv[get_pid()]["dstf"]:
                if vr("dstf") is None:
                    raise RuntimeError
                vr("dstf").write(vr("srcd"))
    elif vr("srcisd") is 1 and vr("dstisd") is 2:
        be.api.setvar("argj", "mkdir {}".format(vr("dst")))
        be.based.command.fpexec("/bin/mkdir.py")
        gc.collect()
        gc.collect()
        for pv[get_pid()]["i"] in listdir(vr("src")):
            term.write(vr("src") + "/" + vr("i") + " -> " + vr("dst") + "/" + vr("i"))
            if be.api.isdir(pv[get_pid()]["src"] + "/" + pv[get_pid()]["i"]):
                be.api.setvar(
                    "argj",
                    "cp " + vr("src") + "/" + vr("i") + " " + vr("dst") + "/" + vr("i"),
                )
                be.based.command.fpexec("/bin/cp.py")
                vr("src", pv[get_pid()]["src"][: vr("src").rfind("/")])
                vr("dst", vr("dst")[: vr("dst").rfind("/")])
                vr("srcisd", be.api.isdir(vr("src")))
                vr("dstisd", be.api.isdir(vr("dst")))
            else:
                with be.api.fopen(vr("src") + "/" + vr("i"), "rb") as srcf:
                    vr("srcd", srcf.read())
                    with be.api.fopen(vr("dst") + "/" + vr("i"), "wb") as dstf:
                        dstf.write(vr("srcd"))
                    vrd("srcd")
            gc.collect()
            gc.collect()
    elif vr("srcisd") is 0 and vr("dstisd") is 1:
        with be.api.fopen(vr("src"), "rb") as pv[get_pid()]["srcf"]:
            with be.api.fopen(
                vr("dst") + "/" + vr("src")[vr("src").rfind("/") + 1 :], "wb"
            ) as pv[get_pid()]["dstf"]:
                if vr("dstf") is None:
                    raise RuntimeError
                vr("dstf").write(vr("srcd"))
    be.api.setvar("return", "0")

except IndexError:
    be.based.error(1)
    be.api.setvar("return", "1")

except RuntimeError:
    be.based.error(7)
    be.api.setvar("return", "1")

except OSError:
    be.based.error(4, f=be.based.user_vars["argj"].split()[1])
