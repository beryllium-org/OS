rename_process("mkuart")
vr("opts", be.api.xarg())
be.api.setvar("return", "1")
vr("uart", None)
if "b" in vr("opts")["o"]:
    if "UART" in be.devices["gpiochip"][0].pins:
        try:
            vr("uart", be.devices["gpiochip"][0].pin("UART", force=True)())
        except ValueError:
            term.write("Could not allocate the predefined UART port!")
    else:
        term.write("This board does not have a predefined UART port!")
elif "t" in vr("opts")["o"] and "r" in vr("opts")["o"]:
    vr("txp", vr("opts")["o"]["t"])
    vr("rxp", vr("opts")["o"]["r"])
    if (
        vr("txp") in be.devices["gpiochip"][0].pins
        and vr("rxp") in be.devices["gpiochip"][0].pins
    ):
        if be.devices["gpiochip"][0].is_free(vr("txp")) and be.devices["gpiochip"][
            0
        ].is_free(vr("rxp")):
            vr(
                "uart",
                busio.UART(
                    tx=be.devices["gpiochip"][0].pin(vr("txp")),
                    rx=be.devices["gpiochip"][0].pin(vr("rxp")),
                ),
            )
        else:
            term.write("The specified pins currently unavailable!")
    else:
        term.write("Invalid pins!")
else:
    be.based.run("cat /usr/share/help/mkuart.txt")

if vr("uart") is not None:
    vr("baud", 115200)
    if "baud" in vr("opts")["o"]:
        try:
            vr("baud", int(vr("opts")["o"]["baud"]))
        except:
            term.write("Invalid baud, keeping 115200!")
    vr("uart").baudrate = vr("baud")
    vr("existing", list(pv[0]["consoles"].keys()))
    vr("index", 0)
    while ("ttyUART" + str(vr("index"))) in vr("existing"):
        vrp("index")
    pv[0]["consoles"]["ttyUART" + str(vr("index"))] = vr("uart")
    dmtex("Created UART console at /dev/ttyUART" + str(vr("index")))
    be.api.setvar("return", "0")
else:
    term.write("No UART port was configured.")
