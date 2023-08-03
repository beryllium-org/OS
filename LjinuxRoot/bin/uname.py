try:
    if ljinux.based.user_vars["argj"].split()[1] == "-a":
        pv[get_pid()]["tt"] = time.localtime()
        pv[get_pid()]["dat"] = [
            ljinux.based.system_vars["BOARD"],
            ljinux.based.system_vars["VERSION"],
            pv[get_pid()]["tt"].tm_year,
            pv[get_pid()]["tt"].tm_mday,
            pv[get_pid()]["tt"].tm_mon,
            pv[get_pid()]["tt"].tm_hour,
            pv[get_pid()]["tt"].tm_min,
            pv[get_pid()]["tt"].tm_sec,
        ]

        for pv[get_pid()]["i"] in range(3, 8):
            pv[get_pid()]["dat"][pv[get_pid()]["i"]] = str(
                pv[get_pid()]["dat"][pv[get_pid()]["i"]]
            )
            if len(pv[get_pid()]["dat"][pv[get_pid()]["i"]]) == 1:
                pv[get_pid()]["dat"][pv[get_pid()]["i"]] = (
                    "0" + pv[get_pid()]["dat"][pv[get_pid()]["i"]]
                )

        term.write(
            "Ljinux {} {} {}/{}/{} {}:{}:{} circuitpython Ljinux".format(
                pv[get_pid()]["dat"][0],
                pv[get_pid()]["dat"][1],
                pv[get_pid()]["dat"][3],
                pv[get_pid()]["dat"][4],
                pv[get_pid()]["dat"][2],
                pv[get_pid()]["dat"][5],
                pv[get_pid()]["dat"][6],
                pv[get_pid()]["dat"][7],
            )
        )
except IndexError:
    term.write("Ljinux")
ljinux.api.setvar("return", "0")
