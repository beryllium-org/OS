rename_process("jpkg-install")
if gc.mem_free() < 100000:
    term.write("Low memory, wiping dmesg log..")
    be.based.run("_ndmesg")
vr("fl", set())
be.api.subscript("/bin/jpkg/generatelist.py")

for pv[get_pid()]["fileext"] in vr("opts")["w"][1:]:
    if vr("errored"):
        term.write(
            f"{colors.error}JPKG Error{colors.endc}: A fatal error has occured, exiting.."
        )
        break
    be.based.silent = True
    be.based.command.fpexec("/bin/random.py")
    be.based.silent = False
    vr("extpath", "/tmp/" + be.api.getvar("return")[2:] + vr("fileext")[:-4])
    be.based.run("mkdir " + vr("extpath"))

    term.write(
        "{}JPKG{}: Extracting {} ...".format(
            colors.green_t, colors.endc, vr("fileext")[:-4]
        )
    )
    be.based.run("jz -q -d {} {}".format(vr("fileext"), vr("extpath")))
    if be.api.getvar("return") == "0":
        term.write(f"{colors.green_t}JPKG{colors.endc}: Extracted to " + vr("extpath"))
    else:
        term.write(f"{colors.error}JPKG Error{colors.endc}: Package extraction failed!")
        vr("errored", True)
        break
    pv[get_pid()]["fl"].add(vr("extpath"))
vr("bckdir", getcwd())
vr("os_olddir", be.based.olddir)
be.based.olddir = None
vr("updatee", set())
if not vr("errored"):
    for pv[get_pid()]["fileext"] in vr("fl"):
        term.write(
            '{}JPKG{}: Reading properties "{}" ...'.format(
                colors.green_t, colors.endc, vr("fileext")
            )
        )
        chdir(pv[0]["root"] + vr("fileext"))

        if "Manifest.json" in listdir():
            with open("Manifest.json") as pv[get_pid()]["manifest_f"]:
                from json import load

                vr("manifest", load(vr("manifest_f")))
                del load

                if vr("jpkg_version") < vr("manifest")["JPKG_minimum_version"]:
                    vr("errored", True)
                    term.write(
                        f"{colors.error}JPKG Error{colors.endc}: Package "
                        + vr("manifest")["package_name"]
                        + " requires a higher version of jpkg, cannot continue."
                    )
                    break

                try:  # Go on, have a stroke tryna read this
                    if vr("manifest")["package_name"] not in vr("pklist")[0].keys() or (
                        vr("pklist")[0][vr("manifest")["package_name"]][0][0]
                        <= vr("manifest")["version"][0]
                        or vr("pklist")[0][vr("manifest")["package_name"]][0][1]
                        <= vr("manifest")["version"][1]
                        or vr("pklist")[0][vr("manifest")["package_name"]][0][2]
                        <= vr("manifest")["version"][2]
                    ):
                        vr("pklist")[0][vr("manifest")["package_name"]] = [
                            vr("manifest")["version"],
                            vr("manifest")["dependencies"],
                            vr("manifest")["conflicts"],
                        ]
                    else:  # exists and version <=
                        vr("errored", True)
                        term.write(
                            f"{colors.error}JPKG Error{colors.endc}: Package "
                            + vr("manifest")["package_name"]
                            + " version smaller than current ("
                            + str(vr("pklist")[0][vr("manifest")["package_name"]][0][0])
                            + "."
                            + str(vr("pklist")[0][vr("manifest")["package_name"]][0][1])
                            + "."
                            + str(vr("pklist")[0][vr("manifest")["package_name"]][0][2])
                            + ")."
                        )
                except KeyError:
                    term.write(
                        f"{colors.error}JPKG Error{colors.endc}: Invalid package manifest!"
                    )
                    vr("errored", True)
                    break

                for pv[get_pid()]["depsc"] in vr("manifest")["dependencies"]:
                    if vr("depsc") not in vr("pklist")[1]:
                        vr("pklist")[1].add(vr("depsc"))

                for pv[get_pid()]["confc"] in vr("manifest")["conflicts"]:
                    if vr("confc") not in vr("pklist")[2]:
                        vr("pklist")[2].add(vr("confc"))
        else:
            term.write(
                f"{colors.error}JPKG Error{colors.endc}: Not a valid JPKG package!"
            )
            vr("errored", True)
            break

