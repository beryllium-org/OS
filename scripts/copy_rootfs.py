from os import system, mkdir, environ
from sys import path as spath

spath.append("../scripts/CircuitMPY/")
import circuitmpy

if "FSNAME" not in environ:
    environ["FSNAME"] = "LJINUX"
[boardpath, board, version] = circuitmpy.detect_board()

if boardpath == "":
    print(
        "Error: Board not found.\nMake sure it is attached and mounted before you run make"
    )
    exit(1)

if system(f"test -d {boardpath}/LjinuxRoot") != 0:
    mkdir(f"{boardpath}/LjinuxRoot")

print("[1/2] Updating /LjinuxRoot")
system(f"rsync -r --update ../LjinuxRoot/* {boardpath}/LjinuxRoot/")
print("[2/2] Installing board pinout map.")
system(
    f"rsync --update ../Boardfiles/{board}/pinout.map {boardpath}/LjinuxRoot/bin/pinout.map"
)
system("sync")
