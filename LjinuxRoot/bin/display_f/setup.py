global display_availability
ljinux.io.ledset(3)  # act
try:
    i2c = busio.I2C(
        pintab[configg["displaySCL"]], pintab[configg["displaySDA"]]
    )  # SCL, SDA
    ljinux.farland.oled = adafruit_ssd1306.SSD1306_I2C(
        128, 64, i2c
    )  # I use the i2c cuz it ez
    del i2c
    ljinux.farland.oled.fill(0)  # cuz why not
    ljinux.farland.oled.show()
    display_availability = True
except (RuntimeError, KeyError, NameError):
    print(
        "Failed to create display object, display functions will be unavailable"
    )
    try:
        del modules["adafruit_ssd1306"]
        del modules["adafruit_framebuf"]
    except KeyError:
        pass
    dmtex("Unloaded display libraries")
ljinux.io.ledset(1)  # idle
