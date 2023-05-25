from os import system, mkdir
from sys import path as spath

spath.append("../scripts/CircuitMPY/")
import circuitmpy

[boardpath, board, version] = circuitmpy.detect_board()

if boardpath == "":
    print(
        "Error: Board not found.\nMake sure it is attached and mounted before you run make"
    )
    exit(1)

if system(f"test -d {boardpath}/LjinuxRoot") != 0:
    mkdir(f"{boardpath}/LjinuxRoot")

print("[1/3] Updating /LjinuxRoot")
system(f"rsync -r --update ../LjinuxRoot/* {boardpath}/LjinuxRoot/")
print("[2/3] Installing board pinout map.")
system(
    f"rsync --update ../Boardfiles/{board}/pinout.map {boardpath}/LjinuxRoot/bin/pinout.map"
)
print("[3/3] Updating boot configuration")
if system(f"test -d {boardpath}/LjinuxRoot/boot") != 0:
    mkdir(f"{boardpath}/LjinuxRoot/boot")
system(f"rsync -r --update ../bootcfg/* {boardpath}/LjinuxRoot/boot/")
system("sync")
