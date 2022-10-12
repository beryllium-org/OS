ljinux.based.user_vars["return"] = ""

try:
    with open(
        ljinux.api.betterpath(ljinux.based.user_vars["argj"].split()[1]), "r"
    ) as f:
        for line in f:
            print(line, end="")
            ljinux.based.user_vars["return"] += line
            del line
        del f
    gc.collect()
    gc.collect()

except OSError:
    ljinux.based.error(4, ljinux.based.user_vars["argj"].split()[1])
    ljinux.based.user_vars["return"] = "1"

except IndexError:
    ljinux.based.error(1)
    ljinux.based.user_vars["return"] = "1"
