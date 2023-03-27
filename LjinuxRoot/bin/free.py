opts = ljinux.api.xarg()

flag = "k"
if len(opts["o"]) > 0:
    flag = list(opts["o"].keys())[0]
del opts

calc_cond = {
    "b": lambda num: num,  # Bytes
    "k": lambda num: num // 1024,  # Kilobytes
    "m": lambda num: num // (1024**2),  # Megabytes
    "g": lambda num: num // (1024**3),  # Gigabytes
}

try:
    total = calc_cond[flag](usable_ram)
    free = calc_cond[flag](gc.mem_free())
    used = total - free
    gnspace = 12
    space = " "
    spacer0 = gnspace * space  # initial spacer
    spacer1 = (gnspace - 4) * space  # mem spacer
    spacer2 = (gnspace - len(str(total))) * space  # total spacer
    spacer3 = (gnspace - len(str(used))) * space  # used spacer
    del space, gnspace
    term.write(f"{spacer0}Total\nMem:{spacer1}{total}{spacer2}{used}{spacer3}{free}")
    ljinux.api.setvar("return", str(free))
    del total, used, free, spacer0, spacer1, spacer2, spacer3
except KeyError:
    ljinux.based.error(1)
    ljinux.based.user_vars["return"] = "1"

del flag, calc_cond
