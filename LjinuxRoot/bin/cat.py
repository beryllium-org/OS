inpt = ljinux.based.user_vars["argj"].split()

was_held = False
if term.hold_stdout:
    was_held = True
else:
    term.hold_stdout = True


try:
    with open(ljinux.api.betterpath(inpt[1]), "r") as f:
        for line in f:
            term.write(line, end="")
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

if not was_held:
    term.hold_stdout = False
    term.flush_writes()

del was_held, inpt
