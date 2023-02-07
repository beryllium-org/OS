length = len(ljinux.based.user_vars["argj"])

flag = None
if length < 1:
    flag = "-k"
else:
    flag = ljinux.based.user_vars["argj"].split()[1]

calc_cond = {
    "-b": lambda num: num,  # Bytes
    "-k": lambda num: num / 1024,  # Kilobytes
    "-m": lambda num: num / (1024**2),  # Megabytes
    "-g": lambda num: num / (1024**3),  # Gigabytes
}

try:
    total = calc_cond[flag](usable_ram)
    free = calc_cond[flag](gc.mem_free())
    used = total - free
    gnspace = 12
    space = " "
    spacer0 = gnspace * space  # initial spacer
    spacer1 = (gnspace - 4) * space  # mem spacer
    spacer2 = (gnspace - len(total)) * space  # total spacer
    spacer3 = (gnspace - len(used)) * space  # used spacer
    del space, gnspace
    print(f"{spacer0}\n" + f"Mem:{spacer1}{total}{spacer2}{used}{spacer3}{free}")
    ljinux.based.user_vars["return"] = str(free)
    del total, used, free, buffers, cached, spacer0, spacer1, spacer2, spacer3
except KeyError:
    ljinux.based.error(1)
    ljinux.based.user_vars["return"] = "1"

del length, flag, calc_cond
