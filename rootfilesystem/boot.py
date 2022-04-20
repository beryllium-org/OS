print("-" * 16 + "\nL", end="")

devf = False
stash = ""

try:
    with open("/devm", "r") as f:
        stash += "Development mode file detected\n"
    devf = not devf

except OSError:
    pass

print("J", end="")

if devf:
    from storage import getmount, remount

    remount("/", readonly=False)
    print("I", end="")
    m = getmount("/")
    m.label = "Ljinux"
    del m
    remount("/", readonly=True)
    print("N", end="")
else:
    from storage import disable_usb_drive
    disable_usb_drive()
    print("IN", end="")

from supervisor import disable_autoreload

disable_autoreload()
print("UX boot core\n" + "-" * 16 + "\nOutput:\n" + stash)
del stash
del devf
