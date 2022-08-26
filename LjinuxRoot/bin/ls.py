argss_in = {}
args = ljinux.based.user_vars["argj"].split()[1:]
argl = len(args)
if argl > 0 and args[0][0] == "-":
    argss_in = list(args[0][1:])
    argl -= 1
    args = args[1:]

rett = ""
sps = "   "
path = "."

directory_listing = None
if not argl:
    directory_listing = listdir()
elif ljinux.based.fn.isdir(args[0]) is 1:
    path = ljinux.based.fn.betterpath(args[0])
    directory_listing = listdir(path)
else:
    ljinux.based.error(2)

if "l" in argss_in:
    sps = "\n"

if "a" in argss_in:
    print(colors.green_t + "." + colors.endc, end=sps)
    rett += "." + sps
    print(colors.green_t + ".." + colors.endc, end=sps)
    rett += ".." + sps

if directory_listing is not None:
    for dir in directory_listing:
        if dir[:1] == "." and not "a" in argss_in:
            continue
        else:
            print(colors.magenta_t + dir + colors.endc, end=sps)
            rett += dir + sps

if not "l" in argss_in:
    print()
    rett += "\n"

ljinux.based.user_vars["return"] = rett
del sps, rett, directory_listing, argss_in, args, argl, path
