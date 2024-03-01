rename_process("echo")
vr("opts", be.api.xarg())
be.api.setvar("return", "")

vr("li", vr("opts")["hw"] + vr("opts")["w"])
for pv[get_pid()]["i"] in vr("li"):
    be.based.user_vars["return"] += vr("i") + " "

be.api.setvar("return", be.based.user_vars["return"][:-1])

if "n" not in vr("opts")["o"]:
    be.based.user_vars["return"] += "\n"

if not be.based.silent:
    term.nwrite(be.based.user_vars["return"])
