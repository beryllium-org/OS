opts2 = ljinux.based.fn.xarg(ljinux.based.user_vars["argj"])
errored = False

if len(opts2["w"]) > 2 and opts2["w"][0] == "install":
    # preperation

    fl = []  # folder list

    # load system package list
    ljinux.based.command.fpexecc([None, "/bin/random.py"])
    pklist = ljinux.based.user_vars["return"]
    print("JPKG: Package list loaded.")

    # extraction
    for i in opts2["w"][1:]:
        if errored:
            print("A fatal error has occured, exiting..")
            break
        randomm = None
        ljinux.based.silent = True
        ljinux.based.command.fpexecc([None, "/bin/random.py"])
        ljinux.based.silent = False
        randomm = ljinux.based.user_vars["return"].replace(".", "") + args2[1]

        ljinux.based.user_vars["argj"] = "- /tmp/" + randomm
        ljinux.based.command.fpexecc([None, "/bin/mkdir.py"])

        print(f'JPKG: Extracting "{i}".')
        ljinux.based.user_vars["argj"] = f"- quiet decompress {i} /tmp/{randomm}"
        ljinux.based.command.fpexecc([None, "/bin/jz.py"])
        print(f'JPKG: Extracted "{i}".')
        fl.append(randomm)
        del randomm
    print("JPKG: Packages extracted.")

    # parsing
    if not errored:
        bckdir = getcwd()
        for i in fl:
            print(f'JPKG: Reading properties of "{i}"..')
            chdir("/LjinuxRoot/tmp/" + i)

            if "manifest.json" in listdir():
                print("Reading package details..")
                manifest = None
                with open("Manifest.json", "r") as manifest_f:
                    try:
                        manifest = json.load(manifest_f)
                    except:
                        print("A fatal error has occured, exiting..")
                        break
                print(f"JPKG: Manifest loaded.")

                print(f"JPKG: Parsing done.")
                del manifest
            else:
                print("Error: Not a ljinux package!")

            # cleanup
            chdir(bckdir)
        del bckdir

    # cleanup (mandatory)
    if not sdcard_fs:
        remount("/", False)
    for j in fl:
        for i in listdir("/LjinuxRoot/tmp/" + randomm):
            remove(f"/LjinuxRoot/tmp/{randomm}/{i}")
    if not sdcard_fs:
        remount("/", True)
    ljinux.based.user_vars["argj"] = "- /tmp/" + randomm
    ljinux.based.command.fpexecc([None, "/bin/rmdir.py"])
    del fl
else:
    ljinux.based.error(1)
    ljinux.based.user_vars["return"] = "1"

del args2, argl2
