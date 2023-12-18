from storage import getmount, remount, disable_usb_drive
from supervisor import runtime, status_bar
from cptoml import fetch

runtime.autoreload = False
status_bar.console = False

stash = ""

lj_mount = getmount("/")

desired_label = fetch("fs_label", "LJINUX")
if desired_label != None:
    desired_label = desired_label.upper()
    if lj_mount.label != desired_label:
        remount("/", False)
        lj_mount.label = desired_label
        stash += "Reset filesystem label.\n\n"
        remount("/", True)

if fetch("usb_msc_available", "LJINUX"):
    stash += "This board supports USB filesystem enumeration.\n"
    if fetch("usb_msc_enabled", "LJINUX"):
        stash += "USB filesystem is enabled.\nLjinux will access root Read-Only!\n\n"
    else:
        disable_usb_drive()
        stash += (
            "USB filesystem is disabled.\nLjinux will operate in root Read-Write.\n\n"
        )
else:
    stash += "This board does not support USB filesystem enumeration.\n\n"


if fetch("usb_hid_available", "LJINUX"):
    import usb_hid

    stash += "This board supports HID enumeration.\n"

    if fetch("usb_hid_enabled", "LJINUX"):
        stash += "HID Enabled.\n\n"
    else:
        usb_hid.disable()
        stash += "Disabled HID.\n\n"

if fetch("usb_midi_available", "LJINUX"):
    import usb_midi

    stash += "This board supports MIDI enumeration.\n"

    if fetch("usb_midi_enabled", "LJINUX"):
        stash += "HID Enabled.\n\n"
        usb_midi.enable()
    else:
        stash += "Disabled HID.\n\n"

print("Early boot log:\n" + stash)
