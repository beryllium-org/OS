from os import system, mkdir, listdir, uname
from getpass import getuser

ami = getuser()
mpyn = f"../scripts/mpy-cross-{uname().machine}"
print(f"\nUsing mpycross: {mpyn}")
if system(f"test -d /media/{ami}/LJINUX") == 0:
    picop = f"/media/{ami}/LJINUX"
elif system(f"test -d /media/{ami}/CIRCUITPY") == 0:
    picop = f"/media/{ami}/CIRCUITPY"
elif system("test -d /Volumes/LJINUX") == 0:
    picop = "/Volumes/LJINUX"
elif system("test -d /Volumes/CIRCUITPY") == 0:
    picop = "/Volumes/CIRCUITPY"
else:
    print(
        "Error: Board not found.\nMake sure it is attached and mounted before you run make"
    )
    exit(1)

print(f"Using board path: {picop}\n")
if system(f"test -d {picop}/lib") != 0:
    print("Created lib directory.")
    mkdir(f"{picop}/lib")

print("[1/3] Compiling source files and pin allocation tabs\n")
for filee in listdir():
    if filee.endswith(".py"):
        print(f"-> {filee[:-3]}")
        a = system(
            f"{mpyn} ./{filee} -s {filee[:-3]} -v -O4 -o {picop}/lib/{filee[:-3]}.mpy"
        )
        if a != 0:
            print("Compilation error, exiting")
            exit(1)
        del a

print("\n[2/3] Copying base files\n")
for filee in listdir("../rootfilesystem/"):
    print(f"-> {filee}")
    system(f"cp ../rootfilesystem/{filee} {picop}/")

print("\n[3/3] Copying Adafruit hashlib files\n")
for filee in listdir("../other/adafruit_hashlib"):
    print(f"-> {filee}")
    system(f"cp ../other/adafruit_hashlib/{filee} {picop}/lib/adafruit_hashlib/")

system("sync")
print()
del ami, picop, mpyn
