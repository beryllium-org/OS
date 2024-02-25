rename_process("jpkg")
ljinux.api.setvar("return", "1")
vr("opts", ljinux.api.xarg())
vr("errored", False)

vr("jpkg_version", 2)

if len(vr("opts")["w"]) > 1 and vr("opts")["w"][0] == "install":
    ljinux.api.subscript("/bin/jpkg/install.py")

    term.write(
        "\nYou are higly advised to reboot, "
        + "since package decompression severly fragments the memory."
    )
elif len(vr("opts")["w"]) > 1 and vr("opts")["w"][0] == "uninstall":
    ljinux.api.subscript("/bin/jpkg/uninstall.py")
elif len(vr("opts")["w"]) is 1 and vr("opts")["w"][0] == "list":
    for pv[get_pid()]["package"] in listdir(pv[0]["root"] + "/etc/jpkg/installed"):
        with ljinux.api.fopen(
            pv[0]["root"] + "/etc/jpkg/installed/" + vr("package")
        ) as pv[get_pid()]["manifest_f"]:
            from json import load

            vr("manifest", load(vr("manifest_f")))
            del load
            term.write(
                colors.green_t
                + vr("manifest")["package_name"]
                + colors.endc
                + "/"
                + str(vr("manifest")["version"][0])
                + "."
                + str(vr("manifest")["version"][1])
                + "."
                + str(vr("manifest")["version"][2])
                + " [Installed]"
            )
    ljinux.api.setvar("return", "0")
else:
    ljinux.based.run("cat /etc/jpkg/data/help.txt")
    ljinux.api.setvar("return", "1")
