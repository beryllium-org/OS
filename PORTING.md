# Porting ljinux

These instructions are seperated into 3 big steps:

1) Verify your board will actually be able to run ljinux.<br />
    gc.mem_free() should be at least 100000 for ljinux to be able to function.<br />
    Only wifi and usb workflows supported.<br />
    <br />
2) From within "Boardfiles", copy and modify a similar board's folder.<br />
    For the config.json, you need to edit the led to match the respective pin for your board, and set the type.<br />
     If the pin is on board.LED set the value to -1.<br />
     The supported types are "neopixel", "generic" and "generic_invert".<br />
     "generic" is any simple on / off led.<br />
     "generic_invert" is the same but with inverted states.<br />
     "neopixel" is for neopixel leds (duh).<br />
    <br />
    For the pinout.map, you need to create a ascii pinout for the board.<br />
     If you feel too uncreative, you can skip it,<br />
      but your board will not be supported, till I have the time to make the pinout.<br />
    <br />
    For the pintab.py, you need to properly add all the user accessible pins of the board module.<br />
     <code>import board;dir(board)</code><br />
     Make sure not to add duplicate pins, or the board.LED.<br />
    <br />
3) Test your changes by loading ljinux onto the board.
    "make install" will update the config.
