print(
    "Enabling ljinux developer mode..\nKeep in mind the pico will restart automatically, after it's enabled."
)
time.sleep(5)
try:
    f = open("/devm", "r")
    f.close()
    print(
        'based: Error: file exists\nIf you want to disable developer mode, delete the file "devm" from the pico\'s built in filesystem and powercycle it.'
    )
except OSError:
    remount("/", False)
    f = open("/devm", "w")
    f.close()
    remount("/", True)
    global Exit
    global Exit_code
    Exit = True
    Exit_code = 245 
