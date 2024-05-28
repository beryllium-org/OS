from os import system, mkdir, environ
from os import path as ospath
from sys import path as spath

spath.append("../scripts/CircuitMPY/")
spath.append("../source/cptoml/")
import circuitmpy
from cptoml import fetch

if "FSNAME" not in environ:
    environ["FSNAME"] = "BERYLLIUM"
[boardpath, board, version] = circuitmpy.detect_board()

if boardpath is None:
    print(
        "Error: Board not found.\nMake sure it is attached and mounted before you run make"
    )
    exit(1)

if not ospath.exists(boardpath):
    mkdir(boardpath)

print("[1/4] Updating base")
system(f"rsync -r --update ../base/* {boardpath}/")
system(f"rsync ../base/*.py {boardpath}/")
print("[2/4] Installing board pinout map")
system(
    f"rsync --update ../Boardfiles/{board}/pinout.map {boardpath}/Beryllium/bin/pinout.map"
)
print("[3/4] Installing board config")
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

print("[4/4] Cleaning .gitkeep files")
try:
    system(f'find {boardpath} -type f -name ".gitkeep" -delete')
except:
    pass
system("sync")
