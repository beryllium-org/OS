from os import system, mkdir, listdir, environ
from sys import argv
from sys import path as spath

spath.append("../scripts/CircuitMPY/")
spath.append("../other/cptoml/")
import circuitmpy
from cptoml import fetch


def errexit():
    print("Compilation error, exiting")
    exit(1)


optimis = 3
try:
    if argv[1] == "debug":
        print("Alert: Compiling with debug enabled.")
        optimis = 0
except IndexError:
    pass

if "FSNAME" not in environ:
    environ["FSNAME"] = "BERYLLIUM"
[boardpath, board, version] = circuitmpy.detect_board()

if boardpath == None:
    print(
        "Error: Board not found.\nMake sure it is attached and mounted before you run make"
    )
    exit(1)

print(f"Using board path: {boardpath}")
print(f"Building for board: {board}\n")

if system(f"test -d {boardpath}/lib") != 0:
    mkdir(f"{boardpath}/lib")
if system(f"test -d {boardpath}/lib/drivers") != 0:
    mkdir(f"{boardpath}/lib/drivers")

print("[1/6] Compiling source files")
for filee in listdir():
    if filee.endswith(".py"):
        try:
            circuitmpy.compile_mpy(
                f"./{filee}",
                f"{boardpath}/lib/{filee[:-3]}.mpy",
                optim=optimis,
            )
        except OSError:
            errexit()

print("[2/6] Compiling jcurses")
for filee in listdir("jcurses"):
    if filee.endswith(".py"):
        try:
            circuitmpy.compile_mpy(
                f"./jcurses/{filee}",
                f"{boardpath}/lib/{filee[:-3]}.mpy",
                optim=optimis,
            )
        except OSError:
            errexit()

print("[3/6] Copying base files")
for filee in listdir("../rootfilesystem/"):
    system(f"cp ../rootfilesystem/{filee} {boardpath}/")

print("[4/6] Copying board configuration files")
skiptm = False
try:
    if fetch("setup", "BERYLLIUM", toml=f"{boardpath}/settings.toml"):
        skiptm = True
except:
    pass
if not skiptm:
    system(f"cp ../Boardfiles/{board}/settings.toml {boardpath}/settings.toml")
else:
    print(" - Skipped updating toml as setup variable already True")

print("[5/6] Compiling jz")
try:
    circuitmpy.compile_mpy("./jz/jz.py", f"{boardpath}/lib/jz.mpy", optim=optimis)
except OSError:
    errexit()

print("[6/6] Compiling cptoml")
try:
    circuitmpy.compile_mpy(
        "../other/cptoml/cptoml.py", f"{boardpath}/lib/cptoml.mpy", optim=optimis
    )
except OSError:
    errexit()

system("sync")
