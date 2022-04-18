try:
    optss = ljinux.based.fn.get_valid_options(ljinux.based.user_vars["argj"].split()[1], "ne")
    offs = 0
    if len(optss) > 0:
        offs += 1
    if ljinux.based.user_vars["argj"].split()[1 + offs].startswith('"'):
        if ljinux.based.user_vars["argj"].split()[1 + offs].endswith('"'):
            if not ljinux.based.silent:
                print(str(ljinux.based.user_vars["argj"].split()[1 + offs])[1:-1])
            ljinux.based.user_vars["return"] = str(ljinux.based.user_vars["argj"].split()[1 + offs])[1:-1]
        else:
            countt = len(ljinux.based.user_vars["argj"].split()) - offs
            if countt > 2:
                if ljinux.based.user_vars["argj"].split()[countt - 1 + offs].endswith('"'):
                    res = str(ljinux.based.user_vars["argj"].split()[1 + offs])[1:] + " "
                    for i in range(2, countt - 1):
                        res += ljinux.based.user_vars["argj"].split()[i + offs] + " "
                    res += str(ljinux.based.user_vars["argj"].split()[countt - 1 + offs])[:-1]
                    if not ljinux.based.silent:
                        if "n" in optss:
                            print(res, end="")
                        elif "n" in optss and "e" in optss:
                            stdout.write(res)
                        elif "e" in optss:
                            stdout.write(res + "\n")
                        else:
                            print(res)
                    ljinux.based.user_vars["return"] = res
                else:
                    pass
    else:
        try:
            res = ljinux.based.fn.adv_input(ljinux.based.user_vars["argj"].split()[1], str)
            if not ljinux.based.silent:
                print(res)
            ljinux.based.user_vars["return"] = res
            del res
        except ValueError:
            print("based: Error: Variable not found!")
except (IndexError, NameError):
    ljinux.based.error(9)
    ljinux.based.user_vars["return"] = "1"
del optss
