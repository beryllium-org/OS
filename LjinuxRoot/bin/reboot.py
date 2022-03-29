inpt = ljinux.based.user_vars["argj"].split()
global Exit
global Exit_code
Exit = True
try:
    if inpt[1] == "bootloader":
        Exit_code = 243
    elif inpt[1] == "safemode":
        Exit_code = 242
    elif inpt[1] == "uf2":
        Exit_code = 241
    else:
        raise IndexError
except IndexError:
    Exit_code = 245
