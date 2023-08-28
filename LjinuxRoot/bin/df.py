rename_process("df")
from os import statvfs

vr("dfr", statvfs("/"))  # board
vr("dfl", statvfs("/LjinuxRoot"))  # LjinuxRoot
del statvfs

vr("dfd", (pv[get_pid()]["dfr"] == pv[get_pid()]["dfl"]))  # is ljinuxroot on board?

vr("opts", ljinux.api.xarg())


def human_readable(whatever):
    if whatever < 1024:  # kb
        return f"{int(whatever)}b"
    elif whatever < 1048576:  # mb
        return f"{int(whatever/1024)}K"
    elif whatever < 1073741824:  # gb
        return f"{int(whatever/1048576)}M"
    else:
        return f"{int(whatever/1073741824)}G"


if vr("dfd"):
    # get values in bytes
    vr("free", vr("dfr")[1] * vr("dfr")[3])
    vr("total", vr("dfr")[1] * vr("dfr")[2])
    vr("used", vr("total") - vr("free"))

    vr("bs", 2)
    vr("bs_sps", " " * vr("bs"))

    vr(
        "vfree",
        (human_readable(vr("free")) if "h" in vr("opts")["o"] else str(vr("free")))
        + vr("bs_sps"),
    )
    vr(
        "vtotal",
        (human_readable(vr("total")) if "h" in vr("opts")["o"] else str(vr("total")))
        + vr("bs_sps"),
    )
    vr(
        "vused",
        (human_readable(vr("used")) if "h" in vr("opts")["o"] else str(vr("used")))
        + vr("bs_sps"),
    )
    vr("vperc", (str(int(vr("used") * 100 / vr("total"))) + "%"))

    vr("tl", len(vr("vtotal")[: -vr("bs")]))
    vr("ul", len(vr("vused")[: -vr("bs")]))
    vr("fl", len(vr("vfree")[: -vr("bs")]))
    vr("pl", len(vr("vperc")[: -vr("bs")]))

    vr("sps", [vr("bs_sps")] * 4)

    if vr("tl") < 4:
        pv[get_pid()]["vtotal"] += " " * (4 - vr("tl"))
    else:
        pv[get_pid()]["sps"][0] += (vr("tl") - 4) * " "

    if vr("ul") < 4:
        pv[get_pid()]["vused"] += " " * (4 - vr("ul"))
    else:
        pv[get_pid()]["sps"][1] += (vr("ul") - 4) * " "

    if vr("fl") < 5:
        pv[get_pid()]["vfree"] += " " * (5 - vr("fl"))
    else:
        pv[get_pid()]["sps"][2] += (vr("fl") - 5) * " "

    if vr("pl") < 4:
        pv[get_pid()]["vperc"] += " " * (4 - vr("pl"))
    else:
        pv[get_pid()]["sps"][3] += (vr("pl") - 4) * " "

    term.write(
        "Filesystem      Size{}Used{}Avail{}Use%{}Mounted on\n".format(
            vr("sps")[0],
            vr("sps")[1],
            vr("sps")[2],
            vr("sps")[3],
        )
        + "/LjinuxRoot     {}{}{}{}/".format(
            vr("vtotal"),
            vr("vused"),
            vr("vfree"),
            vr("vperc"),
        )
    )
else:
    term.write("Not implemented")

ljinux.api.setvar("return", "0")
del human_readable
