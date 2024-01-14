systemprints(2, "Setting up LEDs")
ljinux.based.run("modprobe " + ljinux.io.ledtype)
if ljinux.io.ledtype in ljinux.modules:
    if ljinux.io.ledtype.startswith("rgb"):
        ljinux.modules[ljinux.io.ledtype].setup(
            ljinux.io.led, ljinux.io.ledg, ljinux.io.ledb
        )
    else:
        ljinux.modules[ljinux.io.ledtype].setup(ljinux.io.led)
    ljinux.io.led_setup = True
    systemprints(1, "Setting up LEDs")
else:
    systemprints(3, "Setting up LEDs")
