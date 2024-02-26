from os import system, mkdir, environ
from sys import path as spath

spath.append("../scripts/CircuitMPY/")
import circuitmpy

if "FSNAME" not in environ:
    environ["FSNAME"] = "BERYLLIUM"
[boardpath, board, version] = circuitmpy.detect_board()

if boardpath == "":
    print(
        "Error: Board not found.\nMake sure it is attached and mounted before you run make"
    )
    exit(1)

if system(f"test -d {boardpath}/Beryllium") != 0:
    mkdir(f"{boardpath}/Beryllium")

print("[1/2] Updating /Beryllium")
system(f"rsync -r --update ../Beryllium/* {boardpath}/Beryllium/")
print("[2/2] Installing board pinout map.")
system(
    f"rsync --update ../Boardfiles/{board}/pinout.map {boardpath}/Beryllium/bin/pinout.map"
)
system("sync")
