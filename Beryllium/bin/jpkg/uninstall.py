rename_process("jpkg-uninstall")
be.api.subscript("/bin/jpkg/generatelist.py")
be.api.setvar("return", "1")
vr("errored", False)

for pv[get_pid()]["package"] in vr("opts")["w"][1:]:
    if vr("package") not in vr("pklist")[0].keys():
        term.write(
            f"{colors.error}JPKG Error{colors.endc}: Package "
            + vr("package")
            + " not installed."
        )
        vr("errored", True)
    if vr("errored"):
        break

if not vr("errored"):
    vrd("pklist")
    gc.collect()
    gc.collect()
    be.api.setvar("omit", set(vr("opts")["w"][1:]))
    term.write(f"{colors.green_t}JPKG{colors.endc}: Updating package list.")
    be.api.subscript("/bin/jpkg/generatelist.py")
    be.api.setvar("return", "1")
    be.api.setvar("omit")  # this deletes it

if not vr("errored"):
    # Dependency checks
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

    # conflict checks
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

if not vr("errored"):
    for pv[get_pid()]["pkgname"] in vr("opts")["w"][1:]:
        with open(
            pv[0]["root"] + "/etc/jpkg/installed/" + vr("pkgname") + ".json", "r"
        ) as pv[get_pid()]["manifest_f"]:
            from json import load

            manifest = load(vr("manifest_f"))  # safe to load now
            del load
            term.write(
                f"{colors.green_t}JPKG{colors.endc}: Removing "
                + manifest["package_name"]
                + " ("
                + str(manifest["version"][0])
                + "."
                + str(manifest["version"][1])
                + "."
                + str(manifest["version"][2])
                + ") ..."
            )
        be.api.setvar("return", "1")

        be.based.command.fpexec("/etc/jpkg/uninstallers/" + vr("pkgname") + ".py")
        if not pv[0]["sdcard_fs"]:
            remount("/", False)

        if be.api.getvar("return") != "0":
            term.write(
                f"{colors.error}JPKG Error{colors.endc}: Package uninstall returned non-zero exit code: "
                + str(be.api.getvar("return"))
            )
            term.write(
                f"{colors.error}JPKG Error{colors.endc}: Manual intervention required!"
            )
            vr("errored", True)
            break
        else:
            # manifest removal
            remove(pv[0]["root"] + "/etc/jpkg/installed/" + vr("pkgname") + ".json")

            # uninstaller removal
            remove(pv[0]["root"] + "/etc/jpkg/uninstallers/" + vr("pkgname") + ".py")

if not pv[0]["sdcard_fs"]:
    remount("/", True)

be.api.setvar("return", str(int(vr("errored"))))
