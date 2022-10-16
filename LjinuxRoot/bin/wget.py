args = ljinux.based.user_vars["argj"].split()
argc = len(args)
if "network" in ljinux.modules and ljinux.modules["network"].connected:
    if argc > 1:
        nam = args[1][args[1].rfind("/") + 1 :] if argc < 3 else args[2]
        with ljinux.api.fopen(nam, "wb") as filee:
            if filee is not None:
                filee.write(ljinux.modules["network"].get(args[1]).content)
            else:
                ljinux.based.error(7)
        ljinux.modules["network"].resetsock()
        del nam
    else:
        ljinux.based.error(9)
else:
    ljinux.based.error(5)
del args, argc
