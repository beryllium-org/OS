aaa = ljinux.based.user_vars["argj"].split()
try:
    if aaa[1] == "set":
        try:
            the_time = time.struct_time(
                (
                    int(aaa[4]),
                    int(aaa[3]),
                    int(aaa[2]),
                    int(aaa[5]),
                    int(aaa[6]),
                    int(aaa[7]),
                    1,
                    -1,
                    -1,
                )
            )  # yr, mon, d, hr, m, s, ss, shit,shit,shit
            rtcc.write_datetime(the_time)
        except IndexError:
            ljinux.based.error(1)
except IndexError:
    tt = time.localtime()
    print(
        "Current time: "
        + str(tt.tm_mday)
        + "/"
        + str(tt.tm_mon)
        + "/"
        + str(tt.tm_year)
        + " "
        + str(tt.tm_hour)
        + ":"
        + str(tt.tm_min)
        + ":"
        + str(tt.tm_sec)
    )
    del tt
del aaa
