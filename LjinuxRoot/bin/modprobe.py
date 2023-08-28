rename_process("modprobe")
vr("args", ljinux.based.user_vars["argj"].split()[1:])
vr("argl", len(vr("args")))
if vr("argl") is not 0:
    vr("module", vr("args")[0])
    vr("ass", None)
    try:
        if vr("args")[1] == "as":
            vr("ass", vr("args")[2])
    except IndexError:
        pass
    vr("loadstr", "from drivers.{} import {}".format(vr("module"), vr("module")))
    vr("dmtextt", 'Modprobe: Loading module "{}"'.format(vr("module")))

    if vr("ass") is not None:
        vr("module", vr("ass"))
        vrp("loadstr", " as " + vr("module"))
        vrp("dmtextt", " as " + vr("module"))

    dmtex(vr("dmtextt"))
    try:
        exec(vr("loadstr"))
        if vr("module") not in ljinux.modules:
            vr(
                "execstr",
                (
                    'ljinux.modules.update({"'
                    + vr("module")
                    + '": '
                    + vr("module")
                    + "()})"
                ),
            )
            exec(vr("execstr"))
        else:
            ljinux.based.error()
    except ImportError:
        ljinux.based.error()
else:
    ljinux.based.error(1)
