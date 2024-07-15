rename_process("python")

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
    "idle": 4,
}
term.buf[1] = ""

vr("currdep", 0)
vr("mass", [])
dmtex("Staring Python shell")
term.write(
    "CircuitPython "
    + be.based.system_vars["IMPLEMENTATION"]
    + " on Beryllium "
    + be.based.system_vars["VERSION"]
    + "\n"
    + "Board: "
    + be.based.system_vars["BOARD"]
    + "\n"
    + 'Type "help", "copyright", "credits" or "license" for more information.'
)
while True:
    term.clear_line()
    term.focus = 0
    be.io.ledset(1)
    try:
        term.program()
    except KeyboardInterrupt:
        term.buf[0] = 2
    be.io.ledset(3)
    if term.buf[0] == 1:
        term.write("^D")
        term.buf[1] = ""
        term.focus = 0
        break
    elif term.buf[0] == 3:
        try:
            if term.focus is 0 and term.buf[1].endswith("."):
                exec(
                    'vr("ljdirtest", dir({}))'.format(
                        term.buf[1][: term.buf[1].rfind(".")]
                    )
                )
                if len(vr("ljdirtest")):
                    term.write()
                    for pv[get_pid()]["i"] in vr("ljdirtest"):
                        if not vr("i").startswith("_"):
                            term.nwrite(vr("i") + "    ")
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
                vr("currdep", 0)
                term.buf[1] = ""
                term.focus = 0
                vr("execstr", "")
                for pv[get_pid()]["i"] in vr("mass"):
                    vrp("execstr", vr("i") + "\n")
                pv[get_pid()]["mass"].clear()
                try:
                    try:
                        exec(vr("execstr"))
                    except Exception as Err:
                        term.write(format_exception(Err)[0])
                except KeyboardInterrupt as Err:
                    term.write("KeyboardInterrupt")
                    term.buf[1] = ""
                    pv[get_pid()]["mass"].clear()
                    term.focus = 0

            else:
                vra("mass", term.buf[1])
                vr("currdep", term.buf[1].count(" "))
                while True:
                    if not term.buf[1][vr("currdep") - 1 :][0] == " ":
                        vrm("currdep")  # currdep--
                    else:
                        break
                term.buf[1] = " " * vr("currdep")
                term.trigger_dict["prefix"] = "... "
                term.focus = 0
                vr("i", 1)

        elif term.buf[1] == "":
            term.trigger_dict["prefix"] = ">>> "
            if vr("currdep") > 0:
                vr("currdep", 0)
                vr("execstr", "")
                for pv[get_pid()]["i"] in vr("mass"):
                    vrp("execstr", vr("i") + "\n")
                pv[get_pid()]["mass"].clear()
                try:
                    try:
                        exec(vr("execstr"))
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
                    vr(
                        "cod",
                        term.buf[1][term.buf[1].find("(") + 1 : term.buf[1].find(")")],
                    )
                    be.api.setvar(
                        "return",
                        vr("cod") if len(vr("cod")) > 0 else "0",
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
            vrp("currdep", 4)
            vra("mass", term.buf[1])
            term.trigger_dict["prefix"] = "... "
            term.buf[1] = " " * vr("currdep")
            term.focus = 0

        else:
            vr("cppy", None)
            vr("pyeqpos1", term.buf[1].find("="))
            vr("pyeqpos2", term.buf[1].find("=="))
            vr("pyskippri", False)
            if (
                ((vr("pyeqpos1") is not -1) and (vr("pyeqpos1") is not vr("pyeqpos2")))
                or (term.buf[1][:7] == "import ")
                or (term.buf[1][:4] in ["del ", "for ", "from"])
                or (term.buf[1][:3] == "if ")
                or (term.buf[1][:6] == "raise ")
            ):
                vr("pyskippri", True)
            try:
                try:
                    if not vr("pyskippri"):
                        exec(f'vr("cppy", {term.buf[1]})')
                    else:
                        exec(term.buf[1])
                    if vr("cppy") is not None:
                        term.write(str(vr("cppy")))
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
    elif term.buf[0] == 4:
        term.buf[1] = ""
        term.focus = 0
        break

dmtex("Python shell session has ended")
be.api.setvar("return", "0")
