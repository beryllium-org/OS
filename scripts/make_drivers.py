from os import system, mkdir, listdir, path, getcwd, environ, chdir
from sys import argv
from sys import path as spath
from shutil import copytree

spath.append("../scripts/CircuitMPY/")
spath.append("../source/cptoml/")
import circuitmpy
from cptoml import fetch


def errexit():
    print("Compilation error, exiting")
    exit(1)


optimis = 3
try:
    if argv[1] == "debug":
        print("Alert: Compiling with debug enabled.")
        optimis = 0
except IndexError:
    pass

if "FSNAME" not in environ:
    environ["FSNAME"] = "BERYLLIUM"
[boardpath, board, version] = circuitmpy.detect_board()

if boardpath == None:
    print(
        "Error: Board not found.\nMake sure it is attached and mounted before you run make"
    )
    exit(1)

drivers = set()

with open(f"../Boardfiles/{board}/drivers.txt") as f:
    tmp_drivers = f.readlines()
    for i in range(len(tmp_drivers)):
        dri = tmp_drivers[i].replace("\n", "")
        if dri:
            drivers.add(dri)

if drivers:
    for i in drivers:
        print("[-/-] Building driver: " + i)
        try:
            circuitmpy.compile_mpy(
                f"../drivers/{i}.py",
                f"{boardpath}/Beryllium/lib/drivers/{i}.mpy",
                optim=optimis,
            )
        except OSError:
            errexit()

system("sync")
