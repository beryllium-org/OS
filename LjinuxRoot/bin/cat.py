ljinux.based.user_vars["return"] = ""
try:
    with open(ljinux.based.user_vars["argj"].split()[1],'r') as f:
        lines = f.readlines()
        for i in lines:
            print(i,end="")
            ljinux.based.user_vars["return"] += i
        f.close()
        gc.collect()
except OSError:
    ljinux.based.error(4)
    ljinux.based.user_vars["return"] = "1"
except IndexError:
    ljinux.based.error(1)
    ljinux.based.user_vars["return"] = "1"