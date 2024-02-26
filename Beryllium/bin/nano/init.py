vr("filee", None)
vr("exists", 2)
vr("weltxt", "[ Welcome to nano.  For basic help, type Ctrl+G. ]")

vr("versionn", "1.9.1")

try:
    vr("filee", be.based.user_vars["argj"].split()[1])
except IndexError:
    pass

if vr("filee") is not None:  # there is arg
    vr("exists", be.api.isdir(vr("filee")))

if vr("exists") == 1:  # it is dir
    vr(
        "weltxt",
        "[ {} is a directory ]".format(vr("filee")[vr("filee").rfind("/") + 1 :]),
    )
    vr("filee", None)
    vr("exists", 2)

vr("dataa", [""])
vr("lc", 0)  # line count
if vr("exists") is 0:  # is file
    with be.api.fopen(vr("filee")) as pv[get_pid()]["f"]:
        vr("ll", vr("f").readlines())
        vr("lines", [])
        for pv[get_pid()]["i"] in range(0, len(vr("ll"))):
            if vr("ll")[vr("i")] != "\n":
                vra("lines", vr("ll")[vr("i")].replace("\n", ""))
            else:
                vra("lines", "")
        vrd("ll")
        # vrd("i")

    be.based.command.fpexec(pv[0]["root"] + "/bin/stringproccessing/line_wrap.py")
    vr("dataa", vr("lines"))
    vr("lc", len(vr("dataa")))
    vrd("lines")

# in case of empty file
if vr("dataa") == []:
    vr("dataa", [""])

term.trigger_dict = {
    "ctrlX": 1,
    "ctrlK": 100,
    "ctrlC": 0,
    "up": 2,
    "down": 8,
    "pgup": 4,
    "pgdw": 5,
    "bck": 11,
    "tab": 12,
    "enter": 10,
    "overflow": 10,
    "rest": "stack",
    "rest_a": "common",
    "echo": "common",
    "prefix": "",
}

vr("target", vr("sizee")[0] - 3)  # no of lines per screen
vr("cl", 0)  # current line
vr("vl", 0)  # 1st visible line
term.buf = [0, None]
if vr("exists") == 2:
    vr("fnam", "New buffer")
else:
    vr("fnam", vr("filee")[vr("filee").rfind("/") + 1 :])
vr("spz", int((vr("sizee")[1] - 11 - len(vr("versionn")) - len(vr("fnam"))) / 2))
vr("sps1", " " * (vr("spz") - 5))
vr("sps2", " " * (vr("spz") + 6))
vrd("spz")

vr(
    "toptxt",
    "{}  LNL nano {}{}{}{}{}\n".format(
        colors.inverse,
        vr("versionn"),
        vr("sps1"),
        vr("fnam"),
        vr("sps2"),
        colors.uninverse,
    ),
)
vrd("versionn")
vrd("sps1")
vrd("sps2")
vrd("fnam")

vr("bottxt", "{}{}{}\n".format(colors.inverse, vr("weltxt"), colors.uninverse))
vr("bottxt_offs", int((vr("sizee")[1] - len(vr("weltxt"))) / 2))
vrd("weltxt")

vr("toolsplit", " " * int(vr("sizee")[1] / 8 - 13 - (vr("sizee")[1] % 2)))

vr(
    "toolbar_items",
    [
        "^G",
        " Help      ",
        "^O",
        " Write Out ",
        "^W",
        " Where Is  ",
        "^K",
        " Cut       ",
        "^T",
        " Execute   ",
        "^C",
        " Location  ",
        "M-U",
        " Undo      ",
        "M-A",
        " Set Mark  ",
        "\n^X",
        " Exit      ",
        "^R",
        " Read File ",
        "^\\",
        " Replace   ",
        "^U",
        " Paste     ",
        "^J",
        " Justify   ",
        "^_",
        " Go To Line",
        "M-E",
        " Redo      ",
        "M-6",
        " Copy",
    ],
)

vr("toolbar_txt", "")

for pv[get_pid()]["i"] in range(0, len(vr("toolbar_items")), 2):
    vrp(
        "toolbar_txt",
        (
            colors.inverse
            + vr("toolbar_items")[vr("i")]
            + colors.uninverse
            + vr("toolbar_items")[vr("i") + 1]
            + vr("toolsplit")
        ),
    )
vrd("toolbar_items")
vrd("i")

vr("q", True)
vr("inb", False)  # in bottom box
vr("bmod", None)  # 0 == saving, 1 == searching, more planned later
vr("savee", 0)
term.hold_stdout = True
term.clear()
term.nwrite(vr("toptxt"))
vrd("toptxt")  # not gonna use it again
term.move(x=vr("sizee")[0] - 2, y=vr("bottxt_offs"))
term.nwrite(vr("bottxt"))
vrd("bottxt")
vrd("bottxt_offs")
term.nwrite(vr("toolbar_txt"))
if len(vr("dataa")) > 1:
    vr("sz", vr("sizee")[0] - 4)
    vr("ld", len(vr("dataa")))
    vr("ltd", vr("sz") if vr("sz") < vr("ld") else vr("ld"))
    vrd("sz")
    vrd("ld")
    for pv[get_pid()]["i"] in range(0, vr("ltd")):
        term.move(x=vr("i") + 2)
        term.nwrite(vr("dataa")[vr("i")])
    vrd("ltd")
term.hold_stdout = False
term.flush_writes()
vr("ok", True)
