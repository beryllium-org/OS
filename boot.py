from storage import disable_usb_drive
from storage import getmount
from storage import remount
from supervisor import disable_autoreload
from gc import collect
print("----------------\nL",end="")
devf = False
stash = ""
try:
    f = open('/devm','r')
    stash += "Development mode file detected\n"
    f.close()
    devf = True
except OSError:
    pass
collect()
print("J",end="")
if(devf != True):
    disable_usb_drive()
    print("IN",end="")
else:
    remount("/", readonly=False)
    print("I",end="")
    m = getmount("/")
    m.label = "Ljinux"
    remount("/", readonly=True)
    collect()
    print("N",end="")
collect()
print("UX",end="")
disable_autoreload()
print(" boot core\n----------------")
print("Output:\n"+stash)
del stash
collect()
