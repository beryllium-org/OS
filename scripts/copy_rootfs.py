from os import system, mkdir, listdir, path, popen
from platform import uname
from getpass import getuser

ami = getuser()
picop = ""
if system(f"test -d /media/{ami}/LJINUX") == 0:
    picop = f"/media/{ami}/LJINUX"
elif system(f"test -d /media/{ami}/CIRCUITPY") == 0:
    picop = f"/media/{ami}/CIRCUITPY"
elif system(f"test -d /media/CIRCUITPY") == 0:
    picop = f"/media/CIRCUITPY"
elif system("test -d /Volumes/LJINUX") == 0:
    picop = "/Volumes/LJINUX"
elif system("test -d /Volumes/CIRCUITPY") == 0:
    picop = "/Volumes/CIRCUITPY"
elif uname().system == "Windows":
    mpyn = f"..\scripts\mpy-cross-windows"
    drives = [chr(x) + ":" for x in range(65, 91) if path.exists(chr(x) + ":")]
    for _ in drives:
        vol = popen("vol " + _)
        if vol.readline()[:-1].split(" ")[-1].upper() in ["CIRCUITPY", "LJINUX"]:
            picop = f"%s" % _
        vol.close()
        if picop != "":
            break
if picop == "":
    print(
        "Error: Board not found.\nMake sure it is attached and mounted before you run make"
    )
    exit(1)

print("\n[Copying root files\n")
if uname().system == "Linux":
    if system(f"test -d {picop}/LjinuxRoot") != 0:
        print("Created LjinuxRoot")
        mkdir(f"{picop}/LjinuxRoot")
    print(f"cp -rv ../LjinuxRoot/* {picop}/LjinuxRoot/")
    system(f"cp -rv ../LjinuxRoot/* {picop}/LjinuxRoot/")
    print(f"cp -v ../Manual.txt {picop}/LjinuxRoot/home/pi/")
    system(f"cp -v ../Manual.txt {picop}/LjinuxRoot/home/pi/")
else:
    print(f"xcopy /y/s ..\\LjinuxRoot\\* {picop}\\LjinuxRoot\\")
    system(f"xcopy /y/s ..\\LjinuxRoot\\* {picop}\\LjinuxRoot\\")
    print(f"copy ..\\Manual.txt {picop}\\LjinuxRoot\\home\\pi\\")
    system(f"copy ..\\Manual.txt {picop}\\LjinuxRoot\\home\\pi\\")