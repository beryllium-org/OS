opts2 = ljinux.api.xarg()
errored = False

jpkg_version = 0

if len(opts2["w"]) > 1 and opts2["w"][0] == "install":
    # preperation

    fl = []  # folder list

    # load system package list
    ljinux.based.command.fpexecc([None, "/etc/jpkg/tools/generatelist.py"])
    pklist = ljinux.based.user_vars["return"]
    ljinux.api.var("return", "1")  # no garbage in return

    """
    pklist[0] is packages w/ version, deps, conficts
    pklist[1] is a set of all deps
    pklist[2] is a set of all conflicts
    """

    # extraction
    for fileext in opts2["w"][1:]:
        if errored:
            print("JPKG Error: A fatal error has occured, exiting..")
            break
        ljinux.based.silent = True
        ljinux.based.command.fpexecc([None, "/bin/random.py"])
        ljinux.based.silent = False
        extpath = "/tmp/" + ljinux.based.user_vars["return"][2:] + fileext[:-4]
        ljinux.api.var("argj", "a " + extpath)
        ljinux.based.command.fpexecc([None, "/bin/mkdir.py"])

        print(f"JPKG: Extracting {fileext[:-4]} ...")
        ljinux.api.var("argj", f"a -q -d {fileext} {extpath}")
        ljinux.based.command.fpexecc([None, "/bin/jz.py"])
        if ljinux.based.user_vars["return"] == "0":
            print("JPKG: Extracted to " + extpath)
        else:
            print("JPKG Error: Package extraction failed!")
            errored = True
            break
        fl.append(extpath)
        del extpath, fileext

    # backup path
    bckdir = getcwd()

    updatee = list()

    # parsing
    if not errored:
        for fileext in fl:
            print(f'JPKG: Reading properties "{fileext}" ...')
            chdir("/LjinuxRoot" + fileext)

            if "Manifest.json" in listdir():
                manifest = None
                with open("Manifest.json", "r") as manifest_f:
                    try:
                        manifest = json.load(manifest_f)
                        if manifest["package_name"] not in pklist[0].keys():
                            pklist[0].update(
                                {
                                    manifest["package_name"]: [
                                        manifest["version"],
                                        manifest["dependencies"],
                                        manifest["conflicts"],
                                    ]
                                }
                            )
                            if manifest["JPKG_minimum_version"] > jpkg_version:
                                errored = True
                                print(
                                    "JPKG Error: Package "
                                    + manifest["package_name"]
                                    + " requires a higher version of jpkg, cannot continue."
                                )
                        else:
                            vrs = pklist[0][manifest["package_name"]][0]
                            if (
                                vrs[0] >= manifest["version"][0]
                                or vrs[1] >= manifest["version"][1]
                                or vrs[2] >= manifest["version"][2]
                            ):  # update
                                updatee.append(manifest["package_name"])
                                pklist[0][manifest["package_name"]] = [
                                    manifest["version"],
                                    manifest["dependencies"],
                                    manifest["conflicts"],
                                ]
                            else:  # version <=
                                errored = True
                                print(
                                    "JPKG Error: Package "
                                    + manifest["package_name"]
                                    + " version smaller than current ("
                                    + str(vrs[0])
                                    + "."
                                    + str(vrs[1])
                                    + "."
                                    + str(vrs[2])
                                    + ")."
                                )
                            del vrs

                        for depsc in manifest["dependencies"]:
                            if depsc not in pklist[1]:
                                pklist[1].append(depsc)
                            del depsc

                        for confc in manifest["conflicts"]:
                            if confc not in pklist[2]:
                                pklist[2].append(confc)
                            del confc
                        del manifest
                    except Exception as err:
                        print(str(err))
                        print("JPKG Error: Could not parse package manifest!")
                        errored = True
                        break
            else:
                print("JPKG Error: Not a ljinux package!")
                errored = True
                break

            del fileext

    # checks before install
    if not errored:
        # Dependency checks
        stdout.write("JPKG: Verifying package transaction ... 0%")
        for dependency in pklist[1]:  # for dep
            if dependency not in pklist[0].keys():  # not in installed
                print(f"\nJPKG Error: Dependency not satisfied: {dependency}")
                errored = True
            del dependency

        stdout.write("\010 \010" * 2 + "50%")
        # conflict checks
        for conflict in pklist[2]:  # for confict
            if conflict in pklist[0].keys():  # in installed
                print(f"\nJPKG Error: Package conflict: {conflict}")
                errored = True
            del conflict

        print("\010 \010" * 3 + "100%")

    # our hopes and prayers it won't fail
    gc.collect()
    gc.collect()

    if not sdcard_fs:
        remount("/", False)

    # installation
    if not errored:
        for fileext in fl:
            chdir("/LjinuxRoot" + fileext)
            with open("Manifest.json", "r") as manifest_f:
                manifest = json.load(manifest_f)  # safe to load now
                print(
                    "JPKG: Setting up "
                    + manifest["package_name"]
                    + " ("
                    + str(manifest["version"][0])
                    + "."
                    + str(manifest["version"][1])
                    + "."
                    + str(manifest["version"][2])
                    + ") ..."
                )
                ljinux.based.command.fpexecc(
                    [
                        None,
                        fileext
                        + "/"
                        + manifest[
                            str(
                                "update"
                                if manifest["package_name"] in updatee
                                else "install"
                            )
                        ],
                    ]
                )

                # manifest install
                with open(
                    "/LjinuxRoot/etc/jpkg/installed/"
                    + manifest["package_name"]
                    + ".json",
                    "w",
                ) as newman:
                    json.dump(manifest, newman)
                    del newman

                # copy uninstaller
                ljinux.api.var(
                    "argj",
                    "cp "
                    + manifest["remove"]
                    + " /LjinuxRoot/etc/jpkg/uninstallers/"
                    + manifest["package_name"]
                    + ".py",
                )
                ljinux.based.command.fpexecc([None, "/bin/cp.py"])

                del manifest
            del fileext

    # go back
    chdir(bckdir)
    del bckdir, updatee

    # cleanup (mandatory)
    for package in fl:
        for filee in listdir("/LjinuxRoot" + package):
            remove(f"/LjinuxRoot{package}/{filee}")
            del filee
        rmdir(f"/LjinuxRoot{package}")
        del package
    if not sdcard_fs:
        remount("/", True)
    del fl

    # return
    ljinux.based.user_vars["return"] = str(int(errored))  # ljinux vars need to be str
    del errored
