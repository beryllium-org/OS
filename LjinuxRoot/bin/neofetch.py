rename_process("neofetch")

gc.collect()
gc.collect()
gc.collect()
gc.collect()

vr(
    "raml",
    "{}KiB / {}KiB".format(
        trunc((pv[0]["usable_ram"] - gc.mem_free()) / 1024),
        int(pv[0]["usable_ram"] / 1024),
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

vr("sep", 28)  # where do we begin collumn #2
vr(
    "logo",
    [
        f"{colors.green_t}  ,----,{colors.endc}                    ",
        f"{colors.green_t}  ,----.|{colors.endc}      {colors.magenta_t},----._{colors.endc}",
        f"{colors.green_t}  |LLL|l:{colors.endc}     {colors.magenta_t}.-- -.'j\\{colors.endc}",
        f"{colors.green_t}  :LLL:l|{colors.endc}     {colors.magenta_t}|JJJJ|jjj:{colors.endc}",
        f"{colors.green_t}  |LLL'l:{colors.endc}     {colors.magenta_t}:JJJJ;jjj|{colors.endc}",
        f"{colors.green_t}  ;LLL;l'{colors.endc}     {colors.magenta_t}:JJJJ|jjj|{colors.endc}",
        f"{colors.green_t}  'LLL|l|{colors.endc}     {colors.magenta_t}|JJJJ:jjj:{colors.endc}",
        f"{colors.green_t}  |LLL|l|{colors.endc}     {colors.magenta_t}:JJJJ|jjj:{colors.endc}",
        f"{colors.green_t}  'LLL:l;_____{colors.endc}{colors.magenta_t}|JJJJ;jjj|{colors.endc}",
        f"{colors.green_t}  |LLL|;.____{colors.endc}{colors.magenta_t};lJJJJ|jjj|{colors.endc}",
        f"{colors.green_t}  ;LLL:{colors.endc} {colors.magenta_t}/JJJJ/\JJJJ/jjj:{colors.endc}",
        f"{colors.green_t}  |LLL,{colors.endc}{colors.magenta_t}/JJ../jj`..-jjjj,{colors.endc}",
        f"{colors.green_t}   ---'{colors.endc}{colors.magenta_t}\JJJJ\jjjjjjjjj; {colors.endc}",
        f"{colors.green_t}        {colors.endc}{colors.magenta_t}\JJJJ\jjjjjj,'{colors.endc}",
        f"{colors.magenta_t}         \"---....--'{colors.endc}",
    ],
)
vr(
    "tex",
    [
        (
            colors.cyan_t
            + ljinux.based.system_vars["USER"]
            + "@"
            + ljinux.based.system_vars["HOSTNAME"]
            + colors.endc
        ),
        "---------",
        (
            colors.red_t
            + "OS"
            + colors.endc
            + ": "
            + colors.yellow_t
            + "Ljinux "
            + ljinux.based.system_vars["VERSION"]
            + colors.endc
        ),
        (
            colors.red_t
            + "Host"
            + colors.endc
            + ": "
            + ljinux.based.system_vars["BOARD"]
        ),
        (
            colors.red_t
            + "CircuitPython"
            + colors.endc
            + ": "
            + ljinux.based.system_vars["IMPLEMENTATION"]
        ),
        "{}Uptime{}: {}".format(colors.red_t, colors.endc, vr("ustr")),
        f"{colors.red_t}Packages{colors.endc}: "
        + str(len(listdir("/LjinuxRoot/etc/jpkg/Installed")))
        + " (jpkg)",
        f"{colors.red_t}Shell{colors.endc}: {colors.magenta_t}Based{colors.endc}",
        "{}Resolution:{} {}x{}".format(
            colors.red_t, colors.endc, vr("size")[1], vr("size")[0]
        ),
        f"{colors.red_t}WM{colors.endc}: Farland",
        "{}Terminal{}: {}".format(colors.red_t, colors.endc, pv[0]["console_active"]),
        "{}CPU{}: {}".format(colors.red_t, colors.endc, vr("cpul")),
        "{}System Memory{}: {}".format(colors.red_t, colors.endc, vr("raml")),
    ],
)

try:
    import espidf

    vr("total", espidf.heap_caps_get_total_size())
    vr("used", vr("total") - espidf.heap_caps_get_free_size())
    vr(
        "erram",
        "{}KiB / {}KiB".format(trunc((vr("used")) / 1024), trunc((vr("total")) / 1024)),
    )
    vrp("tex", ["\033[31mESPIDF Memory{}: {}".format(colors.endc, vr("erram"))])

    del espidf
except ImportError:
    pass

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
            + ((vr("sep") - len(ljinux.api.remove_ansi(vr("logo")[vr("i")]))) * " ")
        )
    except IndexError:
        term.nwrite(vr("sep") * " ")
    try:
        term.nwrite(vr("tex")[vr("i")])
    except IndexError:
        pass
    term.write()
