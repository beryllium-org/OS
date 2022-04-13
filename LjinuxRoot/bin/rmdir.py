global sdcard_fs
try:
    if not sdcard_fs:
        remount("/", False)
    rmdir(ljinux.based.user_vars["argj"].split()[1])
    if not sdcard_fs:
        remount("/", True)
except (OSError, RuntimeError) as errr:
    if str(errr) == "[Errno 2] No such file/directory":
        print(
            "rmdir: failed to remove ‘"
            + ljinux.based.user_vars["argj"].split()[1]
            + "’: No such file or directory"
        )
    else:
        print(
            "rmdir: failed to remove ‘"
            + ljinux.based.user_vars["argj"].split()[1]
            + "’: Cannot write, the pi pico is in read only mode!\nMake sure to disable to usb drive to be able to access these functions!"
        )
    del errr
except IndexError:
    pass 
