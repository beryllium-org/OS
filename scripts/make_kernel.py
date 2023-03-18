from os import system, mkdir, listdir, path, popen, getcwd
from platform import uname
from getpass import getuser
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

if uname().system == "Linux":
    slash = "/"
    copy = "rsync -h"
else:
    slash = "\\"
    copy = "copy"

[boardpath, board, version] = circuitmpy.detect_board()

if boardpath == None:
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

print("[1/7] Compiling source files")
for filee in listdir():
    if filee.endswith(".py"):
        try:
            circuitmpy.compile_mpy(
                f"./{filee}".replace("/", slash),
                f"{boardpath}/lib/{filee[:-3]}.mpy".replace("/", slash),
                optim=optimis,
            )
        except OSError:
            errexit()

print("[2/7] Compiling jcurses")
for filee in listdir("jcurses"):
    if filee.endswith(".py"):
        try:
            circuitmpy.compile_mpy(
                f"./jcurses/{filee}".replace("/", slash),
                f"{boardpath}/lib/{filee[:-3]}.mpy".replace("/", slash),
                optim=optimis,
            )
        except OSError:
            errexit()

print("[3/7] Copying base files")
for filee in listdir("../rootfilesystem/".replace("/", slash)):
    system(
        f"cp ../rootfilesystem/{filee} {boardpath}/".replace("/", slash).replace(
            "cp", copy
        )
    )

print("[4/7] Copying board configuration files")
skiptm = False
try:
    if fetch("setup", "LJINUX", toml=f"{boardpath}/settings.toml"):
        skiptm = True
except:
    pass
if not skiptm:
    system(
        f"cp ../Boardfiles/{board}/settings.toml {boardpath}/settings.toml".replace(
            "/", slash
        ).replace("cp", copy)
    )
else:
    print(" - Skipped updating toml as setup variable already True")
try:
    circuitmpy.compile_mpy(
        f"../Boardfiles/{board}/pintab.py", f"{boardpath}/lib/pintab.mpy", optim=optimis
    )
except OSError:
    errexit()

print("[5/7] Compiling jz")
try:
    circuitmpy.compile_mpy("./jz/jz.py", f"{boardpath}/lib/jz.mpy", optim=optimis)
except OSError:
    errexit()

print("[6/7] Compiling cptoml")
try:
    circuitmpy.compile_mpy(
        "../other/cptoml/cptoml.py", f"{boardpath}/lib/cptoml.mpy", optim=optimis
    )
except OSError:
    errexit()


print("[6/7] Checking for additional requirements")
if path.exists(f"../Boardfiles/{board}/needs_fake_cdc".replace("/", slash)):
    print("This board needs fake-cdc\n\n[1/1] Compiling fake_cdc\n-> usb_cdc")
    try:
        circuitmpy.compile_mpy(
            "../other/fakecdc/usb_cdc.py", f"{boardpath}/lib/usb_cdc.mpy", optim=optimis
        )
    except OSError:
        errexit()

system("sync")
