opts = ljinux.api.xarg(ljinux.based.user_vars["argj"], False)
mod = opts["n"][opts["n"].rfind("/") + 1 :]

lines = 10 if not ("n" in opts["o"]) else int(opts["o"]["n"])

try:
    with open(ljinux.api.betterpath(opts["w"][0]), "r") as f:
        content = f.readlines()
        count = len(content)
        start = 0 if mod == "head.lja" else count - lines
        end = lines if mod == "head.lja" else count - 1
        for item in content[start:end]:
            print(item, end="")
        if mod == "tail.lja":
            print(content[-1])
        del content, count, start, end
        ljinux.based.user_vars["return"] = "0"
except OSError:
    ljinux.based.error(4, filee)
    ljinux.based.user_vars["return"] = "1"
except IndexError:
    ljinux.based.error(9)
    ljinux.based.user_vars["return"] = "1"

del lines, opts, mod
