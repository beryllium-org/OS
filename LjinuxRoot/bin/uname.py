try:
    if ljinux.based.user_vars["argj"].split()[1] == "-a":
        tt = time.localtime()
        print(
            "Ljinux {} {} {}/{}/{} {}:{}:{} circuitpython Ljinux".format(
                ljinux.based.system_vars["BOARD"],
                ljinux.based.system_vars["VERSION"],
                tt.tm_mday, tt.tm_mon, tt.tm_year,
                tt.tm_hour, tt.tm_min, tt.tm_sec
            )
        )
        del tt
except IndexError:
    print("Ljinux")
ljinux.based.user_vars["return"] = "0"
