rename_process("preload")
vr("opts", be.api.xarg())
if "help" in vr("opts")["o"] or "h" in vr("opts")["o"]:
    term.write("Usage: preload [filename..]\n\n")
else:
    if use_compiler:
        for pv[get_pid()]["i"] in vr("opts")["w"]:
            with be.api.fs.open(vr("i")) as pv[get_pid()]["f"]:
                if vr("f") is None:
                    be.based.error(
                        4, vr("i"), prefix=colors.error + "Preload" + colors.endc
                    )
                    be.api.setvar("return", "1")
                    break
                else:
                    vr("prog", vr("f").read())
                    vr("prog", compile(vr("prog"), "preload", "exec"))
                    be.code_cache[be.api.fs.resolve(vr("i"))] = vr("prog")
    else:
        term.write("Compiler unavailable.")
be.api.setvar("return", "0")
