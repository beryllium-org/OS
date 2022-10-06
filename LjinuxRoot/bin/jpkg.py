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
            print("A fatal error has occured, exiting..")
            break
        ljinux.based.silent = True
        ljinux.based.command.fpexecc([None, "/bin/random.py"])
        ljinux.based.silent = False
        extpath = "/tmp/" + ljinux.based.user_vars["return"][2:] + fileext[:-4]
        ljinux.based.user_vars["argj"] = "a " + extpath
        ljinux.based.command.fpexecc([None, "/bin/mkdir.py"])

        print(f"JPKG: Extracting {fileext[:-4]}")
        ljinux.based.user_vars["argj"] = f"a -q -d {fileext} {extpath}"
        ljinux.based.command.fpexecc([None, "/bin/jz.py"])
        if ljinux.based.user_vars["return"] == "0":
            print(f"JPKG: Extracted to " + extpath)
        else:
            print("JPKG: ERROR: Package extraction failed!")
            errored = True
            break
        fl.append(extpath)
        del extpath, fileext

    # parsing
    if not errored:
        bckdir = getcwd()
        for fileext in fl:
            print(f'JPKG: Reading properties.. "{fileext}"')
            chdir("/LjinuxRoot" + fileext)

            if "Manifest.json" in listdir():
                manifest = None
                with open("Manifest.json", "r") as manifest_f:
                    try:
                        manifest = json.load(manifest_f)
                    except:
                        print("JPKG: Error: Could not parse package manifest!")
                        break
                del manifest
            else:
                print("Error: Not a ljinux package!")
                errored = True
                break

            chdir(bckdir)
            del fileext
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
    del fl
else:
    ljinux.based.error(1)
    ljinux.based.user_vars["return"] = "1"

del opts2, jpkg_version
