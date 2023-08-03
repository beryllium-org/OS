rename_process("modprobe")
pv[get_pid()]["args"] = ljinux.based.user_vars["argj"].split()[1:]
pv[get_pid()]["argl"] = len(pv[get_pid()]["args"])
if pv[get_pid()]["argl"] is not 0:
    pv[get_pid()]["module"] = pv[get_pid()]["args"][0]
    pv[get_pid()]["ass"] = None
    try:
        if pv[get_pid()]["args"][1] == "as":
            pv[get_pid()]["ass"] = pv[get_pid()]["args"][2]
    except IndexError:
        pass
    pv[get_pid()]["loadstr"] = "from drivers.{} import {}".format(
        pv[get_pid()]["module"], pv[get_pid()]["module"]
    )
    pv[get_pid()]["dmtextt"] = 'Modprobe: Loading module "{}"'.format(
        pv[get_pid()]["module"]
    )

    if pv[get_pid()]["ass"] is not None:
        pv[get_pid()]["module"] = pv[get_pid()]["ass"]
        pv[get_pid()]["loadstr"] += " as " + pv[get_pid()]["module"]
        pv[get_pid()]["dmtextt"] += " as " + pv[get_pid()]["module"]

    dmtex(pv[get_pid()]["dmtextt"])
    try:
        exec(pv[get_pid()]["loadstr"])
        if pv[get_pid()]["module"] not in ljinux.modules:
            pv[get_pid()]["execstr"] = (
                'ljinux.modules.update({"'
                + pv[get_pid()]["module"]
                + '": '
                + pv[get_pid()]["module"]
                + "()})"
            )
            exec(pv[get_pid()]["execstr"])
        else:
            ljinux.based.error()
    except ImportError:
        ljinux.based.error()
else:
    ljinux.based.error(1)
