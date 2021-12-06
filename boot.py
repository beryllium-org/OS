import usb_cdc
import board
import digitalio
import storage
import supervisor

securityPin = digitalio.DigitalInOut(board.GP0)
powerpin = digitalio.DigitalInOut(board.GP1)
securityPin.switch_to_input(pull=digitalio.Pull.DOWN)
powerpin.switch_to_output()
powerpin.value = True

if(securityPin.value != True):
    storage.disable_usb_drive()
    #usb_cdc.disable()
    print("Locked")
else:
    print("Unlocked")
supervisor.disable_autoreload()
