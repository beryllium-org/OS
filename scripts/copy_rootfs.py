from os import system, mkdir, environ
from sys import path as spath

spath.append("../scripts/CircuitMPY/")
spath.append("../other/cptoml/")
import circuitmpy
from cptoml import fetch

if "FSNAME" not in environ:
    environ["FSNAME"] = "BERYLLIUM"
[boardpath, board, version] = circuitmpy.detect_board()

if boardpath == "":
    print(
        "Error: Board not found.\nMake sure it is attached and mounted before you run make"
    )
    exit(1)

print("[1/3] Updating base")
system(f"rsync -r --update ../base/* {boardpath}/")
print("[2/3] Installing board pinout map")
system(
    f"rsync --update ../Boardfiles/{board}/pinout.map {boardpath}/Beryllium/bin/pinout.map"
)
print("[3/3] Installing board config")
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

system("sync")
