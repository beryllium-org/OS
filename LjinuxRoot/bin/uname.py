try:
    if ljinux.based.user_vars["argj"].split()[1] == "-a":
        tt = time.localtime()
        print(
            "Ljinux Raspberry Pi Pico "
            + ljinux.based.system_vars["Version"]
            + " "
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
            + " circuitpython Ljinux"
        )
        del tt
except IndexError:
    print("Ljinux")
ljinux.based.user_vars["return"] = "0"
