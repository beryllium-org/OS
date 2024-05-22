rename_process("cardputer display init")
from drivers.cardputerVT import cardputerVT

pv[0]["consoles"]["tty1"] = cardputerVT()
be.based.run("mknod DISPLAY")
be.devices["DISPLAY"][0] = be.devices["gpiochip"][0].pin("DISPLAY", force=True)
del cardputerVT
