rename_process("touch")
vr("opts", ljinux.api.xarg())

for pv[get_pid()]["i"] in vr("opts")["w"]:
    if ljinux.api.isdir(vr("i")) != 2:
        ljinux.based.error(10)
    else:
        with ljinux.api.fopen(vr("i"), "w") as pv[get_pid()]["f"]:
            if vr("f") is None:
                ljinux.based.error(7)
