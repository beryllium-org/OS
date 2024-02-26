# Porting Beryllium OS

These instructions are seperated into 3 big steps:

1) Verify your board will actually be able to run it.<br />
    gc.mem_free() should be at least 100000 for the kernel to be able to function.<br />
    Your board should have at least one serial port, or wifi.<br />
    <br />
2) From within "Boardfiles", copy and modify a similar board's folder.<br />
    For the settings.toml, you need to edit the led to match the respective pin for your board, and set the type.<br />
     The supported types are "neopixel", "neopixel_invert", "generic", "generic_invert", "rgb" and "rgb_invert".<br />
     "generic" is any simple on / off led.<br />
     "neopixel" is for neopixel leds.<br />
     "rgb" is for tri-color leds.<br />
    <br />
    For the pinout.map, you need to create a ascii pinout for the board.<br />
     If you feel too uncreative, you can skip it.<br />
    <br />
    For the extras, include whatever modules your board's hardware needs.<br />
    For example, or adding native wifi support, create a file named <code>driver_wifi.driver</code> in folder extras.<br />
    Files in extras that have their name end with .driver will pull a .py file from other/drivers.<br />
    Files in extras that have their name end with .other will pull from other/ a file or a folder.<br />
    To include a folder deeper in other/, use dots in place of slashes, for example, to include other/Adafruit_CircuitPython_HTTPServer/, create a file named "Adafruit_CircuitPython_HTTPServer.adafruit_httpserver.other".<br />
    <br />
3) Test your changes by loading beryllium onto the board.<br />
