rename_process("free")
vr("opts", be.api.xarg())

vr("flag", "k")
if len(vr("opts")["o"]) > 0:
    vr("flag", list(vr("opts")["o"].keys())[0])

vr(
    "calc_cond",
    {
        "b": lambda num: num,  # Bytes
        "k": lambda num: num // 1024,  # Kilobytes
        "m": lambda num: num // (1024**2),  # Megabytes
        "g": lambda num: num // (1024**3),  # Gigabytes
    },
)

try:
    vr("total", vr("calc_cond")[vr("flag")](vr("usable_ram", pid=0)))
    vr("free", vr("calc_cond")[vr("flag")](gc.mem_free()))
    vr("used", vr("total") - vr("free"))
    vr("gnspace", 12)
    vr("space", " ")
    vr("spacer0", (vr("gnspace") * vr("space")))  # initial spacer
    vr("spacer1", (vr("gnspace") - 4) * vr("space"))  # mem spacer
    vr("spacer2", (vr("gnspace") - len(str(vr("total")))) * vr("space"))  # total spacer
    vr("spacer3", (vr("gnspace") - len(str(vr("used")))) * vr("space"))  # used spacer
    term.write(
        "{}Total{}{}{}{}\nMem:{}{}{}{}{}{}".format(
            vr("spacer0"),
            vr("spacer1")[:-1],
            "Used",
            vr("spacer2"),
            "Free",
            vr("spacer1"),
            vr("total"),
            vr("spacer2"),
            vr("used"),
            vr("spacer3"),
            vr("free"),
        )
    )
    be.api.setvar("return", str(vr("free")))
except KeyError:
    be.based.error(1)
    be.api.setvar("return", 1)
