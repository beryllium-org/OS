from os import system, mkdir, listdir, path, popen, getcwd
from platform import uname
from getpass import getuser
from sys import argv
from sys import path as spath

spath.append("../scripts/CircuitMPY/")
import circuitmpy


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

if uname().system == "Linux":
    slash = "/"
    copy = "rsync -h"
else:
    slash = "\\"
    copy = "copy"

[boardpath, board, version] = circuitmpy.detect_board()

if board == "":
    print(
        "Error: Board not found.\nMake sure it is attached and mounted before you run make"
    )
    exit(1)

print(f"Using board path: {boardpath}")
print(f"Building for board: {board}\n")

if system(f"test -d {boardpath}/lib".replace("/", slash)) != 0:
    mkdir(f"{boardpath}/lib".replace("/", slash))
if system(f"test -d {boardpath}/lib/drivers".replace("/", slash)) != 0:
    mkdir(f"{boardpath}/lib/drivers".replace("/", slash))

print("[1/5] Compiling source files")
for filee in listdir():
    if filee.endswith(".py"):
        try:
            circuitmpy.compile_mpy(
                f"./{filee}", f"{boardpath}/lib/{filee[:-3]}.mpy", optim=optimis
            )
        except OSError:
            errexit()

print("[2/5] Compiling jcurses")
for filee in listdir("jcurses"):
    if filee.endswith(".py"):
        try:
            circuitmpy.compile_mpy(
                f"./jcurses/{filee}", f"{boardpath}/lib/{filee[:-3]}.mpy", optim=optimis
            )
        except OSError:
            errexit()

print("[3/5] Copying base files")
for filee in listdir("../rootfilesystem/".replace("/", slash)):
    system(
        f"cp ../rootfilesystem/{filee} {boardpath}/".replace("/", slash).replace(
            "cp", copy
        )
    )

print("[4/5] Copying board configuration files")
system(
    f"cp ../Boardfiles/{board}/config.json {boardpath}/".replace("/", slash).replace(
        "cp", copy
    )
)
try:
    circuitmpy.compile_mpy(
        f"../Boardfiles/{board}/pintab.py", f"{boardpath}/lib/pintab.mpy", optim=optimis
    )
except OSError:
    errexit()

print("[5/5] Compiling jz")
try:
    circuitmpy.compile_mpy(f"./jz/jz.py", f"{boardpath}/lib/jz.mpy", optim=optimis)
except OSError:
    errexit()

system("sync")
