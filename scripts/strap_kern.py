from os import system, listdir, path, getcwd, environ, chdir
from sys import path as spath

spath.append("../scripts/CircuitMPY/")
spath.append("../other/cptoml/")
import circuitmpy


if "FSNAME" not in environ:
    environ["FSNAME"] = "BERYLLIUM"
[boardpath, board, version] = circuitmpy.detect_board()

if boardpath == None:
    print(
        "Error: Board not found.\nMake sure it is attached and mounted before you run make"
    )
    exit(1)

olddir = getcwd()
print("[-/-] Strapping core packages..")
chdir("../scripts/jpkgstrap/")
target_root = boardpath + "/Beryllium"
if target_root.startswith("build"):
    target_root = "../../source/" + target_root
target_root = path.abspath(target_root)
cmd = "python3 jpkgstrap.py " + target_root + " -U"
for i in ["cptoml", "jcurses", "jz", "kernel", "manual"]:
    cmd += " ../../source/core_packages/" + i + ".jpk"
system(cmd)

chdir(olddir)
system("sync")
