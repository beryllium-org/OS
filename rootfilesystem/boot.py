from storage import getmount, remount, disable_usb_drive
from supervisor import disable_autoreload

print("-" * 16 + "\nL", end="")

devf = False
stash = ""

try:
    with open("/devm", "r") as f:
        stash = "Development mode file detected\n"
    devf = not devf

except OSError:
    pass

print("J", end="")
remount("/", readonly=False)
print("I", end="")

lj_mount = getmount("/")
lj_mount.label = "lJinux"
del lj_mount

remount("/", readonly=True)
print("N", end="")

if not devf:
    disable_usb_drive()
    print("IN", end="")

disable_autoreload()
print("UX boot core\n" + "-" * 16 + "\nOutput:\n" + stash)

del devf, stash, disable_autoreload, disable_usb_drive, remount, getmount
