term_old = term.trigger_dict
term.trigger_dict = {
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

currdep = 0
mass = []
dmtex("Staring Python shell")
print(
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
        print("^D")
        term.buf[1] = ""
        term.focus = 0
        break
    elif term.buf[0] == 3:
        try:
            if term.focus is 0 and term.buf[1].endswith("."):
                exec(
                    "ljdirtest = dir({})".format(term.buf[1][: term.buf[1].rfind(".")])
                )
                if len(ljdirtest):
                    stdout.write("\n")
                    for i in ljdirtest:
                        if not i.startswith("_"):
                            stdout.write(i + "    ")
                        del i
                    stdout.write("\n")
                del ljdirtest
            else:
                raise Exception
        except:
            term.buf[1] += "    "
    elif term.buf[0] == 0:
        print()
        if term.buf[1].startswith(" "):
            if term.buf[1].isspace():
                term.trigger_dict["prefix"] = ">>> "
                currdep = 0
                term.buf[1] = ""
                term.focus = 0
                execstr = ""
                for i in mass:
                    execstr += i + "\n"
                mass.clear()
                try:
                    exec(execstr)
                except Exception as Err:
                    print(str(Err))
                del execstr
            else:
                mass.append(term.buf[1])
                currdep = term.buf[1].count(" ")
                while True:
                    if not term.buf[1][currdep - 1 :][0] == " ":
                        currdep -= 1
                    else:
                        break
                term.buf[1] = " " * currdep
                term.trigger_dict["prefix"] = "... "
                term.focus = 0
                i = 1

        elif term.buf[1] == "":
            term.trigger_dict["prefix"] = ">>> "
            if currdep > 0:
                currdep = 0
                execstr = ""
                for i in mass:
                    execstr += i + "\n"
                mass.clear()
                try:
                    exec(execstr)
                except Exception as Err:
                    print(str(Err))
                del execstr

        elif term.buf[1].startswith("exit"):
            try:
                if term.buf[1][4] == "(":
                    cod = term.buf[1][term.buf[1].find("(") + 1 : term.buf[1].find(")")]
                    ljinux.based.user_vars["return"] = cod if len(cod) > 0 else "0"
                    del cod
                    term.buf[1] = ""
                    term.focus = 0
                    break
                else:
                    raise IndexError
            except IndexError:
                term.buf[1] = ""
                term.focus = 0
                print("Use exit() or Ctrl-D (i.e. EOF) to exit")

        elif term.buf[1].endswith(":"):
            currdep += 4
            mass.append(term.buf[1])
            term.trigger_dict["prefix"] = "... "
            term.buf[1] = " " * currdep
            term.focus = 0

        else:
            try:
                cppy = None
                pyeqpos1 = term.buf[1].find("=")
                pyeqpos2 = term.buf[1].find("==")
                pyskippri = False
                if (
                    ((pyeqpos1 is not -1) and (pyeqpos1 is not pyeqpos2))
                    or (term.buf[1][:7] == "import ")
                    or (term.buf[1][:4] in ["del ", "for ", "from"])
                    or (term.buf[1][:3] == "if ")
                    or (term.buf[1][:6] == "raise ")
                ):
                    pyskippri = True
                del pyeqpos1, pyeqpos2
                if not pyskippri:
                    exec("cppy=" + term.buf[1])
                else:
                    exec(term.buf[1])
                del pyskippri
                if cppy is not None:
                    print(str(cppy))
                del cppy
            except Exception as Err:
                print(str(Err))
            term.buf[1] = ""
            term.focus = 0
    elif term.buf[0] == 2:
        print("\nKeyboardInterrupt")
        term.buf[1] = ""
        mass.clear()
        term.focus = 0
dmtex("Python shell session has ended")
term.trigger_dict = term_old
del term_old, mass, currdep
ljinux.based.user_vars["return"] = "0"
