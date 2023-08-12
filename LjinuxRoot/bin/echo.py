rename_process("echo")
vr("opts", ljinux.api.xarg())
ljinux.api.setvar("return", "")

vr("li", vr("opts")["hw"] + vr("opts")["w"])
for pv[get_pid()]["i"] in vr("li"):
    ljinux.based.user_vars["return"] += vr("i") + " "

ljinux.api.setvar("return", ljinux.based.user_vars["return"][:-1])

if "n" not in vr("opts")["o"]:
    ljinux.based.user_vars["return"] += "\n"

if not ljinux.based.silent:
    term.nwrite(ljinux.based.user_vars["return"])
