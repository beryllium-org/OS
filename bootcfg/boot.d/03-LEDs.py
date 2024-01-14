systemprints(2, "Setting up LEDs")
ljinux.based.run("modprobe " + ljinux.io.ledtype)
if ljinux.io.ledtype in ljinux.devices:
    if ljinux.io.ledtype.startswith("rgb"):
        ljinux.devices[ljinux.io.ledtype][0].setup(
            ljinux.io.led, ljinux.io.ledg, ljinux.io.ledb
        )
    else:
        ljinux.devices[ljinux.io.ledtype][0].setup(ljinux.io.led)
    ljinux.io.led_setup = True
    systemprints(1, "Setting up LEDs")
else:
    systemprints(3, "Setting up LEDs")
