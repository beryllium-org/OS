try:
    f = open(ljinux.based.user_vars["argj"].split()[1], "r")
    f.close()
    print("based: Error: file exists")
except OSError:
    global sdcard_fs
    if not sdcard_fs:
        try:
            remount("/", False)
            f = open(ljinux.based.user_vars["argj"].split()[1], "w")
            f.close()
            if not sdcard_fs:
                remount("/", True)
        except RuntimeError:
            print("based: Cannot remount built in fs in development mode")
