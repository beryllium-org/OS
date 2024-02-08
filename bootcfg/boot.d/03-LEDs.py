systemprints(2, "Setting up LEDs")

vr("type", cptoml.fetch("ledtype", "LJINUX"))

if vr("type").startswith("generic"):
    pass
elif vr("type").startswith("neopixel"):
    pass
elif vr("type").startswith("rgb"):
    pass
else:
    vr("type", None)  # Crash process

ljinux.based.run("modprobe led_" + vr("type"))
ljinux.io.ledtype = "led_" + vr("type")

if ljinux.io.ledtype in ljinux.devices:
    if vr("type").startswith("rgb"):
        pv[0]["digitalio_store"]["LED_RED"] = ljinux.devices["gpiochip"][0].output(
            "LED_RED"
        )
        pv[0]["digitalio_store"]["LED_GREEN"] = ljinux.devices["gpiochip"][0].output(
            "LED_GREEN"
        )
        pv[0]["digitalio_store"]["LED_BLUE"] = ljinux.devices["gpiochip"][0].output(
            "LED_BLUE"
        )

        ljinux.devices[ljinux.io.ledtype][0].setup(
            pv[0]["digitalio_store"]["LED_RED"],
            pv[0]["digitalio_store"]["LED_GREEN"],
            pv[0]["digitalio_store"]["LED_BLUE"],
        )
    else:
        vr("ldn", cptoml.fetch("led", "LJINUX"))
        pv[0]["digitalio_store"][vr("ldn")] = ljinux.devices["gpiochip"][0].output(
            vr("ldn")
        )
        if (
            vr("type").startswith("neopixel")
            and "NEOPIXEL_POWER" in ljinux.devices["gpiochip"][0].pins
        ):
            pv[0]["digitalio_store"]["NEOPIXEL_POWER"] = ljinux.devices["gpiochip"][
                0
            ].output("NEOPIXEL_POWER")
            pv[0]["digitalio_store"]["NEOPIXEL_POWER"].value = 1
        ljinux.devices[ljinux.io.ledtype][0].setup(pv[0]["digitalio_store"][vr("ldn")])
    ljinux.io.led_setup = True
    systemprints(1, "Setting up LEDs")
else:
    systemprints(3, "Setting up LEDs")
