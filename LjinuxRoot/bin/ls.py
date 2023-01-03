opts = ljinux.api.xarg()
li = opts["hw"] + opts["w"]
co = "".join(opts["o"])
del opts

sps = "   "
path = "./"

if len(li):
    if ljinux.api.isdir(li[0]) is 1:
        path = li[0]
        if not path.endswith("/"):
            path += "/"
    else:
        ljinux.based.error(2)

directory_listing = listdir(ljinux.api.betterpath(path))
directory_listing.sort()

if "l" in co:
    sps = "\n"

if "a" in co:
    term.write(colors.green_t + "." + colors.endc, end=sps)
    if not (path == "/" or (path == "./" and getcwd() == "/")):
        term.write(colors.green_t + ".." + colors.endc, end=sps)

if directory_listing is not None:
    for dirr in directory_listing:
        col = ""
        if ljinux.api.isdir(f"{dirr}", path) is 0:
            if dirr.startswith("."):
                col = colors.green_t
        else:
            col = colors.okcyan
        if dirr[:1] == "." and not "a" in co:
            continue
        else:
            term.write(col + dirr + colors.endc, end=sps)
        del col, dirr

if not "l" in co:
    term.write()

ljinux.api.setvar("return", "0")

del sps, path, directory_listing, li, co
