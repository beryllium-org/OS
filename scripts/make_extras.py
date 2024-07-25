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

packages = set()

with open(f"../Boardfiles/{board}/packages.txt") as f:
    tmp_packages = f.readlines()
    for i in range(len(tmp_packages)):
        pk = tmp_packages[i].replace("\n", "")
        if pk:
            packages.add(pk)

if packages:
    olddir = getcwd()
    for i in packages:
        print("[-/-] Building package: " + i)
        chdir("../packages/" + i)
        system("make clean package")
        chdir(olddir)
    print("[-/-] Strapping packages..")
    chdir("../scripts/jpkgstrap/")
    target_root = boardpath + "/Beryllium"
    if target_root.startswith("build"):
        target_root = "../../source/" + target_root
    target_root = path.abspath(target_root)
    cmd = "python3 jpkgstrap.py " + target_root + " -U"
    for i in packages:
        cmd += " ../../packages/" + i + "/" + i + ".jpk"
    system(cmd)
    chdir(olddir)

system("sync")
