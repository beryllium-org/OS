rename_process("wiopad init")
be.based.run("modprobe wiopad")
pv[0]["consoles"]["ttyDISPLAY0"].stdio = be.devices["wiopad"][0]
