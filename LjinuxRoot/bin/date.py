args = ljinux.based.user_vars["argj"].split()
try:
    if args[1] == "set":
        try:
            the_time = time.struct_time(
                (
                    int(args[4]),
                    int(args[3]),
                    int(args[2]),
                    int(args[5]),
                    int(args[6]),
                    int(args[7]),
                    1,
                    -1,
                    -1,
                )
            )  # yr, mon, d, hr, m, s, ss, shit,shit,shit
            rtcc.write_datetime(the_time)
        except IndexError:
            ljinux.based.error(1)
    else:
        raise IndexError
except IndexError:
    tt = time.localtime()
    daydict = {
        1: "Mon",
        2: "Tue",
        3: "Wed",
        4: "Thu",
        5: "Fri",
        6: "Sat",
        7: "Sun",
    }
    day = daydict[tt.tm_wday]
    del daydict

    print(
        f"{day} {tt.tm_mday} {tt.tm_mon} {tt.tm_year} {tt.tm_hour}:{tt.tm_min}:{tt.tm_sec}"
    )
    del tt, day
del args
