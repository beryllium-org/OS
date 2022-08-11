from os import system, mkdir, listdir, path, popen
from platform import uname
from getpass import getuser

if uname().system == "Linux":
    slash = "/"
    copy = "cp"
else:
    slash = "\\"
    copy = "copy"
ami = getuser()
mpyn = f"../scripts/mpy-cross-{uname().machine}"
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
        if vol.readline()[:-1].split(" ")[-1].upper() == "CIRCUITPY":
            picop = f"%s" % _
        vol.close()
        if picop != "":
            break
if picop == "":
    print(
        "Error: Board not found.\nMake sure it is attached and mounted before you run make"
    )
    exit(1)

print(f"\nUsing mpycross: {mpyn}")
print(f"Using board path: {picop}\n")

if system(f"test -d {picop}/lib".replace("/", slash)) != 0:
    print("Created lib directory.")
    mkdir(f"{picop}/lib".replace("/", slash))

if system(f"test -d {picop}/lib/drivers".replace("/", slash)) != 0:
    print("Created lib/drivers directory.")
    mkdir(f"{picop}/lib/drivers".replace("/", slash))

print(" - [1/1] Compiling wifi drivers\n")

print(f" ---> wifi")
a = system(
    f"{mpyn} ../other/drivers/wifi.py -s driver_wifi -v -O4 -o {picop}/lib/drivers/driver_wifi.mpy".replace(
        "/", slash
    )
)

print(f" ---> adafruit_requests")
b = system(
    f"{mpyn} ../other/Adafruit_CircuitPython_Requests/adafruit_requests.py -s adafruit_requests -v -O4 -o {picop}/lib/adafruit_requests.mpy".replace(
        "/", slash
    )
)

if a != 0 or b != 0:
    print("Compilation error, exiting")
    exit(1)
del a, b

system("sync")
print()
del ami, picop, mpyn
