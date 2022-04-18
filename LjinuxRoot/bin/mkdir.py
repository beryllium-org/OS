global sdcard_fs
try:
    if not sdcard_fs:
        remount("/", False)
    mkdir(ljinux.based.fn.betterpath(ljinux.based.user_vars["argj"].split()[1]))
    if not sdcard_fs:
        remount("/", True)
except (OSError, RuntimeError) as errr:
    if str(errr) == "[Errno 17] File exists":
        print(
            "mkdir: cannot create directory ‘"
            + ljinux.based.user_vars["argj"].split()[1]
            + "’: File exists"
        )
    else:
        print(
            "mkdir: cannot create directory ‘"
            + ljinux.based.user_vars["argj"].split()[1]
            + "’: Cannot write, the pi pico is in read only mode!\nMake sure to disable to usb drive to be able to access these functions!"
        )
    del errr
except IndexError:
    pass
