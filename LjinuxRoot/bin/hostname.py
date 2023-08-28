rename_process("hostname")
vr("opts", ljinux.api.xarg())

if len(vr("opts")["w"]) > 0:
    ljinux.based.system_vars["HOSTNAME"] = vr("opts")["w"][0]
    # Replace with setvar when setvar tries to sudo.
else:
    term.write(ljinux.api.getvar("HOSTNAME"))

if "network" in ljinux.modules:
    ljinux.modules["network"].hostname(ljinux.api.getvar("HOSTNAME"))
