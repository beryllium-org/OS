import board
from digitalio import DigitalInOut
from digitalio import Pull
from storage import disable_usb_drive
from storage import getmount
from storage import remount
from supervisor import disable_autoreload
from gc import collect

securityPin = DigitalInOut(board.GP0)
powerpin = DigitalInOut(board.GP1)
securityPin.switch_to_input(pull=Pull.DOWN)
powerpin.switch_to_output()
powerpin.value = True

remount("/", readonly=False)
m = getmount("/")
m.label = "Ljinux"
remount("/", readonly=True)

if(securityPin.value != True):
    disable_usb_drive()
    print("Locked")
else:
    print("Unlocked")
disable_autoreload()

securityPin.deinit()
powerpin.deinit()
del securityPin
del powerpin
collect()
