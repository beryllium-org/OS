rename_process("preload")
vr("opts", ljinux.api.xarg())
if "help" in vr("opts")["o"] or "-h" in vr("opts")["o"]:
    term.write("Usage: preload [filename..]\n\n")
else:
    if use_compiler:
        for pv[get_pid()]["i"] in vr("opts")["w"]:
            with ljinux.api.fopen(vr("i")) as pv[get_pid()]["f"]:
                if vr("f") is None:
                    ljinux.based.error(
                        4, vr("i"), prefix=colors.error + "Preload" + colors.endc
                    )
                    ljinux.api.setvar("return", "1")
                    break
                else:
                    vr("prog", vr("f").read())
                    vr("prog", compile(vr("prog"), "preload", "exec"))
                    ljinux.code_cache[ljinux.api.betterpath(vr("i"))] = vr("prog")
    else:
        term.write("Compiler unavailable.")
ljinux.api.setvar("return", "0")
