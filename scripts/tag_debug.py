import subprocess
from os import environ
from sys import path as spath

spath.append("../source/cptoml/")
spath.append("../scripts/CircuitMPY/")
import circuitmpy
from cptoml import put

if "FSNAME" not in environ:
    environ["FSNAME"] = "BERYLLIUM"
[boardpath, board, version] = circuitmpy.detect_board()

if boardpath == None:
    print(
        "Error: Board not found.\nMake sure it is attached and mounted before you run make"
    )
    exit(1)


def cmd(txt):
    try:
        return subprocess.check_output(txt).strip().decode("utf-8")
    except subprocess.CalledProcessError as e:
        return None


def get_tag() -> str:
    cmd(["git", "fetch", "--tags"])
    desc = cmd(["git", "describe", "--tags"])
    desc += "-debug"
    if cmd(["git", "status", "--porcelain"]):
        desc += "-dirty"
    print(desc)
    return desc


def write_tag(tag: str):
    put("git_tag", tag, subtable="BERYLLIUM", toml=f"{boardpath}/settings.toml")


if __name__ == "__main__":
    write_tag(get_tag())
