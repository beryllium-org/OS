print("""
Enabling ljinux developer mode..
Keep in mind the pico will restart automatically, after it's enabled.
""")

time.sleep(5)

try:
    with open("/devm", "r") as f:
        print(
            'based: Error: file exists\n',
            'If you want to disable developer mode,',
            'delete the file "devm" from the pico\'s built in filesystem and powercycle it.'
        )    
    
except OSError:
    remount("/", False)
    
    with open("/devm", "w") as f:
        remount("/", True)
        global Exit
        global Exit_code
        Exit = True
        Exit_code = 245
