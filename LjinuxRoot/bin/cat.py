ljinux.api.setvar("return", "")
inpt = ljinux.based.user_vars["argj"].split()

try:
    with open(ljinux.api.betterpath(inpt[1]), "r") as f:
        for line in f:
            print(line, end="")
            ljinux.based.user_vars["return"] += line
            del line
        del f
    gc.collect()
    gc.collect()

except OSError:
    ljinux.based.error(4, inpt[1])
    ljinux.api.setvar("return", "1")

except IndexError:
    ljinux.based.error(1)
    ljinux.api.setvar("return", "1")
del inpt
