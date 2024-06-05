from os import system, mkdir, environ, getcwd, chdir
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

try:
    mkdir(boardpath + "/Beryllium")
except FileExistsError:
    pass
try:
    mkdir(boardpath + "/Beryllium/etc")
except FileExistsError:
    pass
try:
    mkdir(boardpath + "/Beryllium/etc/jpkg")
except FileExistsError:
    pass
try:
    mkdir(boardpath + "/Beryllium/etc/jpkg/installed")
except FileExistsError:
    pass

print("\n[1/4] Strapping base")
olddir = getcwd()
chdir("../scripts/jpkgstrap/")
target_root = boardpath + "/Beryllium"
if target_root.startswith("build"):
    target_root = "../../source/" + target_root
target_root = ospath.abspath(target_root)
cmd = "python3 jpkgstrap.py " + target_root + " -U ../../source/core_packages/base.jpk"
system(cmd)

print("\n[2/4] Strapping coreutils")
cmd = (
    "python3 jpkgstrap.py "
    + target_root
    + " -U ../../source/core_packages/coreutils.jpk"
)
system(cmd)
chdir(olddir)

print("\n[3/5] Copying bootloader files")
system(f"rsync ../base/*.py {boardpath}/")

print("[4/5] Installing board pinout map")
system(
    f"rsync --update ../Boardfiles/{board}/pinout.map {boardpath}/Beryllium/bin/pinout.map"
)
print("[5/5] Installing board config")
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
