from os import system, mkdir, listdir, path, popen
from platform import uname
from getpass import getuser
from sys import argv


def errexit():
    print("Compilation error, exiting")
    exit(1)


optimis = "-O4"
try:
    if argv[1] == "debug":
        print("Alert: Compiling with debug enabled.")
        optimis = ""
except IndexError:
    pass

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

print("[1/7] Compiling source files\n")
for filee in listdir():
    if filee.endswith(".py"):
        print(f"-> {filee[:-3]}")
        a = system(
            f"{mpyn} ./{filee} -s {filee[:-3]} -v {optimis} -o {picop}/lib/{filee[:-3]}.mpy".replace(
                "/", slash
            )
        )
        if a != 0:
            errexit()
        del a

print("\n[2/7] Compiling jcurses\n")
for filee in listdir("jcurses"):
    if filee.endswith(".py"):
        print(f"-> {filee[:-3]}")
        a = system(
            f"{mpyn} ./jcurses/{filee} -s {filee[:-3]} -v {optimis} -o {picop}/lib/{filee[:-3]}.mpy".replace(
                "/", slash
            )
        )
        if a != 0:
            errexit()
        del a

print("\n[3/7] Copying base files\n")
for filee in listdir("../rootfilesystem/".replace("/", slash)):
    print(f"-> {filee}")
    system(
        f"cp ../rootfilesystem/{filee} {picop}/".replace("/", slash).replace("cp", copy)
    )

print("\n[4/7] Compiling Adafruit hashlib\n")
if system(f"test -d {picop}/lib/adafruit_hashlib".replace("/", slash)) != 0:
    print("Created adafruit_hashlib directory.")
    mkdir(f"{picop}/lib/adafruit_hashlib".replace("/", slash))
for filee in listdir(
    "../other/Adafruit_CircuitPython_hashlib/adafruit_hashlib/".replace("/", slash)
):
    print(f"-> {filee}")
    a = system(
        f"{mpyn} ../other/Adafruit_CircuitPython_hashlib/adafruit_hashlib/{filee} -s {filee[:-3]} -v {optimis} -o {picop}/lib/adafruit_hashlib/{filee[:-3]}.mpy".replace(
            "/", slash
        )
    )
    if a != 0:
        errexit()
    del a

print("\n[5/7] Compiling Adafruit hid\n")
if system(f"test -d {picop}/lib/adafruit_hid".replace("/", slash)) != 0:
    print("Created adafruit_hid directory.")
    mkdir(f"{picop}/lib/adafruit_hid".replace("/", slash))
for filee in listdir(
    "../other/Adafruit_CircuitPython_HID/adafruit_hid/".replace("/", slash)
):
    print(f"-> {filee}")
    a = system(
        f"{mpyn} ../other/Adafruit_CircuitPython_HID/adafruit_hid/{filee} -s {filee[:-3]} -v {optimis} -o {picop}/lib/adafruit_hid/{filee[:-3]}.mpy".replace(
            "/", slash
        )
    )
    if a != 0:
        errexit()
    del a

print("\n[6/7] Compiling Adafruit ntp\n")
print(f"-> adafruit_ntp.py")
a = system(
    f"{mpyn} ../other/Adafruit_CircuitPython_NTP/adafruit_ntp.py -s adafruit_ntp -v {optimis} -o {picop}/lib/adafruit_ntp.mpy".replace(
        "/", slash
    )
)
if a != 0:
    print("Compilation error, exiting")
    exit(1)
del a

print("\n[7/7] Compiling jz\n")
print(f"-> jz_board.py")
a = system(
    f"{mpyn} ./jz/jz_board.py -s jz_board -v {optimis} -o {picop}/lib/jz.mpy".replace(
        "/", slash
    )
)
if a != 0:
    errexit()
del a

system("sync")
print()
del ami, picop, mpyn, optimis, errexit
