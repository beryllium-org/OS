inpt = ljinux.based.user_vars["argj"].split()
global Exit
global Exit_code
Exit = True
try:
    if inpt[1] == "bootloader":
        Exit_code = 243
        print(
            "Please disconnect from serial to continue..\nTo continue anyways, press Ctrl + C"
        )
        try:
            while console.connected:
                time.sleep(0.2)
        except KeyboardInterrupt:
            pass
    elif inpt[1] == "safemode":
        Exit_code = 242
    elif inpt[1] == "uf2":
        Exit_code = 241
    else:
        raise IndexError
except IndexError:
    Exit_code = 245
