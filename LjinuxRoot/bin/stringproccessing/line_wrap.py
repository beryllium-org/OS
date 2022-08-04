ljinux.based.user_vars["output"] = []
for i in ljinux.based.user_vars["input"]:
    remaining = i
    if remaining != "":
        while len(remaining) > 0:
            if len(remaining) > sizee[1]:
                """
                too long, has to be split
                has to be a "while", for page long lines
                """
                ljinux.based.user_vars["output"].append(remaining[: sizee[1]])
                remaining = remaining[sizee[1] :]
            else:
                ljinux.based.user_vars["output"].append(remaining)
                remaining = ""
    else:
        ljinux.based.user_vars["output"].append(remaining)
    del remaining
