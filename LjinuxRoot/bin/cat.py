ljinux.based.user_vars["return"] = ""

try:
    with open(ljinux.based.user_vars["argj"].split()[1], "r") as f:
        lines = f.readlines()
        for line in lines:
            print(line, end="")
            ljinux.based.user_vars["return"] += line
            del line
        del lines, f
    gc.collect()
    gc.collect()

except OSError:
    ljinux.based.error(4, ljinux.based.user_vars["argj"].split()[1])
    ljinux.based.user_vars["return"] = "1"

except IndexError:
    ljinux.based.error(1)
    ljinux.based.user_vars["return"] = "1"
