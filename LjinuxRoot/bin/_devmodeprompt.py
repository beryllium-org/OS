if cptoml.fetch("usb_msc_available", "LJINUX"):
    try:
        remount("/", False)
        remount("/", True)
    except RuntimeError:
        if cptoml.fetch("usb_msc_enabled", "LJINUX"):
            term.write(
                f"""\n{colors.red_t}Warning:{colors.endc} USB filesystem is permenantly enabled!
While it is enabled, Ljinux will only be able to
access the file system {colors.red_t}READ ONLY{colors.endc}.

To disable it, {colors.red_t}set usb_msc_enabled to 'false'{colors.endc} in '&/settings.toml'!
"""
            )
        else:
            term.write(
                f"""\n{colors.red_t}Warning:{colors.endc} USB filesystem is enabled for this boot!

Please reboot to perform write operations from ljinux.
"""
            )
