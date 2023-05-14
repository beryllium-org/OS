inpt = ljinux.based.user_vars["argj"].split()

try:
    with open(ljinux.api.betterpath(inpt[1]), "r") as f:
        for line in f:
            term.nwrite(line)
            del line
        del f
        gc.collect()
    gc.collect()
    ljinux.api.setvar("return", "0")

except OSError:
    ljinux.based.error(4, inpt[1])
    ljinux.api.setvar("return", "1")

except IndexError:
    ljinux.based.error(1)
    ljinux.api.setvar("return", "1")

del inpt
