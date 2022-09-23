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
    system(f"cp -rv ../LjinuxRoot/* {picop}/LjinuxRoot/")
    system(f"cp -v ../Manual.txt {picop}/LjinuxRoot/home/board/")
    system(f"cp -v ../Boardfiles/{board}/pinout.map {picop}/LjinuxRoot/bin/pinout.map")
else:
    system(f"xcopy /y/s ..\\LjinuxRoot\\* {picop}\\LjinuxRoot\\")
    system(f"copy ..\\Manual.txt {picop}\\LjinuxRoot\\home\\board\\")
