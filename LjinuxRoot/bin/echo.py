rename_process("echo")
pv[get_pid()]["opts"] = ljinux.api.xarg()
ljinux.api.setvar("return", "")

pv[get_pid()]["li"] = pv[get_pid()]["opts"]["hw"] + pv[get_pid()]["opts"]["w"]
for pv[get_pid()]["i"] in pv[get_pid()]["li"]:
    ljinux.based.user_vars["return"] += pv[get_pid()]["i"] + " "

ljinux.api.setvar("return", ljinux.based.user_vars["return"][:-1])

if "n" not in pv[get_pid()]["opts"]["o"]:
    ljinux.based.user_vars["return"] += "\n"

if not ljinux.based.silent:
    term.nwrite(ljinux.based.user_vars["return"])
