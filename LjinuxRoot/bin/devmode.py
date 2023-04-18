if not cptoml.fetch("usb_access", "LJINUX"):
    opts = ljinux.api.xarg()
    cont = True
    if "q" not in opts["o"]:  # -q skips message & delay
        term.write(
            "Enabling ljinux developer mode in 5 seconds..\n"
            + "Keep in mind that the board will restart immediately after it's enabled.\n"
            + "Press 'Ctrl + C' to abort"
        )
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            cont = False
            term.write("Aborted.")
            ljinux.api.setvar("return", "1")
    if cont:
        remount("/", False)
        cptoml.put("usb_access", True, "LJINUX")
        remount("/", True)
        global Exit
        global Exit_code
        Exit = True
        Exit_code = 245
    del opts, cont
else:
    term.write(
        "Developer mode already enabled! To disable it, set 'usb_access' to 'false' in '&/settings.toml'."
    )
