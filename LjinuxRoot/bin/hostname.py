rename_process("hostname")
vr("opts", ljinux.api.xarg())

if "help" in vr("opts")["o"] or "h" in vr("opts")["o"]:
    ljinux.based.run("cat /usr/share/help/hostname.txt")
elif "version" in vr("opts")["o"] or "V" in vr("opts")["o"]:
    term.write("LNL Hostname 0.0.2")
elif len(vr("opts")["w"]) > 0:
    ljinux.based.system_vars["HOSTNAME"] = vr("opts")["w"][0]
    with ljinux.api.fopen("/etc/hostname", "w") as pv[get_pid()]["hs"]:
        if vr("hs") is not None:
            vr("hs").write(vr("opts")["w"][0] + "\n")
        else:
            ljinux.based.error(7, prefix=f"{colors.red_t}Hostname{colors.endc}")
else:
    term.write(ljinux.api.getvar("HOSTNAME"))

if "network" in ljinux.modules:
    ljinux.modules["network"].hostname(ljinux.api.getvar("HOSTNAME"))
