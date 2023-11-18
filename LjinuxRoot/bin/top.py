rename_process("top")

# Time
vr("tt", time.localtime())
vr("tmh", str(vr("tt").tm_hour))
if len(vr("tmh")) < 2:
    vr("tmh", "0" + vr("tmh"))
vrp("tmh", ":")
vr("tmm", str(vr("tt").tm_min))
if len(vr("tmm")) < 2:
    vr("tmm", "0" + vr("tmm"))
vrp("tmm", ":")
vr("tms", str(vr("tt").tm_sec))
if len(vr("tms")) < 2:
    vr("tms", "0" + vr("tms"))
vr("tstr", (vr("tmh") + vr("tmm") + vr("tms")))

# Uptime
vr("time", int(pv[0]["uptimee"] + time.monotonic()))
vr("hr", vr("time") // 3600)
vrm("time", vr("hr") * 3600)
vr("min", vr("time") // 60)
vrm("time", vr("min") * 60)

vr("hr", str(vr("hr")))
if len(vr("hr")) < 2:
    vr("hr", "0" + vr("hr"))
vrp("hr", ":")
vr("min", str(vr("min")))
if len(vr("min")) < 2:
    vr("min", "0" + vr("min"))
vrp("min", ":")
vr("time", str(vr("time")))
if len(vr("time")) < 2:
    vr("time", "0" + vr("time"))
vr("ustr", (vr("hr") + vr("min") + vr("time")))

term.write(
    "top - {} up {}, 1 users, load average: 1,00, 1,00, 1,00".format(
        vr("tstr"), vr("ustr")
    )
)
clear_process_storage()

vr("c", [0, 0, 0])
for pv[get_pid()]["i"] in pvd.keys():
    pv[get_pid()]["c"][pvd[pv[get_pid()]["i"]]["status"]] += 1

term.write(
    "Tasks:    {} total,    {} running,    {} sleeping,    {} zombie".format(
        len(pvd), vr("c")[0], vr("c")[1], vr("c")[2]
    )
)

term.write(
    "KiB Mem: {} total, {} free, {} used, {} buff/cache\n".format(
        round((gc.mem_alloc() + gc.mem_free()) / 1024, 1),
        round(gc.mem_free() / 1024, 1),
        round(gc.mem_alloc() / 1024, 1),
        0.0,
    )
)
term.write(f"{colors.inverse}    PID USER      PRESERVE NAME{colors.uninverse}")

vr("k", list(pvd.keys()))
pv[get_pid()]["k"].sort()
pv[get_pid()]["k"].reverse()
for pv[get_pid()]["i"] in vr("k"):
    vr("strpid", str(vr("i")))
    while len(vr("strpid")) < 7:
        vr("strpid", " " + vr("strpid"))
    term.nwrite(vr("strpid"))
    vrd("strpid")
    term.nwrite(
        " " + pvd[vr("i")]["owner"][:10] + " " * (10 - len(pvd[vr("i")]["owner"][:10]))
    )
    term.nwrite(
        str(pvd[vr("i")]["preserve"]) + " " * (5 if pvd[vr("i")]["preserve"] else 4)
    )
    term.write(pvd[vr("i")]["name"])
