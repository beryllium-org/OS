class neopixel_colors:
    """
    Ljinux colors for the neopixel led
    """

    idle = bytearray([3, 0, 0])  # for idling in terminal
    idletype = bytearray([2, 0, 0])  # alternative idle, to indicate input

    activity = bytearray([5, 5, 0])  # loading nuclear launch codes

    waiting = bytearray([0, 0, 5])  # done with init, waiting for serial

    error = bytearray([0, 50, 0])  # when errors occur

    killtheuser = bytearray([255, 255, 255])  # kekw

    off = bytearray([0, 0, 0])  # power off the led
