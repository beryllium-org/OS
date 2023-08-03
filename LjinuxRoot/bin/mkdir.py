rename_process("mkdir")
try:
    pv[get_pid()]["wd"] = ljinux.api.betterpath(
        ljinux.based.user_vars["argj"].split()[1]
    )
    if ljinux.api.isdir(pv[get_pid()]["wd"]) == 2:
        if not pv[0]["sdcard_fs"]:
            remount("/", False)
        if ljinux.api.isdir(pv[get_pid()]["wd"][: wd.rfind("/")]) == 2:
            pv[get_pid()]["fpaths"] = pv[get_pid()]["wd"][
                : pv[get_pid()]["wd"].find("/") + 1
            ]
            pv[get_pid()]["wd"] = pv[get_pid()]["wd"][
                pv[get_pid()]["wd"].find("/") + 1 :
            ]
            while pv[get_pid()]["wd"].find("/") != -1:
                pv[get_pid()]["fpaths"] += pv[get_pid()]["wd"][
                    : pv[get_pid()]["wd"].find("/") + 1
                ]
                pv[get_pid()]["wd"] = pv[get_pid()]["wd"][
                    pv[get_pid()]["wd"].find("/") + 1 :
                ]
                if ljinux.api.isdir(pv[get_pid()]["fpaths"]) == 2:
                    mkdir(pv[get_pid()]["fpaths"])
            pv[get_pid()]["wd"] = pv[get_pid()]["fpaths"] + pv[get_pid()]["wd"]
        mkdir(pv[get_pid()]["wd"])
        if not pv[0]["sdcard_fs"]:
            remount("/", True)
        ljinux.api.setvar("return", "0")
    else:
        raise OSError
except OSError:
    term.write(
        "mkdir: cannot create directory ‘"
        + ljinux.based.user_vars["argj"].split()[1]
        + "’: File exists"
    )
    ljinux.api.setvar("return", "1")
except RuntimeError:
    ljinux.based.error(7)
    ljinux.api.setvar("return", "1")
except IndexError:
    ljinux.based.error(1)
    ljinux.api.setvar("return", "1")
