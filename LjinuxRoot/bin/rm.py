global sdcard_fs
try:
    if not sdcard_fs:
        remount("/", False)
    remove(ljinux.based.user_vars["argj"].split()[1])
    if not sdcard_fs:
        remount("/", True)
except (OSError, RuntimeError) as errr:
    if str(errr) == "[Errno 2] No such file/directory":
        print(
            "rm: failed to remove ‘"
            + ljinux.based.user_vars["argj"].split()[1]
            + "’: No such file or directory"
        )
    elif str(errr) == "[Errno 21] EISDIR":
        print("rm: Is directory")
    else:
        print(
            "rm: failed to remove ‘"
            + ljinux.based.user_vars["argj"].split()[1]
            + "’: Cannot write, the pi pico is in read only mode!\nMake sure to disable to usb drive to be able to access these functions!"
        )
    del errr
except IndexError:
    pass 
