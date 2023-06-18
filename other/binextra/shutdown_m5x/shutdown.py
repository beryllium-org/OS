ljinux.io.ledset(1)
ljinux.deinit_consoles()
a = digitalio.DigitalInOut(board.BAT_HOLD)
a.switch_to_output()
a.value = 0
while True:
    sleep(100)
