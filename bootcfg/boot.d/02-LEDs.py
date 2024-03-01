systemprints(2, "Setting up LEDs")

vr("type", cptoml.fetch("ledtype", "BERYLLIUM"))

if vr("type").startswith("generic"):
    pass
elif vr("type").startswith("neopixel"):
    pass
elif vr("type").startswith("rgb"):
    pass
else:
    vr("type", None)  # Crash process

be.based.run("modprobe led_" + vr("type"))
be.io.ledtype = "led_" + vr("type")

if be.io.ledtype in be.devices:
    if vr("type").startswith("rgb"):
        pv[0]["digitalio_store"]["LED_RED"] = be.devices["gpiochip"][0].output(
            "LED_RED"
        )
        pv[0]["digitalio_store"]["LED_GREEN"] = be.devices["gpiochip"][0].output(
            "LED_GREEN"
        )
        pv[0]["digitalio_store"]["LED_BLUE"] = be.devices["gpiochip"][0].output(
            "LED_BLUE"
        )

        be.devices[be.io.ledtype][0].setup(
            pv[0]["digitalio_store"]["LED_RED"],
            pv[0]["digitalio_store"]["LED_GREEN"],
            pv[0]["digitalio_store"]["LED_BLUE"],
        )
    else:
        vr("ldn", cptoml.fetch("led", "BERYLLIUM"))
        pv[0]["digitalio_store"][vr("ldn")] = be.devices["gpiochip"][0].output(
            vr("ldn")
        )
        if (
            vr("type").startswith("neopixel")
            and "NEOPIXEL_POWER" in be.devices["gpiochip"][0].pins
        ):
            pv[0]["digitalio_store"]["NEOPIXEL_POWER"] = be.devices["gpiochip"][
                0
            ].output("NEOPIXEL_POWER")
            pv[0]["digitalio_store"]["NEOPIXEL_POWER"].value = 1
        be.devices[be.io.ledtype][0].setup(pv[0]["digitalio_store"][vr("ldn")])
    be.io.led_setup = True
    systemprints(1, "Setting up LEDs")
else:
    systemprints(3, "Setting up LEDs")
