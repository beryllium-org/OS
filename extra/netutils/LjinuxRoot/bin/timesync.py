rename_process("timesync")
if "network" in be.devices and be.devices["network"][0].connected:
    if be.devices["network"][0].timeset():
        be.based.system_vars["TIMEZONE_OFFSET"] = be.devices["network"][0]._tz
        be.api.setvar("return", "0")
    else:
        dmtex("Could not sync time.")
        be.api.setvar("return", "1")
