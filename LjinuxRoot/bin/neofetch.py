global uptimee

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

Ccpu = "{} ({}) @ {}Mhz".format(platform, len(cpus), trunc(cpu.frequency / 1000000))
gc.collect()
gc.collect()
Rram = "{}KiB / 264KiB".format(trunc(abs(264 - gc.mem_free() / 1000)))

print(
    """\033[32m    `.::///+:/-.        --///+//-:``    {}@{} \033[0m
\033[32m   `+oooooooooooo:   `+oooooooooooo:  \033[0m  ---------
\033[32m    /oooo++//ooooo:  ooooo+//+ooooo.  \033[0m  \033[31mOS\033[0m: \033[33mLjinux {}\033[0m
\033[32m    `+ooooooo:-:oo-  +o+::/ooooooo:   \033[0m  \033[31mHost\033[0m: {}  
\033[32m    `:oooooooo+``    `.oooooooo+-    \033[0m   \033[31mCircuitPython\033[0m: {}
\033[32m      `:++ooo/.        :+ooo+/.`     \033[0m   \033[31mUptime\033[0m: {}
\033[91m         ...`  `.----.` ``..         \033[0m   \033[31mPackages\033[0m: 0 ()
\033[91m        .::::-``:::::::::.`-:::-`    \033[0m   \033[31mShell\033[0m: \033[35mBased\033[0m
\033[91m     -:::-`   .:::::::-`  `-:::-     \033[0m   \033[31mWM\033[0m: Farland
\033[91m    `::.  `.--.`  `` `.---.``.::`    \033[0m   \033[31mTerminal\033[0m: TTYACM0
\033[91m    `  ` `.::::::::`  -::::::::` ``   \033[0m  \033[31mCPU\033[0m: {}
\033[91m   .::` .:::::::::- `::::::::::``::.  \033[0m  \033[31mMemory\033[0m: {}
\033[91m  -:::` ::::::::::.  ::::::::::.`:::- \033[0m
\033[91m  ::::  -::::::::.   `-::::::::  :::: \033[0m
\033[91m  -::-   .-:::-.``....``.-::-.   -::- \033[0m
\033[91m  .. ``       .::::::::.     `..`..  \033[0m
\033[91m    -:::-`   -::::::::::`  .:::::`   \033[0m
\033[91m    :::::::` -::::::::::` :::::::.   \033[0m
\033[91m    .:::::::  -::::::::. ::::::::    \033[0m
\033[91m     `-:::::`   ..--.`   ::::::.     \033[0m
\033[91m       `...`  `...--..`  `...`       \033[0m
\033[91m             .::::::::::             \033[0m
\033[91m              `.-::::-`              \033[0m
""".format(
        ljinux.based.system_vars["USER"],
        ljinux.based.system_vars["HOSTNAME"],
        ljinux.based.system_vars["VERSION"],
        ljinux.based.system_vars["BOARD"],
        ljinux.based.system_vars["IMPLEMENTATION"],
        uptimestr,
        Ccpu,
        Rram,
    )
)

del Rram, Ccpu
del uptimestr
del neofetch_time
del hours, minutes
