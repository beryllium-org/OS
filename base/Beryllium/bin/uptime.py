rename_process("uptime")
vr("tt", time.localtime())
vr(
    "dat",
    [
        vr("tt").tm_hour,
        vr("tt").tm_min,
        vr("tt").tm_sec,
    ],
)

for pv[get_pid()]["i"] in range(3):
    vr("dat")[vr("i")] = str(vr("dat")[vr("i")])
    if len(str(vr("dat")[vr("i")])) < 2:
        vr("dat")[vr("i")] = "0" + vr("dat")[vr("i")]

term.nwrite(" " + ":".join(vr("dat")) + " up ")

clear_process_storage()

vr("timef", pv[0]["uptimee"] + time.monotonic())
vr("time", int(vr("timef")))
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
term.nwrite(vr("hr") + vr("min") + vr("time"))
term.write(",  1 user,  load average: 1.00, 1.00, 1.00")

be.api.setvar("return", "0")
