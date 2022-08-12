args = ljinux.based.user_vars["argj"].split()[1:]
argl = len(args)
if argl is not 0:
    module = args[0]
    ass = None
    try:
        if args[1] == "as":
            ass = args[2]
    except IndexError:
        pass
    loadstr = f"from drivers.{module} import {module}"
    if ass is not None:
        module = ass
        loadstr += f" as {module}"
    del ass
    try:
        exec(loadstr)
        if module not in ljinux.modules:
            execstr = (
                "ljinux.modules.update({\"" +
                module +
                "\": " +
                module +
                "()})"
            )
            exec(execstr)
            del execstr
        else:
            ljinux.based.error()
    except ImportError:
        ljinux.based.error()
    del loadstr
else:
    ljinux.based.error(1)

del args, argl
