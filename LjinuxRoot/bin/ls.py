argss_in = {}

in_l = 0

aa = ll = False

rett = ""

directory_listing = listdir()
try:
    if "-" == ljinux.based.user_vars["argj"].split()[1][:1]:
        argss_in = list(ljinux.based.user_vars["argj"].split()[1][1:])
except IndexError:
    pass

if "l" in argss_in:
    ll = True

if "a" in argss_in:
    if ll:
        print(colors.green_t + "." + colors.endc)
        rett += "."
        print(colors.green_t + ".." + colors.endc)
        rett += ".."
    else:
        print(colors.green_t + "." + colors.endc, end="   ")
        rett += ".   "
        print(colors.green_t + ".." + colors.endc, end="   ")
        rett += "..   "
    aa = True
    in_l += 2

for dir in directory_listing:
    if dir[:1] == ".":
        if aa:
            if not ll:
                print(colors.magenta_t + dir + colors.endc, end="   ")
                rett += dir + "   "
            else:
                print(colors.magenta_t + dir + colors.endc)
                rett += dir
    else:
        if not ll:
            print(colors.magenta_t + dir + colors.endc, end="   ")
            rett += dir + "   "
        else:
            print(colors.magenta_t + dir + colors.endc)
            rett += dir
    in_l += 1

if not ll:
    print("\n", end="")
    rett += "\n"

ljinux.based.user_vars["return"] = rett
