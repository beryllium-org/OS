from storage import (
    disable_usb_drive, 
    getmount, 
    remount
)

from supervisor import disable_autoreload

print('-' * 16 + "\nL",end="")

devf = False
stash = ""

try:
    with open('/devm', 'r') as f: 
        stash += "Development mode file detected\n"
    devf = not devf

except OSError:
    pass

print("J",end="")

if(devf != True):
    disable_usb_drive()
    print("IN",end="")
    
else:
    remount("/", readonly=False
            )
    print("I",end="")
    m = getmount("/")
    m.label = "Ljinux"
    
    remount("/", readonly=True)
    print("N",end="")
    
print("UX",end="")
disable_autoreload()

print(" boot core\n" + '-' * 16)
print("Output:\n", stash)
