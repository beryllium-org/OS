rename_process("headtail")  # Rename to headtail till we load opts

vr("opts", ljinux.api.xarg())
vr("mod", vr("opts")["n"][vr("opts")["n"].rfind("/") + 1 :])

rename_process(pv[get_pid()]["mod"])  # Set name to current mode.

vr("lines", (10 if not ("n" in vr("opts")["o"]) else int(vr("opts")["o"]["n"])))

vr("held", False)  # Was stdout suppressed already?
if term.hold_stdout:
    vr("held", True)
else:
    term.hold_stdout = True

try:
    with ljinux.api.fopen(vr("opts")["w"][0], "r") as pv[get_pid()]["f"]:
        vr("content", vr("f").readlines())
        vr("count", len(vr("content")))
        vr("start", (0 if vr("mod") == "head" else vr("count") - vr("lines")))
        vr("end", (vr("lines") if vr("mod") == "head" else vr("count") - 1))
        for pv[get_pid()]["item"] in vr("content")[vr("start") : vr("end")]:
            term.nwrite(vr("item"))
        if vr("mod") == "tail":
            term.write(vr("content")[-1])
        ljinux.api.setvar("return", "0")
except OSError:
    ljinux.based.error(4, vr("opts")["w"][0])
    ljinux.api.setvar("return", "1")
except IndexError:
    ljinux.based.error(9)
    ljinux.api.setvar("return", "1")
if not vr("held"):
    term.hold_stdout = False
    term.flush_writes()
