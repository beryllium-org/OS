from os import system, mkdir, listdir, path, popen
from platform import uname
from getpass import getuser
from sys import argv
from detect_board import detect_board


def errexit():
    print("Compilation error, exiting")
    exit(1)


if uname().system == "Linux":
    slash = "/"
    copy = "cp"
else:
    slash = "\\"
    copy = "copy"
mpyn = f"../scripts/mpy-cross-{uname().machine}-8"

[picop, board, version] = detect_board()

if board == "":
    print(
        "Error: Board not found.\nMake sure it is attached and mounted before you run make"
    )
    exit(1)
else:
    try:
        with open(f"../Boardfiles/{board}/needs_fake_cdc".replace("/", slash), "r"):
            print("This board needs fake-cdc\n\n[1/1] Compiling fake_cdc\n-> usb_cdc")
            a = system(
                f"{mpyn} ../other/fakecdc/usb_cdc.py -s usb_cdc -v -O4 -o {picop}/lib/usb_cdc.mpy".replace(
                    "/", slash
                )
            )
            if a != 0:
                errexit()
    except OSError:
        pass

system("sync")
