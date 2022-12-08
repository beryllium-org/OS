from os import system, mkdir, listdir, path, popen
from platform import uname
from getpass import getuser
from sys import path as spath

spath.append("../scripts/CircuitMPY/")
import circuitmpy

[boardpath, board, version] = circuitmpy.detect_board()

if boardpath == "":
    print(
        "Error: Board not found.\nMake sure it is attached and mounted before you run make"
    )
    exit(1)

if uname().system == "Linux":
    if system(f"test -d {boardpath}/LjinuxRoot") != 0:
        print("Created LjinuxRoot")
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
else:
    system(f"xcopy /y/s ..\\LjinuxRoot\\* {boardpath}\\LjinuxRoot\\")
    system(f"xcopy /y/s/d ..\\LjinuxRoot\\boot\\* {boardpath}\\LjinuxRoot\\boot\\")
    system(f"copy ..\\Manual.txt {boardpath}\\LjinuxRoot\\home\\board\\")
system("sync")
