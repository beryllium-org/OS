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
        """
        we really do not have to check for terabytes
        on a microcontroller, RIGHT?
        """
        return f"{int(whatever/1073741824)}G"


if dfd:
    # get values in bytes
    free = dfr[1] * dfr[3]
    total = dfr[1] * dfr[2]
    used = total - free
    perc = str(int(used * 100 / total))

    # do -h
    # yes it has to be done now, so that they are most accurate
    print("Filesystem      Size  Used Avail Use% Mounted on")
    print(
        "/LjinuxRoot     "
        + (human_readable(total) if "h" in opts["o"] else str(total)),
        human_readable(used) if "h" in opts["o"] else str(used),
        human_readable(free) if "h" in opts["o"] else str(free),
        perc + "% /",
        sep="  ",
    )

    del free, total, used, perc

else:
    print("Not implemented")

del dfr, dfl, dfd, human_readable, opts
