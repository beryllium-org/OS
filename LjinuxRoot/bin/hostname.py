rename_process("hostname")
pv[get_pid()]["opts"] = ljinux.api.xarg()

if len(pv[get_pid()]["opts"]["w"]) > 0:
    ljinux.based.system_vars["HOSTNAME"] = pv[get_pid()]["opts"]["w"][0]
    # Replace with setvar when setvar tries to sudo.
else:
    term.write(ljinux.api.getvar("HOSTNAME"))

if "network" in ljinux.modules:
    ljinux.modules["network"].hostname(ljinux.api.getvar("HOSTNAME"))
