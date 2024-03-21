rename_process("hostname")
vr("opts", be.api.xarg())

if "help" in vr("opts")["o"] or "h" in vr("opts")["o"]:
    be.based.run("cat /usr/share/help/hostname.txt")
elif "version" in vr("opts")["o"] or "V" in vr("opts")["o"]:
    term.write("LNL Hostname 0.0.2")
elif len(vr("opts")["w"]) > 0:
    be.based.system_vars["HOSTNAME"] = vr("opts")["w"][0]
    with be.api.fs.open("/etc/hostname", "w") as pv[get_pid()]["hs"]:
        if vr("hs") is not None:
            vr("hs").write(vr("opts")["w"][0] + "\n")
        else:
            be.based.error(7, prefix=f"{colors.red_t}Hostname{colors.endc}")
else:
    term.write(be.api.getvar("HOSTNAME"))

if "network" in be.devices:
    be.devices["network"][0].hostname(be.api.getvar("HOSTNAME"))
