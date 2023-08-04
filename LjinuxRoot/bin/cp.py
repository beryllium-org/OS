rename_process("cp")
try:
    vr("rd", getcwd())
    vr("src", ljinux.api.betterpath(ljinux.based.user_vars["argj"].split()[1]))
    vr("srcisd", ljinux.api.isdir(vr("src"), rdir=vr("rd")))
    vr("dst", ljinux.api.betterpath(ljinux.based.user_vars["argj"].split()[2]))
    vr("dstisd", ljinux.api.isdir(vr("dst"), rdir=vr("rd")))
    vrd("rd")

    if vr("srcisd") is 2 or (vr("dstisd") is 2 and vr("dst").endswith("/")):
        raise OSError
    elif vr("srcisd") is 0 and vr("dstisd") in [0, 2]:
        with ljinux.api.fopen(vr("src"), "rb") as srcf:
            vr("srcd", srcf.read())
            with ljinux.api.fopen(vr("dst"), "wb") as dstf:
                dstf.write(vr("srcd"))
    elif vr("srcisd") is 1 and vr("dstisd") is 2:
        ljinux.api.setvar("argj", "mkdir {}".format(vr("dst")))
        ljinux.based.command.fpexec("/bin/mkdir.py")
        gc.collect()
        gc.collect()
        for pv[get_pid()]["i"] in listdir(vr("src")):
            term.write(vr("src") + "/" + vr("i") + " -> " + vr("dst") + "/" + vr("i"))
            if ljinux.api.isdir(pv[get_pid()]["src"] + "/" + pv[get_pid()]["i"]):
                ljinux.api.setvar(
                    "argj",
                    "cp " + vr("src") + "/" + vr("i") + " " + vr("dst") + "/" + vr("i"),
                )
                ljinux.based.command.fpexec("/bin/cp.py")
                vr("src", pv[get_pid()]["src"][: vr("src").rfind("/")])
                vr("dst", vr("dst")[: vr("dst").rfind("/")])
                vr("srcisd", ljinux.api.isdir(vr("src")))
                vr("dstisd", ljinux.api.isdir(vr("dst")))
            else:
                with ljinux.api.fopen(vr("src") + "/" + vr("i"), "rb") as srcf:
                    vr("srcd", srcf.read())
                    with ljinux.api.fopen(vr("dst") + "/" + vr("i"), "wb") as dstf:
                        dstf.write(vr("srcd"))
                    vrd("srcd")
            gc.collect()
            gc.collect()
    elif vr("srcisd") is 0 and vr("dstisd") is 1:
        with ljinux.api.fopen(vr("src"), "rb") as srcf:
            vr("srcd", srcf.read())
            with ljinux.api.fopen(
                vr("dst") + "/" + vr("src")[vr("src").rfind("/") + 1 :], "wb"
            ) as dstf:
                dstf.write(vr("srcd"))
    ljinux.api.setvar("return", "0")

except IndexError:
    ljinux.based.error(1)
    ljinux.api.setvar("return", "1")

except RuntimeError:
    ljinux.based.error(7)
    ljinux.api.setvar("return", "1")

except OSError:
    ljinux.based.error(4, f=ljinux.based.user_vars["argj"].split()[1])
