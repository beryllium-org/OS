rename_process("wget")
pv[get_pid()]["args"] = ljinux.based.user_vars["argj"].split()
pv[get_pid()]["argc"] = len(args)
if "network" in ljinux.modules and ljinux.modules["network"].connected:
    if pv[get_pid()]["argc"] > 1:
        pv[get_pid()]["nam"] = (
            pv[get_pid()]["args"][1][pv[get_pid()]["args"][1].rfind("/") + 1 :]
            if pv[get_pid()]["argc"] < 3
            else pv[get_pid()]["args"][2]
        )
        with ljinux.api.fopen(pv[get_pid()]["nam"], "wb") as pv[get_pid()]["filee"]:
            if pv[get_pid()]["filee"] is not None:
                pv[get_pid()]["filee"].write(
                    ljinux.modules["network"].get(pv[get_pid()]["args"][1]).content
                )
            else:
                ljinux.based.error(7)
        ljinux.modules["network"].resetsock()
    else:
        ljinux.based.error(9)
else:
    ljinux.based.error(5)
