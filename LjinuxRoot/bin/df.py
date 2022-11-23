from os import statvfs

dfr = statvfs("/")  # board
dfl = statvfs("/LjinuxRoot")  # LjinuxRoot
dfd = dfr == dfl  # is ljinuxRoot on board?
del statvfs

opts = ljinux.api.xarg()


def human_readable(whatever):
    if whatever < 1024:  # kb
        return f"{int(whatever)}b"
    elif whatever < 1048576:  # mb
        return f"{int(whatever/1024)}K"
    elif whatever < 1073741824:  # gb
        return f"{int(whatever/1048576)}M"
    else:
        return f"{int(whatever/1073741824)}G"


if dfd:
    # get values in bytes
    free = dfr[1] * dfr[3]
    total = dfr[1] * dfr[2]
    used = total - free

    bs = 2
    bs_sps = " " * bs

    vfree = (human_readable(free) if "h" in opts["o"] else str(free)) + bs_sps
    vtotal = (human_readable(total) if "h" in opts["o"] else str(total)) + bs_sps
    vused = (human_readable(used) if "h" in opts["o"] else str(used)) + bs_sps
    vperc = str(int(used * 100 / total)) + "%"

    tl = len(vtotal[:-bs])
    ul = len(vused[:-bs])
    fl = len(vfree[:-bs])
    pl = len(vperc[:-bs])

    sps = [bs_sps] * 4
    del bs_sps

    if tl < 4:
        vtotal += " " * (4 - tl)
    else:
        sps[0] += (tl - 4) * " "
    del tl

    if ul < 4:
        vused += " " * (4 - ul)
    else:
        sps[1] += (ul - 4) * " "
    del ul

    if fl < 5:
        vfree += " " * (5 - fl)
    else:
        sps[2] += (fl - 5) * " "
    del fl

    if pl < 4:
        vperc += " " * (4 - pl)
    else:
        sps[3] += (pl - 4) * " "
    del pl, free, total, used, bs

    term.write(
        f"Filesystem      Size{sps[0]}Used{sps[1]}Avail{sps[2]}Use%{sps[3]}Mounted on\n"
        + f"/LjinuxRoot     {vtotal}{vused}{vfree}{vperc}/"
    )

    del vfree, vtotal, vused, vperc, sps
else:
    print("Not implemented")

ljinux.api.setvar("return", "0")
del dfr, dfl, dfd, human_readable, opts
