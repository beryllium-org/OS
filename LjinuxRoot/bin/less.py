try:
    with open(
        ljinux.based.fn.betterpath(ljinux.based.user_vars["argj"].split()[1]), "r"
    ) as f:

        # prep work
        lines = f.readlines()
        lines1 = []
        for i in lines:
            lines1.append(i.replace("\n", "") if i != "\n" else i)
        del lines
        gc.collect()
        gc.collect()
        sizee = term.detect_size()  # get the terminal size

        # line splitting
        lines2 = []
        for i in lines1:
            remaining = i
            while len(remaining) > 0:
                if len(remaining) > sizee[1]:
                    """
                    too long, has to be split
                    has to be a "while", for page long lines
                    """
                    lines2.append(remaining[: sizee[1]])
                    remaining = remaining[sizee[1] :]
                else:
                    lines2.append(remaining)
                    remaining = ""
            del remaining
            del i
        del lines1
        gc.collect()
        gc.collect()

        # remove spaces from start of line
        lines3 = []
        for i in lines2:
            lines3.append(i if not i.startswith(" ") else i[1:])
            del i
        del lines2
        gc.collect()
        gc.collect()

        # Ready for printing
        term.clear()

        for i in lines3:  # this is for testing only
            print(i)
            del i
        del lines3
        # target = sizee[0] - 1 if len(lines) > sizee[0] - 1 else len(lines) - 1
        # for i in range(0, target):
        #    print(lines[i], end="")
        # del f, target
    ljinux.based.user_vars["return"] += "0"
    stdout.write("\n")
    gc.collect()
    gc.collect()

except OSError:
    ljinux.based.error(4, ljinux.based.user_vars["argj"].split()[1])
    ljinux.based.user_vars["return"] = "1"

except IndexError:
    ljinux.based.error(1)
    ljinux.based.user_vars["return"] = "1"
