from storage import disable_usb_drive
from storage import getmount
from storage import remount
from supervisor import disable_autoreload
from gc import collect

devf = False

try:
    f = open('/devm','r')
    print("Development mode file detected")
    f.close()
    devf = True
except OSError:
    pass

remount("/", readonly=False)
m = getmount("/")
m.label = "Ljinux"
remount("/", readonly=True)

if(devf != True):
    disable_usb_drive()
    print("Locked")
else:
    print("Unlocked")
disable_autoreload()
collect()
