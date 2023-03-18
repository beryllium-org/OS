from storage import getmount, remount, disable_usb_drive
from supervisor import runtime, status_bar
from cptoml import fetch

runtime.autoreload = False
status_bar.console = False
print("-" * 16 + "\nL", end="")

devm = fetch("usb_access", "LJINUX")
stash = ""
if devm:
    stash = "Development mode usb_access has been enabled!\n"
print("J", end="")

lj_mount = getmount("/")
print("I", end="")

desired_label = "ljinux"
if lj_mount.label != desired_label:
    remount("/", False)
    lj_mount.label = desired_label
    remount("/", True)
print("N", end="")

if not devm:
    try:
        disable_usb_drive()
    except RuntimeError:
        pass
print("UX boot core\n" + "-" * 16 + "\nOutput:\n" + stash)
