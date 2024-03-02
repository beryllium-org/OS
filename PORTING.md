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
    For packages.txt you need to include all the packages this board needs.<br />
    You are advised to view similar boards's packages.txt<br />
    <br />
    For drivers.txt just like packages, include what is needed for all the board to work fully out of the box.<br />
    If something you want doesn't exist, you may make it, or skip it.<br />
    <br />
    For both packages.txt and drivers.txt you should only have one item per line, followed by no spaces or comments.<br />
    <br />
3) Test your changes by loading beryllium onto the board.<br />
    Ensure the status led works, and the statuses are not inverted and that all the needed packages are preinstalled.<br />
