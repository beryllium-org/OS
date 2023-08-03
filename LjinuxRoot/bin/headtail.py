rename_process("headtail")  # Rename to headtail till we load opts

pv[get_pid()]["opts"] = ljinux.api.xarg(ljinux.based.user_vars["argj"], False)
pv[get_pid()]["mod"] = pv[get_pid()]["opts"]["n"][
    pv[get_pid()]["opts"]["n"].rfind("/") + 1 :
]
rename_process(pv[get_pid()]["mod"])  # Set name to current mode.
pv[get_pid()]["lines"] = (
    10
    if not ("n" in pv[get_pid()]["opts"]["o"])
    else int(pv[get_pid()]["opts"]["o"]["n"])
)

pv[get_pid()]["held"] = False  # Was stdout suppressed already?
if term.hold_stdout:
    pv[get_pid()]["held"] = True
else:
    term.hold_stdout = True

try:
    with ljinux.api.fopen(pv[get_pid()]["opts"]["w"][0], "r") as f:
        pv[get_pid()]["content"] = f.readlines()
        pv[get_pid()]["count"] = len(pv[get_pid()]["content"])
        pv[get_pid()]["start"] = (
            0
            if pv[get_pid()]["mod"] == "head"
            else pv[get_pid()]["count"] - pv[get_pid()]["lines"]
        )
        pv[get_pid()]["end"] = (
            pv[get_pid()]["lines"]
            if pv[get_pid()]["mod"] == "head"
            else pv[get_pid()]["count"] - 1
        )
        for pv[get_pid()]["item"] in pv[get_pid()]["content"][
            pv[get_pid()]["start"] : pv[get_pid()]["end"]
        ]:
            term.nwrite(pv[get_pid()]["item"])
        if pv[get_pid()]["mod"] == "tail":
            term.write(pv[get_pid()]["content"][-1])
        ljinux.api.setvar("return", "0")
except OSError:
    ljinux.based.error(4, filee)
    ljinux.api.setvar("return", "1")
except IndexError:
    ljinux.based.error(9)
    ljinux.api.setvar("return", "1")
if not pv[get_pid()]["held"]:
    term.hold_stdout = False
    term.flush_writes()
