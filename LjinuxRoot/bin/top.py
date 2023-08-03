rename_process("top")
# term.clear()

# Time
pv[get_pid()]["tt"] = time.localtime()
pv[get_pid()]["tmh"] = str(pv[get_pid()]["tt"].tm_hour)
if len(pv[get_pid()]["tmh"]) < 2:
    pv[get_pid()]["tmh"] = "0" + pv[get_pid()]["tmh"]
pv[get_pid()]["tmh"] += ":"
pv[get_pid()]["tmm"] = str(pv[get_pid()]["tt"].tm_min)
if len(pv[get_pid()]["tmm"]) < 2:
    pv[get_pid()]["tmm"] = "0" + pv[get_pid()]["tmm"]
pv[get_pid()]["tmm"] += ":"
pv[get_pid()]["tms"] = str(pv[get_pid()]["tt"].tm_sec)
if len(pv[get_pid()]["tms"]) < 2:
    pv[get_pid()]["tms"] = "0" + pv[get_pid()]["tms"]
pv[get_pid()]["tstr"] = (
    pv[get_pid()]["tmh"] + pv[get_pid()]["tmm"] + pv[get_pid()]["tms"]
)

# Uptime
pv[get_pid()]["time"] = int(pv[0]["uptimee"] + time.monotonic())
pv[get_pid()]["hr"] = pv[get_pid()]["time"] // 3600
pv[get_pid()]["time"] -= pv[get_pid()]["hr"] * 3600
pv[get_pid()]["min"] = pv[get_pid()]["time"] // 60
pv[get_pid()]["time"] -= pv[get_pid()]["min"] * 60

pv[get_pid()]["hr"] = str(pv[get_pid()]["hr"])
if len(pv[get_pid()]["hr"]) < 2:
    pv[get_pid()]["hr"] = "0" + pv[get_pid()]["hr"]
pv[get_pid()]["hr"] += ":"
pv[get_pid()]["min"] = str(pv[get_pid()]["min"])
if len(pv[get_pid()]["min"]) < 2:
    pv[get_pid()]["min"] = "0" + pv[get_pid()]["min"]
pv[get_pid()]["min"] += ":"
pv[get_pid()]["time"] = str(pv[get_pid()]["time"])
if len(pv[get_pid()]["time"]) < 2:
    pv[get_pid()]["time"] = "0" + pv[get_pid()]["time"]
pv[get_pid()]["ustr"] = (
    pv[get_pid()]["hr"] + pv[get_pid()]["min"] + pv[get_pid()]["time"]
)

term.write(
    "top - {} up {}, 1 users, load average: 1,00, 1,00, 1,00".format(
        pv[get_pid()]["tstr"], pv[get_pid()]["ustr"]
    )
)
clear_process_storage()

pv[get_pid()]["c"] = [0, 0, 0]
for pv[get_pid()]["i"] in pvd.keys():
    pv[get_pid()]["c"][pvd[pv[get_pid()]["i"]]["status"]] += 1

term.write(
    "Tasks:    {} total,    {} running,    {} sleeping,    {} zombie".format(
        len(pvd), pv[get_pid()]["c"][0], pv[get_pid()]["c"][1], pv[get_pid()]["c"][2]
    )
)

term.write(
    "KiB Mem: {} total, {} free, {} used, {} buff/cache\n".format(
        round(pv[0]["usable_ram"] / 1024, 1),
        round(gc.mem_free() / 1024, 1),
        round(gc.mem_alloc() / 1024, 1),
        0.0,
    )
)
term.write(f"{colors.inverse}    PID USER      PRESERVE NAME{colors.uninverse}")

pv[get_pid()]["k"] = list(pvd.keys())
pv[get_pid()]["k"].sort()
pv[get_pid()]["k"].reverse()
for pv[get_pid()]["i"] in pv[get_pid()]["k"]:
    pv[get_pid()]["strpid"] = str(pv[get_pid()]["i"])
    while len(pv[get_pid()]["strpid"]) < 7:
        pv[get_pid()]["strpid"] = " " + pv[get_pid()]["strpid"]
    term.nwrite(pv[get_pid()]["strpid"])
    del pv[get_pid()]["strpid"]
    term.nwrite(
        " "
        + pvd[pv[get_pid()]["i"]]["owner"][:10]
        + " " * (10 - len(pvd[pv[get_pid()]["i"]]["owner"][:10]))
    )
    term.nwrite(
        str(pvd[pv[get_pid()]["i"]]["preserve"])
        + " " * (5 if pvd[pv[get_pid()]["i"]]["preserve"] else 4)
    )
    term.write(pvd[pv[get_pid()]["i"]]["name"])
