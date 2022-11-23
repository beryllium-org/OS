opts = ljinux.api.xarg()

if len(opts["w"]) > 0:
    ljinux.api.setvar("HOSTNAME", opts["w"][0])
else:
    term.write(ljinux.api.getvar("HOSTNAME"))
del opts

if "network" in ljinux.modules:
    ljinux.modules["network"].hostname(ljinux.api.getvar("HOSTNAME"))
