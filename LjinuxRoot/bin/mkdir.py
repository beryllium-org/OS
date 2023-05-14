global sdcard_fs
try:
    wd = ljinux.api.betterpath(ljinux.based.user_vars["argj"].split()[1])
    if ljinux.api.isdir(wd) == 2:
        if not sdcard_fs:
            remount("/", False)

        if ljinux.api.isdir(wd[: wd.rfind("/")]) == 2:
            fpaths = wd[: wd.find("/") + 1]
            wd = wd[wd.find("/") + 1 :]
            while wd.find("/") != -1:
                fpaths += wd[: wd.find("/") + 1]
                wd = wd[wd.find("/") + 1 :]
                if ljinux.api.isdir(fpaths) == 2:
                    mkdir(fpaths)
            wd = fpaths + wd
            del fpaths
        mkdir(wd)
        del wd

        if not sdcard_fs:
            remount("/", True)

        ljinux.based.user_vars["return"] = "0"

    else:
        raise OSError

except OSError:
    term.write(
        "mkdir: cannot create directory ‘"
        + ljinux.based.user_vars["argj"].split()[1]
        + "’: File exists"
    )
    ljinux.based.user_vars["return"] = "1"

except RuntimeError:
    ljinux.based.error(7)
    ljinux.based.user_vars["return"] = "1"

except IndexError:
    ljinux.based.error(1)
    ljinux.based.user_vars["return"] = "1"
