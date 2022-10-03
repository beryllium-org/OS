from storage import getmount, remount, disable_usb_drive

try:
    from supervisor import disable_autoreload
except ImportError:
    from supervisor import runtime

    def disable_autoreload():
        runtime.autoreload = False


try:
    from supervisor import status_bar

    status_bar.console = False
    del status_bar
except ImportError:
    pass
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
lj_mount = getmount("/")
print("I", end="")
desired_label = "ljinux"
if lj_mount.label != desired_label:
    remount("/", readonly=False)
    lj_mount.label = desired_label
    remount("/", readonly=True)
del desired_label, lj_mount

print("N", end="")
if not devf:
    try:
        disable_usb_drive()
    except RuntimeError:
        pass
print("U", end="")
disable_autoreload()
print("X boot core\n" + "-" * 16 + "\nOutput:\n" + stash)
del devf, stash, disable_autoreload, disable_usb_drive, remount, getmount
try:
    del runtime
except:
    pass
