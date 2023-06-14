from os import system, mkdir, listdir, path, getcwd
from sys import argv
from sys import path as spath
from shutil import copy

spath.append("../scripts/CircuitMPY/")
spath.append("../other/cptoml/")
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

[boardpath, board, version] = circuitmpy.detect_board()

if boardpath == None:
    print(
        "Error: Board not found.\nMake sure it is attached and mounted before you run make"
    )
    exit(1)

if system(f"test -d {boardpath}/lib") != 0:
    mkdir(f"{boardpath}/lib")
if system(f"test -d {boardpath}/lib/drivers") != 0:
    mkdir(f"{boardpath}/lib/drivers")

if path.exists(f"../Boardfiles/{board}/extras"):
    for i in listdir(f"../Boardfiles/{board}/extras/"):
        if i.endswith(".other"):
            source_p = "../other/" + i[:-6].replace(".", "/")
            target_p = f"{boardpath}/lib/" + source_p[source_p.rfind("/") + 1 :]
            print(f"[-/-] Compiling extras: {source_p}")
            if path.isdir(source_p):
                if not path.exists(target_p):
                    mkdir(target_p)
                for filee in listdir(source_p):
                    circuitmpy.compile_mpy(
                        f"{source_p}/{filee}",
                        f"{target_p}/{filee[:-3]}.mpy",
                        optim=optimis,
                    )
            elif path.isfile(source_p + ".py"):
                try:
                    circuitmpy.compile_mpy(
                        f"../other/{source_p}.py", f"{target_p}.mpy", optim=optimis
                    )
                except OSError:
                    errexit()
            else:
                errexit()
            del source_p, target_p
        elif i.endswith(".py"):
            print(f"[-/-] Compiling extras: extras/{i[:-2]}")
            if path.isdir(f"../Boardfiles/{board}/extras/{i}"):
                print("NOT IMPLEMENTED")
                errexit()
            elif path.isfile(f"../Boardfiles/{board}/extras/{i}"):
                try:
                    circuitmpy.compile_mpy(
                        f"../Boardfiles/{board}/extras/{i}",
                        f"{boardpath}/lib/{i[:-3]}.mpy",
                        optim=optimis,
                    )
                except OSError:
                    errexit()
            else:
                errexit()
        elif i.endswith(".driver"):
            print(f"[-/-] Compiling extras: drivers/{i[:-7]}")
            if path.isdir(f"../Boardfiles/{board}/extras/{i}"):
                print("NOT IMPLEMENTED")
                errexit()
            elif path.isfile(f"../Boardfiles/{board}/extras/{i}"):
                try:
                    circuitmpy.compile_mpy(
                        f"../other/drivers/{i[:-7]}.py",
                        f"{boardpath}/lib/drivers/{i[:-7]}.mpy",
                        optim=optimis,
                    )
                except OSError:
                    errexit()
            else:
                errexit()
        elif i.endswith(".bin"):
            print("[-/-] Copying extras: binextra/" + i[:-4])
            if path.isdir("../other/binextra/" + i[:-4]):
                source_p = f"../other/binextra/{i[:-4]}/"
                target_p = boardpath + "/LjinuxRoot/bin/"
                for j in listdir(source_p):
                    copy(source_p + j, target_p + j)
            else:
                print("Use folders instead")
                errexit()
        else:
            errexit()

system("sync")
