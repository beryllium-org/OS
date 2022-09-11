from os import system, mkdir, listdir, path, popen
from platform import uname
from getpass import getuser
from sys import argv
from detect_board import detect_board


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
mpyn = f"../scripts/mpy-cross-{uname().machine}"

[picop, board] = detect_board()

if board == "":
    print(
        "Error: Board not found.\nMake sure it is attached and mounted before you run make"
    )
    exit(1)

print(f"\nUsing mpycross: {mpyn}")
print(f"Using board path: {picop}")
print(f"Building for board: {board}\n")

if system(f"test -d {picop}/lib".replace("/", slash)) != 0:
    print("Created lib directory.")
    mkdir(f"{picop}/lib".replace("/", slash))

print("[1/6] Compiling source files\n")
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

print("\n[2/6] Compiling jcurses\n")
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

print("\n[3/6] Copying base files\n")
for filee in listdir("../rootfilesystem/".replace("/", slash)):
    print(f"-> {filee}")
    system(
        f"cp ../rootfilesystem/{filee} {picop}/".replace("/", slash).replace("cp", copy)
    )

print("\n[4/6] Copying board configuration files\n")
print("-> config")
system(
    f"cp ../Boardfiles/{board}/config.json {picop}/".replace("/", slash).replace(
        "cp", copy
    )
)
print("-> pintab")
a = system(
    f"{mpyn} ../Boardfiles/{board}/pintab.py -s pintab -v -O4 -o {picop}/lib/pintab.mpy".replace(
        "/", slash
    )
)
if a != 0:
    errexit()

print("\n[5/7] Compiling Adafruit hashlib\n")
if system(f"test -d {picop}/lib/adafruit_hashlib".replace("/", slash)) != 0:
    print("Created adafruit_hashlib directory.")
    mkdir(f"{picop}/lib/adafruit_hashlib".replace("/", slash))
for filee in listdir(
    "../other/Adafruit_CircuitPython_hashlib/adafruit_hashlib/".replace("/", slash)
):
    print(f"-> {filee[:-3]}")
    a = system(
        f"{mpyn} ../other/Adafruit_CircuitPython_hashlib/adafruit_hashlib/{filee} -s {filee[:-3]} -v -O4 -o {picop}/lib/adafruit_hashlib/{filee[:-3]}.mpy".replace(
            "/", slash
        )
    )
    if a != 0:
        errexit()

print("\n[6/7] Compiling Adafruit hid\n")
if system(f"test -d {picop}/lib/adafruit_hid".replace("/", slash)) != 0:
    print("Created adafruit_hid directory.")
    mkdir(f"{picop}/lib/adafruit_hid".replace("/", slash))
for filee in listdir(
    "../other/Adafruit_CircuitPython_HID/adafruit_hid/".replace("/", slash)
):
    print(f"-> {filee[:-3]}")
    a = system(
        f"{mpyn} ../other/Adafruit_CircuitPython_HID/adafruit_hid/{filee} -s {filee[:-3]} -v -O4 -o {picop}/lib/adafruit_hid/{filee[:-3]}.mpy".replace(
            "/", slash
        )
    )
    if a != 0:
        errexit()

print("\n[7/7] Compiling jz\n")
print("-> jz_board")
a = system(
    f"{mpyn} ./jz/jz_board.py -s jz_board -v {optimis} -o {picop}/lib/jz.mpy".replace(
        "/", slash
    )
)
if a != 0:
    errexit()

system("sync")
print()
