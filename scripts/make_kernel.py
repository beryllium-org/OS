from os import system, mkdir, listdir, environ, getcwd, chdir, remove
from sys import argv
from sys import path as spath
import shutil

spath.append("../scripts/CircuitMPY/")
spath.append("./jz")
import circuitmpy
from jz import compress


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

print(f"Using board path: {boardpath}")
print(f"Building for board: {board}\n")

print("[1/5] Building kernel package")

kern_files = ["be.py", "lj_colours.py", "lj_colours_placebo.py", "neopixel_colors.py"]
jcurses_files = ["jcurses.py", "jcurses_data.py"]

for filee in kern_files:
    try:
        circuitmpy.compile_mpy(
            f"./{filee}",
            f"./core_packages/kernel/{filee[:-3]}.mpy",
            optim=optimis,
        )
    except OSError:
        errexit()

olddir = getcwd()
chdir("core_packages/kernel")
execstr = ""
for filee in listdir():
    execstr += f", '{filee}'"
execstr = "compress(" + execstr[2:] + ", '../kernel.jpk')"
exec(execstr)
chdir(olddir)

for filee in kern_files:
    remove(f"./core_packages/kernel/{filee[:-3]}.mpy")
print("Done")

print("\n[2/5] Building jcurses package")
for filee in jcurses_files:
    try:
        circuitmpy.compile_mpy(
            f"./jcurses/{filee}",
            f"./core_packages/jcurses/{filee[:-3]}.mpy",
            optim=optimis,
        )
    except OSError:
        errexit()

chdir("core_packages/jcurses")
execstr = ""
for filee in listdir():
    execstr += f", '{filee}'"
execstr = "compress(" + execstr[2:] + ", '../jcurses.jpk')"
exec(execstr)
chdir(olddir)

for filee in jcurses_files:
    remove(f"./core_packages/jcurses/{filee[:-3]}.mpy")
print("Done")

print("\n[3/5] Building jz package")
try:
    circuitmpy.compile_mpy("./jz/jz.py", f"./core_packages/jz/jz.mpy", optim=optimis)
except OSError:
    errexit()
print("Done")

chdir("core_packages/jz")
execstr = ""
for filee in listdir():
    execstr += f", '{filee}'"
execstr = "compress(" + execstr[2:] + ", '../jz.jpk')"
exec(execstr)
chdir(olddir)

remove(f"./core_packages/jz/jz.mpy")
print("Done")

print("\n[4/5] Building cptoml package")
try:
    circuitmpy.compile_mpy(
        "../source/cptoml/cptoml.py",
        f"./core_packages/cptoml/cptoml.mpy",
        optim=optimis,
    )
except OSError:
    errexit()

chdir("core_packages/cptoml")
execstr = ""
for filee in listdir():
    execstr += f", '{filee}'"
execstr = "compress(" + execstr[2:] + ", '../cptoml.jpk')"
exec(execstr)
chdir(olddir)
remove(f"./core_packages/cptoml/cptoml.mpy")

print("\n[5/5] Creating manual package")
shutil.copyfile(
    "../Manual.txt",
    "core_packages/manual/Manual.txt",
)
chdir("core_packages/manual")
execstr = ""
for filee in listdir():
    execstr += f", '{filee}'"
execstr = "compress(" + execstr[2:] + ", '../manual.jpk')"
exec(execstr)
chdir(olddir)

print("Done")
