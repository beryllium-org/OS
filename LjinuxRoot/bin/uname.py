try:
    if ljinux.based.user_vars["argj"].split()[1] == "-a":
        tt = time.localtime()
        dat = [
            ljinux.based.system_vars["BOARD"],
            ljinux.based.system_vars["VERSION"],
            tt.tm_year,
            tt.tm_mday,
            tt.tm_mon,
            tt.tm_hour,
            tt.tm_min,
            tt.tm_sec,
        ]

        for i in range(3, 8):
            dat[i] = f"0{dat[i]}" if len(str(dat[i])) < 2 else dat[i]
        del i

        print(
            f"Ljinux {dat[0]} {dat[1]} {dat[3]}/{dat[4]}/{dat[2]} {dat[5]}:{dat[6]}:{dat[7]} circuitpython Ljinux"
        )
        del tt, dat
except IndexError:
    print("Ljinux")
ljinux.based.user_vars["return"] = "0"
