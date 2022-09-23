from os import system, mkdir, listdir, path, popen, environ
from platform import uname
from getpass import getuser


def detect_board():
    ami = getuser()
    picop = ""
    board = ""
    try:
        board = environ["no_install"]
    except KeyError:
        pass
    if board != "":
        picop = "build_" + board
        try:
            mkdir(picop)
        except:
            pass
    elif system(f"test -d /media/{ami}/LJINUX") == 0:
        picop = f"/media/{ami}/LJINUX"
    elif system(f"test -d /media/{ami}/CIRCUITPY") == 0:
        picop = f"/media/{ami}/CIRCUITPY"
    elif system(f"test -d /media/CIRCUITPY") == 0:
        picop = f"/media/CIRCUITPY"
    elif system("test -d /Volumes/LJINUX") == 0:
        picop = "/Volumes/LJINUX"
    elif system("test -d /Volumes/CIRCUITPY") == 0:
        picop = "/Volumes/CIRCUITPY"
    elif uname().system == "Windows":
        drives = [chr(x) + ":" for x in range(65, 91) if path.exists(chr(x) + ":")]
        for _ in drives:
            vol = popen("vol " + _)
            if vol.readline()[:-1].split(" ")[-1].upper() in ["CIRCUITPY", "LJINUX"]:
                picop = f"%s" % _
            vol.close()
            if picop != "":
                break
    if (not picop == "") and (not picop.startswith("build_")):
        with open(f"{picop}/boot_out.txt", "r") as boot_out:
            magic = boot_out.readlines()
            board = magic[1][9:-1]
            del magic
    return [picop, board]
