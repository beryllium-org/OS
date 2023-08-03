rename_process("python")
from traceback import format_exception

term.trigger_dict = {  # Will automatically be reverted.
    "ctrlD": 1,
    "ctrlC": 2,
    "enter": 0,
    "tab": 3,
    "overflow": 0,
    "rest": "stack",
    "rest_a": "common",
    "echo": "common",
    "prefix": ">>> ",
}
term.buf[1] = ""

pv[get_pid()]["currdep"] = 0
pv[get_pid()]["mass"] = []
dmtex("Staring Python shell")
term.write(
    "CircuitPython "
    + ljinux.based.system_vars["IMPLEMENTATION"]
    + " on ljinux "
    + ljinux.based.system_vars["VERSION"]
    + "\n"
    + "Board: "
    + board.board_id
    + "\n"
    + 'Type "help", "copyright", "credits" or "license" for more information.'
)
while True:
    term.clear_line()
    term.focus = 0
    ljinux.io.ledset(1)
    try:
        term.program()
    except KeyboardInterrupt:
        term.buf[0] = 2
    ljinux.io.ledset(3)
    if term.buf[0] == 1:
        term.write("^D")
        term.buf[1] = ""
        term.focus = 0
        break
    elif term.buf[0] == 3:
        try:
            if term.focus is 0 and term.buf[1].endswith("."):
                exec(
                    'pv[get_pid()]["ljdirtest"] = dir({})'.format(
                        term.buf[1][: term.buf[1].rfind(".")]
                    )
                )
                if len(pv[get_pid()]["ljdirtest"]):
                    term.write()
                    for pv[get_pid()]["i"] in pv[get_pid()]["ljdirtest"]:
                        if not pv[get_pid()]["i"].startswith("_"):
                            term.nwrite(pv[get_pid()]["i"] + "    ")
                    term.write()
            else:
                raise Exception
        except:
            term.buf[1] += "    "
    elif term.buf[0] == 0:
        term.write()
        if term.buf[1].startswith(" "):
            if term.buf[1].isspace():
                term.trigger_dict["prefix"] = ">>> "
                pv[get_pid()]["currdep"] = 0
                term.buf[1] = ""
                term.focus = 0
                pv[get_pid()]["execstr"] = ""
                for pv[get_pid()]["i"] in pv[get_pid()]["mass"]:
                    pv[get_pid()]["execstr"] += pv[get_pid()]["i"] + "\n"
                pv[get_pid()]["mass"].clear()
                try:
                    try:
                        exec(pv[get_pid()]["execstr"])
                    except Exception as Err:
                        term.write(format_exception(Err)[0])
                except KeyboardInterrupt as Err:
                    term.write("KeyboardInterrupt")
                    term.buf[1] = ""
                    pv[get_pid()]["mass"].clear()
                    term.focus = 0

            else:
                pv[get_pid()]["mass"].append(term.buf[1])
                pv[get_pid()]["currdep"] = term.buf[1].count(" ")
                while True:
                    if not term.buf[1][pv[get_pid()]["currdep"] - 1 :][0] == " ":
                        pv[get_pid()]["currdep"] -= 1
                    else:
                        break
                term.buf[1] = " " * pv[get_pid()]["currdep"]
                term.trigger_dict["prefix"] = "... "
                term.focus = 0
                pv[get_pid()]["i"] = 1

        elif term.buf[1] == "":
            term.trigger_dict["prefix"] = ">>> "
            if pv[get_pid()]["currdep"] > 0:
                pv[get_pid()]["currdep"] = 0
                pv[get_pid()]["execstr"] = ""
                for pv[get_pid()]["i"] in pv[get_pid()]["mass"]:
                    pv[get_pid()]["execstr"] += pv[get_pid()]["i"] + "\n"
                pv[get_pid()]["mass"].clear()
                try:
                    try:
                        exec(pv[get_pid()]["execstr"])
                    except Exception as Err:
                        term.write(format_exception(Err)[0])
                except KeyboardInterrupt as Err:
                    term.write("KeyboardInterrupt")
                    term.buf[1] = ""
                    pv[get_pid()]["mass"].clear()
                    term.focus = 0

        elif term.buf[1].startswith("exit"):
            try:
                if term.buf[1][4] == "(":
                    pv[get_pid()]["cod"] = term.buf[1][
                        term.buf[1].find("(") + 1 : term.buf[1].find(")")
                    ]
                    ljinux.api.setvar(
                        "return",
                        pv[get_pid()]["cod"] if len(pv[get_pid()]["cod"]) > 0 else "0",
                    )
                    term.buf[1] = ""
                    term.focus = 0
                    break
                else:
                    raise IndexError
            except IndexError:
                term.buf[1] = ""
                term.focus = 0
                term.write("Use exit() or Ctrl-D (i.e. EOF) to exit")

        elif term.buf[1].endswith(":"):
            pv[get_pid()]["currdep"] += 4
            pv[get_pid()]["mass"].append(term.buf[1])
            term.trigger_dict["prefix"] = "... "
            term.buf[1] = " " * pv[get_pid()]["currdep"]
            term.focus = 0

        else:
            pv[get_pid()]["cppy"] = None
            pv[get_pid()]["pyeqpos1"] = term.buf[1].find("=")
            pv[get_pid()]["pyeqpos2"] = term.buf[1].find("==")
            pv[get_pid()]["pyskippri"] = False
            if (
                (
                    (pv[get_pid()]["pyeqpos1"] is not -1)
                    and (pv[get_pid()]["pyeqpos1"] is not pv[get_pid()]["pyeqpos2"])
                )
                or (term.buf[1][:7] == "import ")
                or (term.buf[1][:4] in ["del ", "for ", "from"])
                or (term.buf[1][:3] == "if ")
                or (term.buf[1][:6] == "raise ")
            ):
                pv[get_pid()]["pyskippri"] = True
            try:
                try:
                    if not pv[get_pid()]["pyskippri"]:
                        exec('pv[get_pid()]["cppy"]=' + term.buf[1])
                    else:
                        exec(term.buf[1])
                    if pv[get_pid()]["cppy"] is not None:
                        term.write(str(pv[get_pid()]["cppy"]))
                except Exception as Err:
                    term.write(format_exception(Err)[0])
            except KeyboardInterrupt as Err:
                term.write("KeyboardInterrupt")
                term.buf[1] = ""
                pv[get_pid()]["mass"].clear()
                term.focus = 0
            term.buf[1] = ""
            term.focus = 0
    elif term.buf[0] == 2:
        term.write("\nKeyboardInterrupt")
        term.buf[1] = ""
        pv[get_pid()]["mass"].clear()
        term.focus = 0
dmtex("Python shell session has ended")
ljinux.api.setvar("return", "0")
del format_exception
