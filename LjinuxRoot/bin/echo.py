opts = ljinux.based.fn.xarg(ljinux.based.user_vars["argj"])
ljinux.based.user_vars["return"] = ""

li = opts["hw"] + opts["w"]
for i in li:
    ljinux.based.user_vars["return"] += i + " "
    del i
del li

ljinux.based.user_vars["return"] = ljinux.based.user_vars["return"][:-1]

if "n" not in opts["o"]:
    ljinux.based.user_vars["return"] += "\n"

del opts

if not ljinux.based.silent:
    stdout.write(ljinux.based.user_vars["return"])
