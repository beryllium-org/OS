if cptoml.fetch("usb_access", "LJINUX"):
    term.write(
        f"""{colors.red_t}\nWarning:{colors.endc} Developer mode has been enabled!
While it is enabled, Ljinux will only be able to
access the file system {colors.red_t}READ ONLY{colors.endc}.

To disable it, {colors.red_t}set usb_access to 'false'{colors.endc} in '&/settings.toml'!
"""
    )
