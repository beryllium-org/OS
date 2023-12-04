rename_process("timesync")
if "network" in ljinux.modules and ljinux.modules["network"].connected:
    if ljinux.modules["network"].timeset():
        ljinux.api.setvar("return", "0")
    else:
        dmtex("Could not sync time.")
        ljinux.api.setvar("return", "1")
