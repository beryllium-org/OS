rename_process("neofetch")

gc.collect()
gc.collect()
gc.collect()
gc.collect()

pv[get_pid()]["raml"] = "{}KiB / {}KiB".format(
    trunc((pv[0]["usable_ram"] - gc.mem_free()) / 1024), int(pv[0]["usable_ram"] / 1024)
)

pv[get_pid()]["time"] = int(pv[0]["uptimee"] + time.monotonic())
pv[get_pid()]["ustr"] = ""
pv[get_pid()]["hr"] = pv[get_pid()]["time"] // 3600  # Take out the hours
pv[get_pid()]["time"] -= pv[get_pid()]["hr"] * 3600
pv[get_pid()]["min"] = pv[get_pid()]["time"] // 60  # Take out the minutes
pv[get_pid()]["time"] -= pv[get_pid()]["min"] * 60
if pv[get_pid()]["hr"] > 0:
    pv[get_pid()]["ustr"] += str(pv[get_pid()]["hr"]) + " hours, "
if pv[get_pid()]["min"] > 0:
    pv[get_pid()]["ustr"] += str(pv[get_pid()]["min"]) + " minutes, "
if pv[get_pid()]["time"] > 0:
    pv[get_pid()]["ustr"] += str(pv[get_pid()]["time"]) + " seconds"
else:
    pv[get_pid()]["ustr"] = pv[get_pid()]["ustr"][:-2]

pv[get_pid()]["cpul"] = str(platform)
pv[get_pid()]["cpul"] += f" (1) @ {trunc(cpu.frequency / 1000000)}Mhz"

pv[get_pid()]["size"] = term.detect_size()

pv[get_pid()]["sep"] = 28  # where do we begin collumn #2
pv[get_pid()]["logo"] = [
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
]
pv[get_pid()]["tex"] = [
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
    (colors.red_t + "Host" + colors.endc + ": " + ljinux.based.system_vars["BOARD"]),
    (
        colors.red_t
        + "CircuitPython"
        + colors.endc
        + ": "
        + ljinux.based.system_vars["IMPLEMENTATION"]
    ),
    "{}Uptime{}: {}".format(colors.red_t, colors.endc, pv[get_pid()]["ustr"]),
    f"{colors.red_t}Packages{colors.endc}: "
    + str(len(listdir("/LjinuxRoot/etc/jpkg/Installed")))
    + " (jpkg)",
    f"{colors.red_t}Shell{colors.endc}: {colors.magenta_t}Based{colors.endc}",
    "{}Resolution:{} {}x{}".format(
        colors.red_t, colors.endc, pv[get_pid()]["size"][1], pv[get_pid()]["size"][0]
    ),
    f"{colors.red_t}WM{colors.endc}: Farland",
    "{}Terminal{}: {}".format(colors.red_t, colors.endc, pv[0]["console_active"]),
    "{}CPU{}: {}".format(colors.red_t, colors.endc, pv[get_pid()]["cpul"]),
    "{}System Memory{}: {}".format(colors.red_t, colors.endc, pv[get_pid()]["raml"]),
]

try:
    import espidf

    total = espidf.heap_caps_get_total_size()
    used = total - espidf.heap_caps_get_free_size()
    erram = f"{trunc((used) / 1024)}KiB / {trunc((total) / 1024)}KiB"
    pv[get_pid()]["tex"] += [f"\033[31mESPIDF Memory{colors.endc}: {erram}"]

    del espidf
except ImportError:
    pass

pv[get_pid()]["tex"] += [
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
]
for i in range(0, max(len(pv[get_pid()]["logo"]), len(pv[get_pid()]["tex"]))):
    try:
        term.nwrite(
            pv[get_pid()]["logo"][i]
            + (
                (
                    pv[get_pid()]["sep"]
                    - len(ljinux.api.remove_ansi(pv[get_pid()]["logo"][i]))
                )
                * " "
            )
        )
    except IndexError:
        term.nwrite(pv[get_pid()]["sep"] * " ")
    try:
        term.nwrite(pv[get_pid()]["tex"][i])
    except IndexError:
        pass
    term.write()
