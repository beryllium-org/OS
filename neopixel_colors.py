class neopixel_colors:
    """
    Ljinux colors for the neopixel led
    """
    
    idle = bytearray([3,0,0]) # for idling in terminal
    idletype = bytearray([2,0,0]) # whilst chars are being inputted
    
    activity = bytearray()
    
    waiting = bytearray([0,0,5]) # done with init, waiting for serial
    
    error = bytearray([0,10,0])
    
    killtheuser = bytearray([255,255,255]) # kekw
