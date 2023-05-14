args = ljinux.based.user_vars["argj"].split()
try:
    if args[1] == "set":
        import rtc

        try:
            rtc.RTC().datetime = time.struct_time(
                (
                    int(args[2]),
                    int(args[3]),
                    int(args[4]),
                    int(args[5]) if len(args) > 5 else 0,
                    int(args[6]) if len(args) > 6 else 0,
                    int(args[7]) if len(args) > 7 else 0,
                    int(args[8]) if len(args) > 8 else 0,
                    int(args[9]) if len(args) > 9 else 0,
                    int(args[10]) if len(args) > 10 else 0,
                )
            )  # yr, mon, d, hr, m, s, ss, shit,shit,shit
        except IndexError:
            ljinux.based.error(1)
        del rtc
    else:
        raise IndexError
except IndexError:
    tt = time.localtime()
    dat = [
        tt.tm_mday,
        tt.tm_mon,
        tt.tm_hour,
        tt.tm_min,
        tt.tm_sec,
    ]

    for i in range(0, 5):
        dat[i] = f"0{dat[i]}" if len(str(dat[i])) < 2 else dat[i]

    daydict = {
        0: "Mon",
        1: "Tue",
        2: "Wed",
        3: "Thu",
        4: "Fri",
        5: "Sat",
        6: "Sun",
    }
    day = daydict[tt.tm_wday]
    del daydict

    term.write(f"{day} {dat[0]} {dat[1]} {tt.tm_year} {dat[2]}:{dat[3]}:{dat[4]}")
    del tt, day, dat
del args
