global uptimee
print("    `.::///+:/-.        --///+//-:``    ", end="")
print(ljinux.based.system_vars["user"], end="")
print("@pico")
print("   `+oooooooooooo:   `+oooooooooooo:    ---------")
print("    /oooo++//ooooo:  ooooo+//+ooooo.    OS: Ljinux", end=" ")
print(ljinux.based.system_vars["Version"])
print("    `+ooooooo:-:oo-  +o+::/ooooooo:     Host: ", end="")
for s in board.board_id.replace("_", " ").split():
    print(s[0].upper() + s[1:], end=" ")
print(" ")
print("     `:oooooooo+``    `.oooooooo+-      CircuitPython:", end=" ")
print(
    str(implementation.version[0])
    + "."
    + str(implementation.version[1])
    + "."
    + str(implementation.version[2])
)
print("       `:++ooo/.        :+ooo+/.`       Uptime:", end=" ")
neofetch_time = int(uptimee + time.monotonic())
uptimestr = ""
hours = neofetch_time // 3600  # Take out the hours
neofetch_time -= hours * 3600  #
minutes = neofetch_time // 60  # Take out the minutes
neofetch_time -= minutes * 60  #
if hours > 0:
    uptimestr += str(hours) + " hours, "
if minutes > 0:
    uptimestr += str(minutes) + " minutes, "
if neofetch_time > 0:
    uptimestr += str(neofetch_time) + " seconds"
else:
    uptimestr = uptimestr[:-2]
print(uptimestr)
del uptimestr
del neofetch_time
del hours
del minutes
gc.collect()
print("          ...`  `.----.` ``..           Packages: 0 ()")
print("       .::::-``:::::::::.`-:::-`        Shell: Based")
print("      -:::-`   .:::::::-`  `-:::-       WM: Farland")
print("     `::.  `.--.`  `` `.---.``.::`      Terminal: TTYACM0")
print("         .::::::::`  -::::::::` `       CPU: ", end="")
print(
    platform
    + " ("
    + str(len((cpus)))
    + ") @ "
    + str(int(cpu.frequency / 1000000))
    + "MHz"
)
print(
    "   .::` .:::::::::- `::::::::::``::.    Memory: "
    + str(int(264 - int(gc.mem_free()) / 1000))
    + "KiB / 264KiB          "
)
print("  -:::` ::::::::::.  ::::::::::.`:::-")
print("  ::::  -::::::::.   `-::::::::  ::::")
print("  -::-   .-:::-.``....``.-::-.   -::-")
print("   .. ``       .::::::::.     `..`..")
print("     -:::-`   -::::::::::`  .:::::`")
print("     :::::::` -::::::::::` :::::::.")
print("     .:::::::  -::::::::. ::::::::")
print("      `-:::::`   ..--.`   ::::::.")
print("        `...`  `...--..`  `...`")
print("              .::::::::::")
print("               `.-::::-`")
