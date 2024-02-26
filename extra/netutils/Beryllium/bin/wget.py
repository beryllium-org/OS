rename_process("wget")
vr("args", be.based.user_vars["argj"].split())
vr("argc", len(vr("args")))
if "network" in be.devices and be.devices["network"][0].connected:
    if vr("argc") > 1:
        vr(
            "nam",
            (
                vr("args")[1][vr("args")[1].rfind("/") + 1 :]
                if vr("argc") < 3
                else vr("args")[2]
            ),
        )
        with be.api.fopen(vr("nam"), "wb") as pv[get_pid()]["filee"]:
            if vr("filee") is not None:
                vr("filee").write(be.devices["network"][0].get(vr("args")[1]).content)
            else:
                be.based.error(7)
        be.devices["network"][0].reset_session()
    else:
        be.based.error(9)
else:
    be.based.error(5)
