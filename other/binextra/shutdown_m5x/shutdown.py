ljinux.io.ledset(1)
ljinux.deinit_consoles()
sleep(1)
from board import BAT_HOLD

a = digitalio.DigitalInOut(BAT_HOLD)
a.switch_to_output()
a.value = 0
while True:
    sleep(100)
