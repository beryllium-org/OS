rename_process("rmi2c")
vr("opts", be.api.xarg())
be.api.setvar("return", "1")
if len(vr("opts")["w"]):
    vr("node", vr("opts")["w"][0])
    vr("ok", False)
    be.api.subscript("/bin/stringproccessing/devid.py")
    if (
        vr("ok")
        and vr("dev_name") in be.devices.keys()
        and vr("dev_name") == "i2c"
        and vr("dev_id") in be.devices[vr("dev_name")].keys()
    ):
        if be.devices[vr("dev_name")][vr("dev_id")].try_lock():
            be.devices[vr("dev_name")][vr("dev_id")].unlock()
            be.devices[vr("dev_name")][vr("dev_id")].deinit()
            del be.devices[vr("dev_name")][vr("dev_id")]
            be.api.setvar("return", "0")
        else:
            term.write("I2C bus in use!")
    else:
        term.write("Invalid I2C bus!")
else:
    term.write("No bus specified.")
