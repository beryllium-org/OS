print("Early boot log:\n")

from storage import getmount, remount, disable_usb_drive
from supervisor import runtime, status_bar
from cptoml import fetch

runtime.autoreload = False
status_bar.console = False

lj_mount = getmount("/")

desired_label = fetch("fs_label", "LJINUX")
if desired_label != None:
    desired_label = desired_label.upper()
    if lj_mount.label != desired_label:
        remount("/", False)
        lj_mount.label = desired_label
        print("Reset filesystem label.\n")
        remount("/", True)

if fetch("usb_msc_available", "LJINUX"):
    print("This board supports USB filesystem enumeration.")
    if fetch("usb_msc_enabled", "LJINUX"):
        print("The USB filesystem is enabled.\nLjinux will access root Read-Only!\n")
    else:
        disable_usb_drive()
        print("The USB filesystem is disabled.\nLjinux will operate normally.\n")
else:
    print("This board does not support USB filesystem enumeration.\n")


if fetch("usb_hid_available", "LJINUX"):
    import usb_hid

    print("This board supports HID enumeration.")

    if fetch("usb_hid_enabled", "LJINUX"):
        print("HID Enabled.\n")
    else:
        usb_hid.disable()
        print("HID Disabled.\n")
else:
    print("This board does not support HID enumeration.\n")

if fetch("usb_midi_available", "LJINUX"):
    import usb_midi

    print("This board supports MIDI enumeration.")

    if fetch("usb_midi_enabled", "LJINUX"):
        print("MIDI Enabled.")
        usb_midi.enable()
    else:
        print("MIDI Disabled.")
else:
    print("This board does not support MIDI enumeration.")
