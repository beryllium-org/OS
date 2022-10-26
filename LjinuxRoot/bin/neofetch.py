global uptimee

neofetch_time = int(uptimee + time.monotonic())

uptimestr = ""

hours = neofetch_time // 3600  # Take out the hours
neofetch_time -= hours * 3600
minutes = neofetch_time // 60  # Take out the minutes
neofetch_time -= minutes * 60

if hours > 0:
    uptimestr += str(hours) + " hours, "
if minutes > 0:
    uptimestr += str(minutes) + " minutes, "
if neofetch_time > 0:
    uptimestr += str(neofetch_time) + " seconds"
else:
    uptimestr = uptimestr[:-2]
del hours, minutes, neofetch_time

Ccpu = f"{platform}"
try:
    from microcontroller import cpus

    Ccpu += f" ({len(cpus)})"
except:
    Ccpu += " (1)"
Ccpu += f" @ {trunc(cpu.frequency / 1000000)}Mhz"

gc.collect()
gc.collect()

Rram = f"{trunc((usable_ram - gc.mem_free()) / 1024)}KiB / {int(usable_ram/1024)}KiB"
sizee = term.detect_size()

# to edit the neofetch, you need to swap logo, tex and seperat

seperat = 28  # where do we begin collumn #2

logo = [
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

tex = [
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
    f"{colors.red_t}Uptime{colors.endc}: {uptimestr}",
    f"{colors.red_t}Packages{colors.endc}: "
    + str(len(listdir("/LjinuxRoot/etc/jpkg/Installed")))
    + " (jpkg)",
    f"{colors.red_t}Shell{colors.endc}: {colors.magenta_t}Based{colors.endc}",
    f"{colors.red_t}Resolution:{colors.endc} {sizee[1]}x{sizee[0]}",
    f"{colors.red_t}WM{colors.endc}: Farland",
    f"{colors.red_t}Terminal{colors.endc}: TTYACM0",
    f"{colors.red_t}CPU{colors.endc}: {Ccpu}",
    f"{colors.red_t}System Memory{colors.endc}: {Rram}",
]

del Rram, Ccpu, sizee
del uptimestr

try:
    import espidf

    total = espidf.heap_caps_get_total_size()
    used = total - espidf.heap_caps_get_free_size()
    erram = f"{trunc((used) / 1024)}KiB / {trunc((total) / 1024)}KiB"
    tex += [f"\033[31mESPIDF Memory{colors.endc}: {erram}"]
    del total, used, erram, espidf
except ImportError:
    pass

tex += [
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
pos = term.detect_pos()
for i in range(0, max(len(logo), len(tex))):
    try:
        stdout.write(logo[i])
    except IndexError:
        pass
    term.move(y=seperat, x=pos[0] + i)
    try:
        stdout.write(tex[i])
    except IndexError:
        pass
    stdout.write("\n")
    del i
del tex, logo, seperat, pos
