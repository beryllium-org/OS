rename_process("df")
from os import statvfs

pv[get_pid()]["dfr"] = statvfs("/")  # board
pv[get_pid()]["dfl"] = statvfs("/LjinuxRoot")  # LjinuxRoot
del statvfs
pv[get_pid()]["dfd"] = (
    pv[get_pid()]["dfr"] == pv[get_pid()]["dfl"]
)  # is ljinuxRoot on board?

pv[get_pid()]["opts"] = ljinux.api.xarg()


def human_readable(whatever):
    if whatever < 1024:  # kb
        return f"{int(whatever)}b"
    elif whatever < 1048576:  # mb
        return f"{int(whatever/1024)}K"
    elif whatever < 1073741824:  # gb
        return f"{int(whatever/1048576)}M"
    else:
        return f"{int(whatever/1073741824)}G"


if pv[get_pid()]["dfd"]:
    # get values in bytes
    pv[get_pid()]["free"] = pv[get_pid()]["dfr"][1] * pv[get_pid()]["dfr"][3]
    pv[get_pid()]["total"] = pv[get_pid()]["dfr"][1] * pv[get_pid()]["dfr"][2]
    pv[get_pid()]["used"] = pv[get_pid()]["total"] - pv[get_pid()]["free"]

    pv[get_pid()]["bs"] = 2
    pv[get_pid()]["bs_sps"] = " " * pv[get_pid()]["bs"]

    pv[get_pid()]["vfree"] = (
        human_readable(pv[get_pid()]["free"])
        if "h" in pv[get_pid()]["opts"]["o"]
        else str(pv[get_pid()]["free"])
    ) + pv[get_pid()]["bs_sps"]
    pv[get_pid()]["vtotal"] = (
        human_readable(pv[get_pid()]["total"])
        if "h" in pv[get_pid()]["opts"]["o"]
        else str(pv[get_pid()]["total"])
    ) + pv[get_pid()]["bs_sps"]
    pv[get_pid()]["vused"] = (
        human_readable(pv[get_pid()]["used"])
        if "h" in pv[get_pid()]["opts"]["o"]
        else str(pv[get_pid()]["used"])
    ) + pv[get_pid()]["bs_sps"]
    pv[get_pid()]["vperc"] = (
        str(int(pv[get_pid()]["used"] * 100 / pv[get_pid()]["total"])) + "%"
    )

    pv[get_pid()]["tl"] = len(pv[get_pid()]["vtotal"][: -pv[get_pid()]["bs"]])
    pv[get_pid()]["ul"] = len(pv[get_pid()]["vused"][: -pv[get_pid()]["bs"]])
    pv[get_pid()]["fl"] = len(pv[get_pid()]["vfree"][: -pv[get_pid()]["bs"]])
    pv[get_pid()]["pl"] = len(pv[get_pid()]["vperc"][: -pv[get_pid()]["bs"]])

    pv[get_pid()]["sps"] = [pv[get_pid()]["bs_sps"]] * 4

    if pv[get_pid()]["tl"] < 4:
        pv[get_pid()]["vtotal"] += " " * (4 - pv[get_pid()]["tl"])
    else:
        pv[get_pid()]["sps"][0] += (pv[get_pid()]["tl"] - 4) * " "

    if pv[get_pid()]["ul"] < 4:
        pv[get_pid()]["vused"] += " " * (4 - pv[get_pid()]["ul"])
    else:
        pv[get_pid()]["sps"][1] += (pv[get_pid()]["ul"] - 4) * " "

    if pv[get_pid()]["fl"] < 5:
        pv[get_pid()]["vfree"] += " " * (5 - pv[get_pid()]["fl"])
    else:
        pv[get_pid()]["sps"][2] += (pv[get_pid()]["fl"] - 5) * " "

    if pv[get_pid()]["pl"] < 4:
        pv[get_pid()]["vperc"] += " " * (4 - pv[get_pid()]["pl"])
    else:
        pv[get_pid()]["sps"][3] += (pv[get_pid()]["pl"] - 4) * " "

    term.write(
        "Filesystem      Size{}Used{}Avail{}Use%{}Mounted on\n".format(
            pv[get_pid()]["sps"][0],
            pv[get_pid()]["sps"][1],
            pv[get_pid()]["sps"][2],
            pv[get_pid()]["sps"][3],
        )
        + "/LjinuxRoot     {}{}{}{}/".format(
            pv[get_pid()]["vtotal"],
            pv[get_pid()]["vused"],
            pv[get_pid()]["vfree"],
            pv[get_pid()]["vperc"],
        )
    )
else:
    term.write("Not implemented")

ljinux.api.setvar("return", "0")
del human_readable
