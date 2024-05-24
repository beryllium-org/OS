rename_process("mki2c")
vr("opts", be.api.xarg())
vr("i2cbus", None)
vr("scl", None)
vr("sda", None)

if "b" in vr("opts")["o"] or "board" in vr("opts")["o"]:
    vr("i2cbus", be.devices["gpiochip"][0].pin("I2C", force=True)())
elif "d" in vr("opts")["o"] and "c" in vr("opts")["o"]:
    vr("scl", vr("opts")["o"]["c"])
    vr("sda", vr("opts")["o"]["d"])
elif "sda" in vr("opts")["o"] and "scl" in vr("opts")["o"]:
    vr("scl", vr("opts")["o"]["scl"])
    vr("sda", vr("opts")["o"]["sda"])
else:
    term.write("aaaa")

if vr("scl"):
    vr("i2cbus", be.devices["gpiochip"][0].i2c(vr("scl"), vr("sda")))

be.api.setvar("return", "1")
if vr("i2cbus"):
    be.based.run("mknod i2c")
    vr("node", be.api.getvar("return"))
    be.api.subscript("/bin/stringproccessing/devid.py")
    be.devices["i2c"][vr("dev_id")] = vr("i2cbus")
    be.api.setvar("return", "0")
