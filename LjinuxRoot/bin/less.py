try:
    with open(
        ljinux.based.fn.betterpath(ljinux.based.user_vars["argj"].split()[1]), "r"
    ) as f:
        lines = f.readlines()
        sizee = term.detect_size()
        term.clear()
        for i in lines:
            while len(i) - 1 > sizee[1]:
                """
                too long, has to be split
                has to be a "while", for stupid long lines
                """
                rest = i[sizee[1] - 1 :]
                i = i[: sizee[1] - 1]

        target = 0
        target = sizee[0] - 1 if len(lines) > sizee[0] - 1 else len(lines) - 1
        for i in range(0, target):
            print(lines[i], end="")
        del f, target
    ljinux.based.user_vars["return"] += "0"
    gc.collect()
    gc.collect()

except OSError:
    ljinux.based.error(4, ljinux.based.user_vars["argj"].split()[1])
    ljinux.based.user_vars["return"] = "1"

except IndexError:
    ljinux.based.error(1)
    ljinux.based.user_vars["return"] = "1"
