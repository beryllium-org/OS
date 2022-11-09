opts = ljinux.api.xarg()
li = opts["hw"] + opts["w"]
co = "".join(opts["o"])

sps = "   "
path = "./"

was_held = False
if term.hold_stdout:
    was_held = True
else:
    term.hold_stdout = True

if len(li):
    if ljinux.api.isdir(li[0]) is 1:
        path = li[0]
        if not path.endswith("/"):
            path += "/"
    else:
        ljinux.based.error(2)

path = ljinux.api.betterpath(path)
directory_listing = listdir(path)

if "l" in co:
    sps = "\n"

if "a" in co:
    term.write(colors.green_t + "." + colors.endc, end=sps)
    if not (path == "/" or (path == "./" and getcwd() == "/")):
        term.write(colors.green_t + ".." + colors.endc, end=sps)

if directory_listing is not None:
    for dir in directory_listing:
        col = "" if ljinux.api.isdir(f"{path}{dir}") is 0 else colors.okcyan
        if dir[:1] == "." and not "a" in co:
            continue
        else:
            term.write(col + dir + colors.endc, end=sps)
        del col

if not "l" in co:
    term.write()

ljinux.api.setvar("return", "0")

if not was_held:
    term.hold_stdout = False
    term.flush_writes()

del was_held, sps, path, directory_listing, opts, li, co
