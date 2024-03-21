rename_process("touch")
vr("opts", be.api.xarg())

for pv[get_pid()]["i"] in vr("opts")["w"]:
    if be.api.isdir(vr("i")) != 2:
        be.based.error(10)
    else:
        with be.api.fs.open(vr("i"), "w") as pv[get_pid()]["f"]:
            if vr("f") is None:
                be.based.error(7)
