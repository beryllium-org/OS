rename_process("free")
pv[get_pid()]["opts"] = ljinux.api.xarg()

pv[get_pid()]["flag"] = "k"
if len(pv[get_pid()]["opts"]["o"]) > 0:
    pv[get_pid()]["flag"] = list(pv[get_pid()]["opts"]["o"].keys())[0]

pv[get_pid()]["calc_cond"] = {
    "b": lambda num: num,  # Bytes
    "k": lambda num: num // 1024,  # Kilobytes
    "m": lambda num: num // (1024**2),  # Megabytes
    "g": lambda num: num // (1024**3),  # Gigabytes
}

try:
    pv[get_pid()]["total"] = pv[get_pid()]["calc_cond"][pv[get_pid()]["flag"]](
        pv[0]["usable_ram"]
    )
    pv[get_pid()]["free"] = pv[get_pid()]["calc_cond"][pv[get_pid()]["flag"]](
        gc.mem_free()
    )
    pv[get_pid()]["used"] = pv[get_pid()]["total"] - pv[get_pid()]["free"]
    pv[get_pid()]["gnspace"] = 12
    pv[get_pid()]["space"] = " "
    pv[get_pid()]["spacer0"] = (
        pv[get_pid()]["gnspace"] * pv[get_pid()]["space"]
    )  # initial spacer
    pv[get_pid()]["spacer1"] = (pv[get_pid()]["gnspace"] - 4) * pv[get_pid()][
        "space"
    ]  # mem spacer
    pv[get_pid()]["spacer2"] = (
        pv[get_pid()]["gnspace"] - len(str(pv[get_pid()]["total"]))
    ) * pv[get_pid()][
        "space"
    ]  # total spacer
    pv[get_pid()]["spacer3"] = (
        pv[get_pid()]["gnspace"] - len(str(pv[get_pid()]["used"]))
    ) * pv[get_pid()][
        "space"
    ]  # used spacer
    term.write(
        "{}Total{}{}{}{}\nMem:{}{}{}{}{}{}".format(
            pv[get_pid()]["spacer0"],
            pv[get_pid()]["spacer1"][:-1],
            "Used",
            pv[get_pid()]["spacer2"],
            "Free",
            pv[get_pid()]["spacer1"],
            pv[get_pid()]["total"],
            pv[get_pid()]["spacer2"],
            pv[get_pid()]["used"],
            pv[get_pid()]["spacer3"],
            pv[get_pid()]["free"],
        )
    )
    ljinux.api.setvar("return", str(pv[get_pid()]["free"]))
except KeyError:
    ljinux.based.error(1)
    ljinux.api.setvar("return", 1)
