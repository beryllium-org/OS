print("Early boot log:\n")

from storage import getmount, remount, disable_usb_drive, remount
from supervisor import runtime, status_bar
from sys import path

path.append("/Beryllium/lib")

import cptoml

runtime.autoreload = False
status_bar.console = False

lj_mount = getmount("/")

desired_label = cptoml.fetch("fs_label", "BERYLLIUM")
if desired_label != None:
    desired_label = desired_label.upper()
    if lj_mount.label != desired_label:
        remount("/", False)
        lj_mount.label = desired_label
        print("Reset filesystem label.")
        remount("/", True)

if cptoml.fetch("usb_msc_available", "BERYLLIUM"):
    print("This board supports USB filesystem enumeration.")
    if cptoml.fetch("usb_msc_enabled", "BERYLLIUM"):
        print("The USB filesystem is enabled.\nBeryllium will access root Read-Only!")
    else:
        if cptoml.fetch("usb_msc_onetime", "BERYLLIUM"):
            remount("/", False)
            cptoml.put("usb_msc_onetime", False, "BERYLLIUM")
            remount("/", True)
            print("The USB filesystem is enabled this once.")
            print("Ljinux will access root Read-Only!")
        else:
            disable_usb_drive()
            print("The USB filesystem is disabled.\nBeryllium will operate normally.")
else:
    print("This board does not support USB filesystem enumeration.")


if cptoml.fetch("usb_hid_available", "BERYLLIUM"):
    import usb_hid

    print("This board supports HID enumeration.")

    if cptoml.fetch("usb_hid_enabled", "BERYLLIUM"):
        print("HID Enabled.")
    else:
        usb_hid.disable()
        print("HID Disabled.")
else:
    print("This board does not support HID enumeration.")

if cptoml.fetch("usb_midi_available", "BERYLLIUM"):
    import usb_midi

    print("This board supports MIDI enumeration.")

    if cptoml.fetch("usb_midi_enabled", "BERYLLIUM"):
        print("MIDI Enabled.")
        usb_midi.enable()
    else:
        print("MIDI Disabled.")
else:
    print("This board does not support MIDI enumeration.")
