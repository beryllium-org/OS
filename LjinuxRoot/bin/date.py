rename_process("date")
pv[get_pid()]["args"] = ljinux.based.user_vars["argj"].split()
try:
    if pv[get_pid()]["args"][1] == "set":
        import rtc

        try:
            rtc.RTC().datetime = time.struct_time(
                (
                    int(pv[get_pid()]["args"][2]),
                    int(pv[get_pid()]["args"][3]),
                    int(pv[get_pid()]["args"][4]),
                    int(pv[get_pid()]["args"][5])
                    if len(pv[get_pid()]["args"]) > 5
                    else 0,
                    int(pv[get_pid()]["args"][6])
                    if len(pv[get_pid()]["args"]) > 6
                    else 0,
                    int(pv[get_pid()]["args"][7])
                    if len(pv[get_pid()]["args"]) > 7
                    else 0,
                    int(pv[get_pid()]["args"][8])
                    if len(pv[get_pid()]["args"]) > 8
                    else 0,
                    int(pv[get_pid()]["args"][9])
                    if len(pv[get_pid()]["args"]) > 9
                    else 0,
                    int(pv[get_pid()]["args"][10])
                    if len(pv[get_pid()]["args"]) > 10
                    else 0,
                )
            )  # yr, mon, d, hr, m, s, ss, shit,shit,shit
        except IndexError:
            ljinux.based.error(1)
        del rtc
    else:
        raise IndexError
except IndexError:
    pv[get_pid()]["tt"] = time.localtime()
    pv[get_pid()]["dat"] = [
        pv[get_pid()]["tt"].tm_mday,
        pv[get_pid()]["tt"].tm_mon,
        pv[get_pid()]["tt"].tm_hour,
        pv[get_pid()]["tt"].tm_min,
        pv[get_pid()]["tt"].tm_sec,
    ]

    for pv[get_pid()]["i"] in range(0, 5):
        pv[get_pid()]["dat"][pv[get_pid()]["i"]] = str(
            pv[get_pid()]["dat"][pv[get_pid()]["i"]]
        )
        if len(str(pv[get_pid()]["dat"][pv[get_pid()]["i"]])) < 2:
            pv[get_pid()]["dat"][pv[get_pid()]["i"]] = (
                "0" + pv[get_pid()]["dat"][pv[get_pid()]["i"]]
            )

    pv[get_pid()]["daydict"] = {
        0: "Mon",
        1: "Tue",
        2: "Wed",
        3: "Thu",
        4: "Fri",
        5: "Sat",
        6: "Sun",
    }
    pv[get_pid()]["day"] = pv[get_pid()]["daydict"][pv[get_pid()]["tt"].tm_wday]
    del pv[get_pid()]["daydict"]

    term.write(
        "{} {} {} {} {}:{}:{}".format(
            pv[get_pid()]["day"],
            pv[get_pid()]["dat"][0],
            pv[get_pid()]["dat"][1],
            pv[get_pid()]["tt"].tm_year,
            pv[get_pid()]["dat"][2],
            pv[get_pid()]["dat"][3],
            pv[get_pid()]["dat"][4],
        )
    )
