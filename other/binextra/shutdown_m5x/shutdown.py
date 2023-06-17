ljinux.io.ledset(1)
ljinux.deinit_consoles()
sleep(1)
a = digitalio.DigitalInOut(board.BAT_HOLD)
a.switch_to_output()
a.value = 0
while True:
    sleep(100)
