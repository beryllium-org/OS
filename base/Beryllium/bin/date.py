rename_process("date")
vr("args", be.based.user_vars["argj"].split())
try:
    if vr("args")[1] == "set":
        import rtc

        try:
            rtc.RTC().datetime = time.struct_time(
                (
                    int(vr("args")[2]),
                    int(vr("args")[3]),
                    int(vr("args")[4]),
                    int(vr("args")[5]) if len(vr("args")) > 5 else 0,
                    int(vr("args")[6]) if len(vr("args")) > 6 else 0,
                    int(vr("args")[7]) if len(vr("args")) > 7 else 0,
                    int(vr("args")[8]) if len(vr("args")) > 8 else 0,
                    int(vr("args")[9]) if len(vr("args")) > 9 else 0,
                    int(vr("args")[10]) if len(vr("args")) > 10 else 0,
                )
            )  # yr, mon, d, hr, m, s, ss, shit,shit,shit
        except IndexError:
            be.based.error(1)
        del rtc
    else:
        raise IndexError
except IndexError:
    vr("tt", time.localtime())
    vr(
        "dat",
        [
            vr("tt").tm_mday,
            vr("tt").tm_mon,
            vr("tt").tm_hour,
            vr("tt").tm_min,
            vr("tt").tm_sec,
        ],
    )

    for pv[get_pid()]["i"] in range(0, 5):
        vr("dat")[vr("i")] = str(vr("dat")[vr("i")])
        if len(str(vr("dat")[vr("i")])) < 2:
            vr("dat")[vr("i")] = "0" + vr("dat")[vr("i")]

    vr(
        "daydict",
        {
            0: "Mon",
            1: "Tue",
            2: "Wed",
            3: "Thu",
            4: "Fri",
            5: "Sat",
            6: "Sun",
        },
    )

    vr("day", vr("daydict")[vr("tt").tm_wday])

    term.write(
        "{} {} {} {} {}:{}:{}".format(
            vr("day"),
            vr("dat")[0],
            vr("dat")[1],
            vr("tt").tm_year,
            vr("dat")[2],
            vr("dat")[3],
            vr("dat")[4],
        )
    )
