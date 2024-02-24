from os import system, mkdir, listdir, environ
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

print("[1/1] Updating /LjinuxRoot/boot/boot.d")
if system(f"test -d {boardpath}/LjinuxRoot/boot") != 0:
    mkdir(boardpath + "/LjinuxRoot/boot")
if system(f"test -d {boardpath}/LjinuxRoot/boot/boot.d") != 0:
    mkdir(boardpath + "/LjinuxRoot/boot/boot.d")
with open(f"../Boardfiles/{board}/boot.txt") as f:
    lines = f.readlines()
    btls = listdir(boardpath + "/LjinuxRoot/boot/boot.d")
    for i in lines:
        i = i[:-1]
        if i not in btls:
            print(f"[-/-] Loading boot.d/{i}")
            system(f"cp ../bootcfg/boot.d/{i} {boardpath}/LjinuxRoot/boot/boot.d/")
if "Init.lja" not in listdir(boardpath + "/LjinuxRoot/boot"):
    print("[-/-] Generating Init.lja")
    system(f"cp ../bootcfg/Init.lja {boardpath}/LjinuxRoot/boot/Init.lja")
system("sync")