# checks before install
if not vr("errored"):
    term.nwrite(
        f"{colors.green_t}JPKG{colors.endc}: Verifying package transaction ... 0%"
    )
    for pv[get_pid()]["dependency"] in vr("pklist")[1]:
        if vr("dependency") not in pklist[0].keys():  # not in installed
            term.nwrite(
                f"\n{colors.error}JPKG Error{colors.endc}: Dependency not satisfied: "
                + vr("dependency")
            )
            vr("errored", True)

    if not vr("errored"):
        term.clear_line()
        term.nwrite(
            f"{colors.green_t}JPKG{colors.endc}: Verifying package transaction ... 50%"
        )
    for pv[get_pid()]["conflict"] in vr("pklist")[2]:
        if vr("conflict") in vr("pklist")[0].keys():  # in installed
            term.nwrite(
                f"\n{colors.error}JPKG Error{colors.endc}: Package conflict: "
                + vr("conflict")
            )
            vr("errored", True)

    if not vr("errored"):
        term.clear_line()
        term.write(
            f"{colors.green_t}JPKG{colors.endc}: Verifying package transaction ... 100%"
        )
    else:
        term.write()

gc.collect()
gc.collect()

if not pv[0]["sdcard_fs"]:
    remount("/", False)

# installation
if not vr("errored"):
    for pv[get_pid()]["fileext"] in vr("fl"):
        chdir(pv[0]["root"] + vr("fileext"))
        with open("Manifest.json", "r") as pv[get_pid()]["manifest_f"]:
            from json import load

            vr("manifest", load(vr("manifest_f")))  # safe to load now
            del load
            term.write(
                f"{colors.green_t}JPKG{colors.endc}: Setting up "
                + vr("manifest")["package_name"]
                + " ("
                + str(vr("manifest")["version"][0])
                + "."
                + str(vr("manifest")["version"][1])
                + "."
                + str(vr("manifest")["version"][2])
                + ") ..."
            )
            be.api.setvar("return", "1")
            be.based.command.fpexec(
                vr("fileext")
                + "/"
                + vr("manifest")[
                    str(
                        "update"
                        if vr("manifest")["package_name"] in vr("updatee")
                        else "install"
                    )
                ],
            )
            if not pv[0]["sdcard_fs"]:
                remount("/", False)
            if be.api.getvar("return") != "0":
                term.write(
                    f"{colors.error}JPKG Error{colors.endc}: Package install returned non-zero exit code: "
                    + str(be.api.getvar("return"))
                )
                vr("errored", True)
                break
            else:
                # manifest install
                with be.api.fopen(
                    "/etc/jpkg/installed/" + vr("manifest")["package_name"] + ".json",
                    "w",
                ) as pv[get_pid()]["newman"]:
                    from json import dump

                    dump(vr("manifest"), vr("newman"))
                    del dump

                # copy uninstaller
                be.based.run(
                    "cp "
                    + vr("manifest")["remove"]
                    + " "
                    + pv[0]["root"]
                    + "/etc/jpkg/uninstallers/"
                    + vr("manifest")["package_name"]
                    + ".py",
                )

            if not pv[0]["sdcard_fs"]:  # again cuz cp reverted it
                remount("/", False)
            vrd("manifest")

chdir(vr("bckdir"))
be.based.olddir = vr("os_olddir")

for pv[get_pid()]["package"] in vr("fl"):
    for pv[get_pid()]["filee"] in listdir(pv[0]["root"] + vr("package")):
        remove(pv[0]["root"] + vr("package") + "/" + vr("filee"))
    rmdir(pv[0]["root"] + vr("package"))

if not pv[0]["sdcard_fs"]:
    remount("/", True)

be.api.setvar("return", str(int(vr("errored"))))
