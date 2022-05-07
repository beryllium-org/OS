try:
    xi = ljinux.based.fn.adv_input(ljinux.based.user_vars["argj"].split()[2], int)
    yi = ljinux.based.fn.adv_input(ljinux.based.user_vars["argj"].split()[3], int)
    xe = ljinux.based.fn.adv_input(ljinux.based.user_vars["argj"].split()[4], int)
    ye = ljinux.based.fn.adv_input(ljinux.based.user_vars["argj"].split()[5], int)
    xz = ljinux.based.fn.adv_input(ljinux.based.user_vars["argj"].split()[6], int)
    yz = ljinux.based.fn.adv_input(ljinux.based.user_vars["argj"].split()[7], int)
    col = ljinux.based.fn.adv_input(ljinux.based.user_vars["argj"].split()[8], int)
    modd = ljinux.based.fn.adv_input(ljinux.based.user_vars["argj"].split()[9], str)
    ljinux.farland.public = [xi, yi, xe, ye, col]
    ljinux.based.command.fpexecc(
        [None, "-n", "/LjinuxRoot/bin/display_f/line.py"]
    )
    ljinux.farland.public = [xi, yi, xz, yz, col]
    ljinux.based.command.fpexecc(
        [None, "-n", "/LjinuxRoot/bin/display_f/line.py"]
    )
    ljinux.farland.public = [xz, yz, xe, ye, col]
    ljinux.based.command.fpexecc(
        [None, "-n", "/LjinuxRoot/bin/display_f/line.py"]
    )
    if modd == "fill":
        templ = ljinux.farland.virt_line(xi, yi, xe, ye)
        for i in templ:
            ljinux.farland.public = [xz, yz, i[0], i[1], col]
            ljinux.based.command.fpexecc(
                [None, "-n", "/LjinuxRoot/bin/display_f/ext_line.py"]
            )
    del xi, yi, xe, ye, xz, yz, col, modd
except (IndexError, ValueError):
    ljinux.based.error(9)
