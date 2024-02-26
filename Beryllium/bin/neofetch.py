rename_process("neofetch")

vr("ramt", gc.mem_alloc() + gc.mem_free())

try:
    import espidf

    vr("idftotal", espidf.heap_caps_get_total_size())
    if vr("idftotal") > vr("ramt"):
        vr("ramt", vr("idftotal"))
    vrd("idftotal")
    del espidf
except ImportError:
    pass

gc.collect()
gc.collect()
gc.collect()
gc.collect()

vr(
    "raml",
    "{}KiB / {}KiB".format(
        trunc((vr("ramt") - gc.mem_free()) / 1024),
        int(vr("ramt") / 1024),
    ),
)

vr("time", int(pv[0]["uptimee"] + time.monotonic()))
vr("ustr", "")
vr("hr", vr("time") // 3600)  # Take out the hours
vrm("time", vr("hr") * 3600)
vr("min", vr("time") // 60)  # Take out the minutes
vrm("time", vr("min") * 60)
if vr("hr") > 0:
    vrp("ustr", str(vr("hr")) + " hours, ")
if vr("min") > 0:
    vrp("ustr", str(vr("min")) + " minutes, ")
if vr("time") > 0:
    vrp("ustr", str(vr("time")) + " seconds")
else:
    vr("ustr", vr("ustr")[:-2])

vr("cpul", str(platform))
vrp("cpul", f" (1) @ {trunc(cpu.frequency / 1000000)}Mhz")

vr("size", term.detect_size(3))

vr("sep", 32)  # where do we begin collumn #2
vr(
    "logo",
    [
        f"{colors.be_main}     ...     ..{colors.endc}",
        f'{colors.be_main}  .=*8888x <"?88h.     4{colors.endc}',
        f"{colors.be_main} X>  '8888H> '8888{colors.endc}",
        f"{colors.be_main}'88h. `8888   8888        .u{colors.endc}",
        f"{colors.be_main}'8888 '8888    \"88>    ud8888.{colors.endc}",
        f"{colors.be_main} `888 '8888.xH888x.  :888'8888.{colors.endc}",
        f'{colors.be_main}   X" :88*~  `*8888> d888 \'88%"{colors.endc}',
        f'{colors.be_main} ~"   !"`      "888> 8888.+"{colors.endc}',
        f"{colors.be_main}  .H8888h.      ?88  8888L{colors.endc}",
        f"{colors.be_main} :\"^\"88888h.    '!   '8888c. .+{colors.endc}",
        f'{colors.be_main} ^    "88888hx.+"     "88888%{colors.endc}',
        f'{colors.be_main}        ^"**""          "YP\'{colors.endc}',
    ],
)
vr(
    "tex",
    [
        (
            colors.yellow_t
            + be.based.system_vars["USER"]
            + "@"
            + be.based.system_vars["HOSTNAME"]
            + colors.endc
        ),
        "---------",
        (
            colors.yellow_t
            + "OS"
            + colors.endc
            + ": "
            + colors.be_main
            + "Beryllium "
            + be.based.system_vars["VERSION"]
            + colors.endc
        ),
        (colors.yellow_t + "Host" + colors.endc + ": " + be.based.system_vars["BOARD"]),
        (
            colors.yellow_t
            + "CircuitPython"
            + colors.endc
            + ": "
            + be.based.system_vars["IMPLEMENTATION"]
        ),
        "{}Uptime{}: {}".format(colors.yellow_t, colors.endc, vr("ustr")),
        f"{colors.yellow_t}Packages{colors.endc}: "
        + str(len(listdir(pv[0]["root"] + "/etc/jpkg/Installed")))
        + " (jpkg)",
        "{}Resolution:{} {}x{}".format(
            colors.yellow_t, colors.endc, vr("size")[1], vr("size")[0]
        ),
        "{}Terminal{}: {}".format(
            colors.yellow_t, colors.endc, pv[0]["console_active"]
        ),
        "{}CPU{}: {}".format(colors.yellow_t, colors.endc, vr("cpul")),
        "{}System Memory{}: {}".format(colors.yellow_t, colors.endc, vr("raml")),
    ],
)

vrp(
    "tex",
    [
        "",
        (
            f"{colors.black_t}███{colors.endc}{colors.red_t}███{colors.endc}"
            + f"{colors.green_t}███{colors.endc}{colors.yellow_t}███{colors.endc}"
            + f"{colors.blue_t}███{colors.endc}{colors.magenta_t}███{colors.endc}"
            + f"{colors.cyan_t}███{colors.endc}{colors.white_t}███{colors.endc}"
        ),
        (
            f"{colors.black_t}███{colors.endc}"
            + f"{colors.red_t}███{colors.endc}{colors.green_t}███{colors.endc}"
            + f"{colors.yellow_t}███{colors.endc}{colors.blue_t}███{colors.endc}"
            + f"{colors.magenta_t}███{colors.endc}{colors.cyan_t}███{colors.endc}"
            + f"{colors.white_t}███{colors.endc}"
        ),
    ],
)
for pv[get_pid()]["i"] in range(0, max(len(vr("logo")), len(vr("tex")))):
    try:
        term.nwrite(
            vr("logo")[vr("i")]
            + ((vr("sep") - len(be.api.remove_ansi(vr("logo")[vr("i")]))) * " ")
        )
    except IndexError:
        term.nwrite(vr("sep") * " ")
    try:
        term.nwrite(vr("tex")[vr("i")])
    except IndexError:
        pass
    term.write()
