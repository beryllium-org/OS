ljinux.api.setvar("output")
ljinux.based.user_vars["output"] = list()
for i in ljinux.based.user_vars["input"]:
    remaining = i
    if remaining != "":
        while len(remaining) > 0:
            if len(remaining) > sizee[1]:
                ljinux.based.user_vars["output"].append(remaining[: sizee[1]])
                remaining = remaining[sizee[1] :]
            else:
                ljinux.based.user_vars["output"].append(remaining)
                remaining = ""
    else:
        ljinux.based.user_vars["output"].append(remaining)
    del remaining
ljinux.api.setvar("input")
