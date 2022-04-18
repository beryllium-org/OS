lines = 10
offs = 0
try:
    if ljinux.based.user_vars["argj"].split()[1][0] == "-":
        ops = ljinux.based.fn.get_valid_options(
            ljinux.based.user_vars["argj"].split()[1], "n"
        )
        offs += 1
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
        with open(ljinux.based.fn.betterpath(filee), "r") as f:
            content = f.readlines()
            count = len(content)
            min(lines, count)
            start = (
                0
                if ljinux.based.user_vars["argj"].split()[0].endswith("head.lja")
                else count - lines
            )
            end = (
                lines
                if ljinux.based.user_vars["argj"].split()[0].endswith("head.lja")
                else count
            )
            for item in content[start : end - 1]:
                print(item, end="")
            print(content[-1])
            del content, count, start, end, filee
            ljinux.based.user_vars["return"] = "0"
    except OSError:
        ljinux.based.error(4, filee)
        ljinux.based.user_vars["return"] = "1"
except IndexError:
    ljinux.based.error(9)
    ljinux.based.user_vars["return"] = "1"
del lines, offs
