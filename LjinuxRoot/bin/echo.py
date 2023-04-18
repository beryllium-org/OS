opts = ljinux.api.xarg()
ljinux.api.setvar("return", "")

li = opts["hw"] + opts["w"]
for i in li:
    ljinux.based.user_vars["return"] += i + " "
    del i
del li

ljinux.api.setvar("return", ljinux.based.user_vars["return"][:-1])

if "n" not in opts["o"]:
    ljinux.based.user_vars["return"] += "\n"

del opts

if not ljinux.based.silent:
    term.nwrite(ljinux.based.user_vars["return"])
