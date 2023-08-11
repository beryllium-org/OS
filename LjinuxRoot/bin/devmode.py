rename_process("devmode")
if not cptoml.fetch("usb_access", "LJINUX"):
    vr("opts", ljinux.api.xarg())
    vr("cont", True)
    if "q" not in vr("opts")["o"]:  # -q skips message & delay
        term.write(
            "Enabling ljinux developer mode in 5 seconds..\n"
            + "Keep in mind that the board will restart immediately after it's enabled.\n"
            + "Press 'Ctrl + C' to abort"
        )
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            vr("cont", False)
            term.write("Aborted.")
            ljinux.api.setvar("return", "1")
    if vr("cont"):
        remount("/", False)
        cptoml.put("usb_access", True, "LJINUX")
        remount("/", True)
        vr("Exit", True, pid=0)
        vr("Exit_code", 245, pid=0)
else:
    term.write(
        "Developer mode already enabled! To disable it, set 'usb_access' to 'false' in '&/settings.toml'."
    )
