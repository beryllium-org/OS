global display_availability
if display_availability:
    typee = ljinux.based.user_vars["argj"].split()[
        1
    ]  # "text / pixel / rectangle / line / circle / triangle / fill"
    if typee == "text":  # x, y, color, text in ""
        try:
            xi = 0
            xi = ljinux.based.fn.adv_input(
                ljinux.based.user_vars["argj"].split()[2], int
            )
            yi = ljinux.based.fn.adv_input(
                ljinux.based.user_vars["argj"].split()[3], int
            )
            txt = ""  # ljinux.based.user_vars["argj"].split()[5]
            col = ljinux.based.fn.adv_input(
                ljinux.based.user_vars["argj"].split()[4], int
            )
            if (
                ljinux.based.user_vars["argj"].split()[5].startswith('"')
            ):  # let's do some string proccessing!
                countt = len(
                    ljinux.based.user_vars["argj"].split()
                )  # get the numb of args
                if countt > 6:
                    txt += (
                        str(ljinux.based.user_vars["argj"].split()[5])[1:] + " "
                    )  # get the first word, remove last char (")
                    if ljinux.based.user_vars["argj"].split()[countt - 1].endswith('"'):
                        for i in range(
                            6, countt - 1
                        ):  # make all the words one thicc string
                            txt += str(ljinux.based.user_vars["argj"].split()[i]) + " "
                        txt += str(ljinux.based.user_vars["argj"].split()[countt - 1])[
                            :-1
                        ]  # last word without last char (")
                    else:
                        ljinux.based.error(9)
                else:
                    txt += str(ljinux.based.user_vars["argj"].split()[5])[1:-1]
            else:
                ljinux.based.error(9)
            ljinux.farland.text(txt, xi, yi, col)
        except (IndexError, ValueError):
            ljinux.based.error(9)
    elif typee == "dot":  # x,y,col
        try:
            xi = ljinux.based.fn.adv_input(
                ljinux.based.user_vars["argj"].split()[2], int
            )
            yi = ljinux.based.fn.adv_input(
                ljinux.based.user_vars["argj"].split()[3], int
            )
            col = ljinux.based.fn.adv_input(
                ljinux.based.user_vars["argj"].split()[4], int
            )
            ljinux.farland.pixel(xi, yi, col)
        except (IndexError, ValueError):
            ljinux.based.error(9)
    elif (
        typee == "rectangle"
    ):  # x start, y start, x stop, y stop, color, mode (fill / border)
        try:
            xi = ljinux.based.fn.adv_input(
                ljinux.based.user_vars["argj"].split()[2], int
            )
            yi = ljinux.based.fn.adv_input(
                ljinux.based.user_vars["argj"].split()[3], int
            )
            xe = ljinux.based.fn.adv_input(
                ljinux.based.user_vars["argj"].split()[4], int
            )
            ye = ljinux.based.fn.adv_input(
                ljinux.based.user_vars["argj"].split()[5], int
            )
            col = ljinux.based.fn.adv_input(
                ljinux.based.user_vars["argj"].split()[6], int
            )
            modd = ljinux.based.fn.adv_input(
                ljinux.based.user_vars["argj"].split()[7], str
            )
            ljinux.farland.public = [xi, yi, xe, ye, col, modd]
            ljinux.based.command.fpexecc(
                [None, "-n", "/LjinuxRoot/bin/display_f/rect.py"]
            )
        except (IndexError, ValueError):
            ljinux.based.error(9)
    elif typee == "line":  # x start, y start, x stop, y stop, color
        try:
            xi = ljinux.based.fn.adv_input(
                ljinux.based.user_vars["argj"].split()[2], int
            )
            yi = ljinux.based.fn.adv_input(
                ljinux.based.user_vars["argj"].split()[3], int
            )
            xe = ljinux.based.fn.adv_input(
                ljinux.based.user_vars["argj"].split()[4], int
            )
            ye = ljinux.based.fn.adv_input(
                ljinux.based.user_vars["argj"].split()[5], int
            )
            col = ljinux.based.fn.adv_input(
                ljinux.based.user_vars["argj"].split()[6], int
            )
            ljinux.farland.public = [xi, yi, xe, ye, col]
            ljinux.based.command.fpexecc(
                [None, "-n", "/LjinuxRoot/bin/display_f/line.py"]
            )
        except (IndexError, ValueError):
            ljinux.based.error(9)
    elif (
        typee == "circle"
    ):  # x center, y center, rad, color, mode (fill/ border / template) TODO fix fill and do template
        try:
            xi = ljinux.based.fn.adv_input(
                ljinux.based.user_vars["argj"].split()[2], int
            )
            yi = ljinux.based.fn.adv_input(
                ljinux.based.user_vars["argj"].split()[3], int
            )
            radd = ljinux.based.fn.adv_input(
                ljinux.based.user_vars["argj"].split()[4], int
            )
            col = ljinux.based.fn.adv_input(
                ljinux.based.user_vars["argj"].split()[5], int
            )
            modd = ljinux.based.fn.adv_input(
                ljinux.based.user_vars["argj"].split()[6], str
            )
            a = modd != "fill"
            ljinux.farland.draw_circle(xi, yi, radd, col, a)
            del a, xi, yi, radd, col, modd
        except (IndexError, ValueError):
            ljinux.based.error(9)
    elif (
        typee == "triangle"
    ):  # x point 1, y point 1, x point 2, y point 2, x point 3, y point 3, color, mode (fill/ border)
        ljinux.based.command.fpexecc(
            [None, "-n", "/LjinuxRoot/bin/display_f/triangle_execution.py"]
        )
    elif typee == "fill":  # color
        try:
            col = ljinux.based.fn.adv_input(
                ljinux.based.user_vars["argj"].split()[2], int
            )
            ljinux.farland.fill(col)
        except (IndexError, ValueError):
            ljinux.based.error(9)
    elif typee == "rhombus":  # todo
        pass
    elif typee == "move":  # todo
        pass
    elif typee == "delete":  # todo more
        optt = ljinux.based.fn.adv_input(ljinux.based.user_vars["argj"].split()[2], int)
        if optt == "all":
            ljinux.farland.clear()
        else:
            ljinux.based.error(1)
    elif typee == "refresh":
        ljinux.farland.frame()
    else:
        ljinux.based.error(1)
    del typee
else:
    ljinux.based.error(6)
