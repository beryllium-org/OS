rename_process("cp")
try:
    pv[get_pid()]["rd"] = getcwd()
    pv[get_pid()]["src"] = ljinux.api.betterpath(
        ljinux.based.user_vars["argj"].split()[1]
    )
    pv[get_pid()]["srcisd"] = ljinux.api.isdir(src, rdir=pv)
    pv[get_pid()]["dst"] = ljinux.api.betterpath(
        ljinux.based.user_vars["argj"].split()[2]
    )
    pv[get_pid()]["dstisd"] = ljinux.api.isdir(dst, rdir=rd)
    del pv[get_pid()]["rd"]

    if pv[get_pid()]["srcisd"] is 2 or (
        pv[get_pid()]["dstisd"] is 2 and pv[get_pid()]["dst"].endswith("/")
    ):
        raise OSError
    elif pv[get_pid()]["srcisd"] is 0 and pv[get_pid()]["dstisd"] in [
        0,
        2,
    ]:  # both files / dst non existent
        with ljinux.api.fopen(pv[get_pid()]["src"], "rb") as pv[get_pid()]["srcf"]:
            pv[get_pid()]["srcd"] = pv[get_pid()]["srcf"].read()
            with ljinux.api.fopen(pv[get_pid()]["dst"], "wb") as pv[get_pid()]["dstf"]:
                pv[get_pid()]["dstf"].write(pv[get_pid()]["srcd"])
    elif srcisd is 1 and dstisd is 2:
        ljinux.api.setvar("argj", f"mkdir {dst}")
        ljinux.based.command.fpexec("/bin/mkdir.py")
        gc.collect()
        gc.collect()
        for pv[get_pid()]["i"] in listdir(pv[get_pid()]["src"]):
            term.write(
                pv[get_pid()]["src"]
                + "/"
                + pv[get_pid()]["i"]
                + " -> "
                + pv[get_pid()]["dst"]
                + "/"
                + pv[get_pid()]["i"]
            )
            if ljinux.api.isdir(pv[get_pid()]["src"] + "/" + pv[get_pid()]["i"]):
                ljinux.api.setvar(
                    "argj",
                    "cp "
                    + pv[get_pid()]["src"]
                    + "/"
                    + pv[get_pid()]["i"]
                    + " "
                    + pv[get_pid()]["dst"]
                    + "/"
                    + pv[get_pid()]["i"],
                )
                ljinux.based.command.fpexec("/bin/cp.py")
                pv[get_pid()]["src"] = pv[get_pid()]["src"][
                    : pv[get_pid()]["src"].rfind("/")
                ]
                pv[get_pid()]["dst"] = pv[get_pid()]["dst"][
                    : pv[get_pid()]["dst"].rfind("/")
                ]
                pv[get_pid()]["srcisd"] = ljinux.api.isdir(pv[get_pid()]["src"])
                pv[get_pid()]["dstisd"] = ljinux.api.isdir(pv[get_pid()]["dst"])
            else:
                with ljinux.api.fopen(
                    pv[get_pid()]["src"] + "/" + pv[get_pid()]["i"], "rb"
                ) as pv[get_pid()]["srcf"]:
                    pv[get_pid()]["srcd"] = pv[get_pid()]["srcf"].read()
                    with ljinux.api.fopen(
                        pv[get_pid()]["dst"] + "/" + pv[get_pid()]["i"], "wb"
                    ) as pv[get_pid()]["dstf"]:
                        pv[get_pid()]["dstf"].write(pv[get_pid()]["srcd"])
            gc.collect()
            gc.collect()
    ljinux.api.setvar("return", "0")

except IndexError:
    ljinux.based.error(1)
    ljinux.api.setvar("return", "1")

except RuntimeError:
    ljinux.based.error(7)
    ljinux.api.setvar("return", "1")

except OSError:
    ljinux.based.error(4, f=ljinux.based.user_vars["argj"].split()[1])
