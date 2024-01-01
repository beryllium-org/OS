rename_process("wget")
vr("args", ljinux.based.user_vars["argj"].split())
vr("argc", len(vr("args")))
if "network" in ljinux.modules and ljinux.modules["network"].connected:
    if vr("argc") > 1:
        vr(
            "nam",
            (
                vr("args")[1][vr("args")[1].rfind("/") + 1 :]
                if vr("argc") < 3
                else vr("args")[2]
            ),
        )
        with ljinux.api.fopen(vr("nam"), "wb") as pv[get_pid()]["filee"]:
            if vr("filee") is not None:
                vr("filee").write(ljinux.modules["network"].get(vr("args")[1]).content)
            else:
                ljinux.based.error(7)
        ljinux.modules["network"].reset_session()
    else:
        ljinux.based.error(9)
else:
    ljinux.based.error(5)
