rename_process("devmode")
if not cptoml.fetch("usb_access", "LJINUX"):
    pv[get_pid()]["opts"] = ljinux.api.xarg()
    pv[get_pid()]["cont"] = True
    if "q" not in pv[get_pid()]["opts"]["o"]:  # -q skips message & delay
        term.write(
            "Enabling ljinux developer mode in 5 seconds..\n"
            + "Keep in mind that the board will restart immediately after it's enabled.\n"
            + "Press 'Ctrl + C' to abort"
        )
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            pv[get_pid()]["cont"] = False
            term.write("Aborted.")
            ljinux.api.setvar("return", "1")
    if pv[get_pid()]["cont"]:
        remount("/", False)
        cptoml.put("usb_access", True, "LJINUX")
        remount("/", True)
        pv[0]["Exit"] = True
        pv[0]["Exit_code"] = 245
else:
    term.write(
        "Developer mode already enabled! To disable it, set 'usb_access' to 'false' in '&/settings.toml'."
    )
