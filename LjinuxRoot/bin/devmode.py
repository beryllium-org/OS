try:
    with open("/devm", "r"):
        pass
    term.write(
        'Error: file exists\nIf you want to disable developer mode, delete the file "devm" from the board\'s USB filesystem and powercycle it.'
    )
except OSError:
    opts = ljinux.api.xarg()
    try:
        if "q" not in opts["o"]:  # -q skips message & delay
            term.write(
                "Enabling ljinux developer mode..\nKeep in mind that the board will restart automatically, after it's enabled."
            )
            time.sleep(5)
        del opts
        remount("/", False)
        f = open("/devm", "w")
        f.close()
        remount("/", True)
        global Exit
        global Exit_code
        Exit = True
        Exit_code = 245
    except KeyboardInterrupt:
        print("Aborted.")
        del opts
        ljinux.api.setvar("return", "1")
