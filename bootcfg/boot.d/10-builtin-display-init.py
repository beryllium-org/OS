rename_process("builtin display init")
from drivers.displayiotty import displayiotty

pv[0]["consoles"]["ttyDISPLAY0"] = displayiotty()
pv[0]["consoles"]["ttyDISPLAY0"].display = be.devices["gpiochip"][0].pin(
    "DISPLAY", force=True
)
pv[0]["consoles"]["ttyDISPLAY0"].enable()
del displayiotty
