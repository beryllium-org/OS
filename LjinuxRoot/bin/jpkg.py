args2 = ljinux.based.user_vars["argj"].split()[1:]
argl2 = len(args2)
# name change required, so that it won't conflict with the nested execution of jz and mkdir
if "network" in ljinux.modules and ljinux.modules["network"].connected == True:
    if argl2 > 1 and args2[0] == "install":
        # preperation
        randomm = None
        ljinux.based.silent = True
        ljinux.based.command.fpexecc([None, "/bin/random.py"])
        ljinux.based.silent = False
        randomm = ljinux.based.user_vars["return"].replace(".", "") + args2[1]

        ljinux.based.user_vars["argj"] = "- /tmp/" + randomm
        ljinux.based.command.fpexecc([None, "/bin/mkdir.py"])

        ljinux.based.user_vars["argj"] = f"- quiet decompress {args2[1]} /tmp/{randomm}"
        ljinux.based.command.fpexecc([None, "/bin/jz.py"])

        # installation
        bckdir = getcwd()
        chdir("/LjinuxRoot/tmp/" + randomm)

        if "manifest.json" in listdir():
            print("Reading package details..")
            manifest = None
            with open(board_config := "manifest.json") as manifest_f:
                manifest = json.load(manifest)
            print(str(manifest))
            del manifest
        else:
            print("Error: Not a ljinux package!")

        # cleanup
        chdir(bckdir)
        del bckdir

        if not sdcard_fs:
            remount("/", False)
        for i in listdir("/LjinuxRoot/tmp/" + randomm):
            remove(f"/LjinuxRoot/tmp/{randomm}/{i}")
        if not sdcard_fs:
            remount("/", True)
        ljinux.based.user_vars["argj"] = "- /tmp/" + randomm
        ljinux.based.command.fpexecc([None, "/bin/rmdir.py"])
        del randomm
    else:
        ljinux.based.error(1)
        ljinux.based.user_vars["return"] = "1"
else:
    ljinux.based.error(5)
    ljinux.based.user_vars["return"] = "1"

del args2, argl2
