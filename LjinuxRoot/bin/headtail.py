lines = 10
try:
    if ljinux.based.user_vars["argj"].split()[1][0] == "-":
        ops = ljinux.based.fn.get_valid_options(ljinux.based.user_vars["argj"].split()[1], "n")
        if "n" in ops and len(ljinux.based.user_vars["argj"].split()) == 4:
            try:
                lines = int(ljinux.based.user_vars["argj"].split()[2])
                filee = ljinux.based.user_vars["argj"].split()[3]
            except IndexError:
                ljinux.based.error(9)
                ljinux.based.user_vars["return"] = "1"
            except ValueError:
                ljinux.based.error(1)
                ljinux.based.user_vars["return"] = "1"
        else:
            ljinux.based.error(1)
            ljinux.based.user_vars["return"] = "1"
        del ops
    elif len(ljinux.based.user_vars["argj"].split()) == 2:
        filee = ljinux.based.user_vars["argj"].split()[1]
    else:
        ljinux.based.error(1)
        ljinux.based.user_vars["return"] = "1"
    try:
        with open(filee, "r") as f:
            content = f.readlines()
            count = len(content)
            if lines > count:
                lines = count
            if type == "head":
                start = 0
                end = lines
            elif type == "tail":
                start = count - lines
                end = count
            for i in range(start, end):
                if i < count - 1:
                    print(content[i], end="")
                else:
                    print(content[i])
            f.close()
            del content
            del count
            del start
            del end
            del filee
            ljinux.based.user_vars["return"] = "0"
    except OSError:
        ljinux.based.error(4, filee)
        ljinux.based.user_vars["return"] = "1"
except IndexError:
    ljinux.based.error(9)
    ljinux.based.user_vars["return"] = "1"
del lines