elif len(opts2["w"]) > 1 and opts2["w"][0] == "uninstall":
    # for comments look in installation
    ljinux.based.command.fpexecc([None, "/etc/jpkg/tools/generatelist.py"])
    pklist = ljinux.based.user_vars["return"]  # for comments look in installation
    ljinux.api.var("return", "1")
    errored = False

    for package in opts2["w"][1:]:
        if package not in pklist[0].keys():
            print(f"JPKG Error: Package {package} not installed.")
            errored = True
            del package
            break
        else:
            del package

    # remove from database in ram
    if not errored:
        pklist.clear()
        gc.collect()
        gc.collect()
        ljinux.based.user_vars.update({"omit": set(opts2["w"][1:])})
        ljinux.based.command.fpexecc([None, "/etc/jpkg/tools/generatelist.py"])
        pklist.update(ljinux.based.user_vars["return"])
        ljinux.api.var("return", "1")
        ljinux.api.var("omit")  # this deletes it

    # check if database is valid
    if not errored:
        # Dependency checks
        stdout.write("JPKG: Verifying package transaction ... 0%")
        for dependency in pklist[1]:  # for dep
            if dependency not in pklist[0].keys():  # not in installed
                print(f"\nJPKG Error: Dependency not satisfied: {dependency}")
                errored = True
            del dependency

        stdout.write("\010 \010" * 2 + "50%")
        # conflict checks
        for conflict in pklist[2]:  # for confict
            if conflict in pklist[0].keys():  # in installed
                print(f"\nJPKG Error: Package conflict: {conflict}")
                errored = True
            del conflict

        print("\010 \010" * 3 + "100%")

    # our hopes and prayers it won't fail
    gc.collect()
    gc.collect()

    if not sdcard_fs:
        remount("/", False)

    # removal
    if not errored:
        for pkgname in opts2["w"][1:]:
            chdir("/LjinuxRoot/etc/jpkg/uninstallers")

            with open(pkgname + ".json", "r") as manifest_f:
                manifest = json.load(manifest_f)  # safe to load now
                print(
                    "JPKG: Removing "
                    + manifest["package_name"]
                    + " ("
                    + str(manifest["version"][0])
                    + "."
                    + str(manifest["version"][1])
                    + "."
                    + str(manifest["version"][2])
                    + ") ..."
                )

                ljinux.based.command.fpexecc([None, pkgname + ".py"])

                # manifest removal
                remove(f"/LjinuxRoot/etc/jpkg/installed/{pkgname}.json")

                del manifest

            # uninstaller removal
            remove(f"/LjinuxRoot/etc/jpkg/uninstallers/{pkgname}.py")

            del pkgname

    # No need to bother going back in dir, since based will do it for us.
    del pklist

    if not sdcard_fs:
        remount("/", True)

    # return
    ljinux.api.var("return", str(int(errored)))
    del errored
else:
    ljinux.based.error(1)
    ljinux.api.var("return", "1")

del opts2, jpkg_version
