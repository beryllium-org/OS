from os import system, mkdir, listdir, uname
from getpass import getuser

ami = getuser()
mpyn = f"../mpy-crosses/mpy-cross-{uname().machine}"
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

print("[1/2] Compiling source files and pin allocation tabs\n")
for filee in listdir():
    if filee.endswith(".py"):
        print(f"-> {filee[:-3]}")
        system(f"{mpyn} ./{filee} -s {filee[:-3]} -v -o {picop}/lib/{filee[:-3]}.mpy")

print("\n[2/2] Copying base files\n")
for filee in listdir("../rootfilesystem/"):
    print(f"-> {filee}")
    system(f"cp -v ../rootfilesystem/{filee} {picop}/")

system("sync")
print()
del ami, picop, mpyn
