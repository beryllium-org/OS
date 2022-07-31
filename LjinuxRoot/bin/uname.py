try:
    if ljinux.based.user_vars["argj"].split()[1] == "-a":
        tt = time.localtime()
        print(
            f"lJinux { ljinux.based.system_vars['BOARD'] } { ljinux.based.system_vars['VERSION'] }"
            + f" {tt.tm_mday}/{tt.tm_mon}/{tt.tm_year} {tt.tm_hour}:{tt.tm_min}:{tt.tm_sec}"
            + " circuitpython Ljinux"
        )
        del tt
except IndexError:
    print("lJinux")
ljinux.based.user_vars["return"] = "0"
