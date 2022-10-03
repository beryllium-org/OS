from os import system, mkdir, listdir, path, popen
from platform import uname
from getpass import getuser
from detect_board import detect_board

[picop, board] = detect_board()

if picop == "":
    print(
        "Error: Board not found.\nMake sure it is attached and mounted before you run make"
    )
    exit(1)

if uname().system == "Linux":
    if system(f"test -d {picop}/LjinuxRoot") != 0:
        print("Created LjinuxRoot")
        mkdir(f"{picop}/LjinuxRoot")
    print("[1/4] Updating /LjinuxRoot")
    system(f"rsync -r --update ../LjinuxRoot/* {picop}/LjinuxRoot/")
    print("[2/4] Installing Manual.")
    system(f"rsync --update ../Manual.txt {picop}/LjinuxRoot/home/board/")
    print("[3/4] Installing board pinout map.")
    system(
        f"rsync --update ../Boardfiles/{board}/pinout.map {picop}/LjinuxRoot/bin/pinout.map"
    )
    print("[4/4] Updating boot configuration")
    if system(f"test -d {picop}/LjinuxRoot/boot") != 0:
        print("      Created boot folder.")
        mkdir(f"{picop}/LjinuxRoot/boot")
    system(f"rsync -r --update ../bootcfg/* {picop}/LjinuxRoot/boot/")
else:
    system(f"xcopy /y/s ..\\LjinuxRoot\\* {picop}\\LjinuxRoot\\")
    system(f"xcopy /y/s/d ..\\LjinuxRoot\\boot\\* {picop}\\LjinuxRoot\\boot\\")
    system(f"copy ..\\Manual.txt {picop}\\LjinuxRoot\\home\\board\\")
system("sync")
