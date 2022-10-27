opts = ljinux.api.xarg()

try:
    f = open("/devm", "r")
    f.close()
    print(
        'Error: file exists\nIf you want to disable developer mode, delete the file "devm" from the board\'s USB filesystem and powercycle it.'
    )
except OSError:
    if "q" not in opts["o"]:  # -q skips message & delay
        print(
            "Enabling ljinux developer mode..\nKeep in mind that the board will restart automatically, after it's enabled."
        )
        time.sleep(5)
    remount("/", False)
    f = open("/devm", "w")
    f.close()
    remount("/", True)
    global Exit
    global Exit_code
    Exit = True
    Exit_code = 245
