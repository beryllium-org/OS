opts2 = ljinux.based.fn.xarg()
errored = False

jpkg_version = 0

if len(opts2["w"]) > 1 and opts2["w"][0] == "install":
    # preperation

    fl = []  # folder list

    # load system package list
    ljinux.based.command.fpexecc([None, "/etc/jpkg/tools/generatelist.py"])
    pklist = ljinux.based.user_vars["return"]
    """
    pklist[0] is packages w/ version, deps, conficts
    pklist[1] is a set of all deps
    pklist[2] is a set of all conflicts
    """
    ljinux.based.user_vars["return"] = "1"
    # we do not want to leave the whole package list in return

    # extraction
    for fileext in opts2["w"][1:]:
        if errored:
            print("JPKG Error: A fatal error has occured, exiting..")
            break
        ljinux.based.silent = True
        ljinux.based.command.fpexecc([None, "/bin/random.py"])
        ljinux.based.silent = False
        extpath = "/tmp/" + ljinux.based.user_vars["return"][2:] + fileext[:-4]
        ljinux.based.user_vars["argj"] = "a " + extpath
        ljinux.based.command.fpexecc([None, "/bin/mkdir.py"])

        print(f"JPKG: Extracting {fileext[:-4]} ...")
        ljinux.based.user_vars["argj"] = f"a -q -d {fileext} {extpath}"
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
                                vrs[0] > manifest["version"][0]
                                or vrs[1] > manifest["version"][1]
                                or vrs[2] > manifest["version"][2]
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
                                    + " version smaller or equal to current."
                                )
                            del vrs

                        pklist[1].extend(
                            [
                                filter(
                                    lambda depsc: depsc not in pklist[1],
                                    manifest["dependencies"],
                                )
                            ]
                        )
                        # for depsc in manifest["dependencies"]:  # keeping it in temporarily
                        # if depsc not in pklist[1]:
                        #    pklist[1].append(depsc)
                        # del depsc

                        pklist[2].extend(
                            [
                                filter(
                                    lambda confc: confc not in pklist[2],
                                    manifest["conflicts"],
                                )
                            ]
                        )
                        # for confc in manifest["conflicts"]:
                        # if confc not in pklist[2]:
                        #    pklist[2].append(confc)
                        # del confc
                        del manifest
                    except:
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
        for pd in pklist[1]:  # for dep
            if pd not in pklist[0].keys():  # not in installed
                print(f"\nJPKG Error: Dependency not satisfied: {pd}")
                errored = True
            del pd

        stdout.write("\010 \010" * 2 + "50%")
        # conflict checks
        for pc in pklist[2]:  # for confict
            if pc in pklist[0].keys():  # in installed
                print(f"\nJPKG Error: Package conflict: {pc}")
                errored = True
            del pc

        print("\010 \010" * 3 + "100%")

    # our hopes and prayers it won't fail
    collect()
    collect()

    # installation
    if not errored:
        for fileext in fl:
            chdir("/LjinuxRoot" + fileext)
            with open("Manifest.json", "r") as manifest_f:
                manifest = json.load(manifest_f)  # safe to load now
                modee = "install"
                if manifest["package_name"] in updatee:
                    modee = "update"
                print(
                    "JPKG: Setting up "
                    + manifest["package_name"]
                    + " ("
                    + manifest["version"]
                    + ") ..."
                )
                ljinux.based.command.fpexecc([None, (fileext + "/" + manifest[modee])])
                del modee
            del fileext

    # go back
    chdir(bckdir)
    del bckdir

    # cleanup (mandatory)
    if not sdcard_fs:
        remount("/", False)
    for j in fl:
        for i in listdir("/LjinuxRoot/tmp/" + j):
            remove(f"/LjinuxRoot/tmp/{randomm}/{i}")
    if not sdcard_fs:
        remount("/", True)
    ljinux.based.user_vars["argj"] = "- /tmp/" + randomm
    ljinux.based.command.fpexecc([None, "/bin/rmdir.py"])
    del fl, newpkgs
else:
    ljinux.based.error(1)
    ljinux.based.user_vars["return"] = "1"

del opts2, jpkg_version
