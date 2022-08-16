args2 = ljinux.based.user_vars["argj"].split()[1:]
argl2 = len(args)
# name change required, so that it won't conflict with the nested execution of jz and mkdir
if "network" in ljinux.modules and ljinux.modules["network"].connected == True:
    if argl2 > 0:
        randomm = None
        del randomm
    else:
        ljinux.based.error(1)
        ljinux.based.user_vars["return"] = "1"
else:
    ljinux.based.error(5)
    ljinux.based.user_vars["return"] = "1"

del args, argl
