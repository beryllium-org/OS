rename_process("rmnod")
vr("opts", be.api.xarg())
be.api.setvar("return", "1")
if len(vr("opts")["w"]):
    vr("node", vr("opts")["w"][0])
    vr("ok", False)
    be.api.subscript("/bin/stringproccessing/devid.py")
    if (
        vr("ok")
        and vr("dev_name") in be.devices.keys()
        and vr("dev_id") in be.devices[vr("dev_name")].keys()
    ):
        del be.devices[vr("dev_name")][vr("dev_id")]
        if not be.devices[vr("dev_name")]:
            del be.devices[vr("dev_name")]
        be.api.setvar("return", "0")
    else:
        term.write("Invalid node!")
else:
    be.based.error(1)
