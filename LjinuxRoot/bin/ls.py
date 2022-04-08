argss_in = {}
in_l = 0
aa = False
ll = False
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
        print(".")
        rett += "."
        print("..")
        rett += ".."
    else:
        print(".", end="   ")
        rett += ".   "
        print("..", end="   ")
        rett += "..   "
    aa = True
    in_l += 2
for i in directory_listing:
    if (i)[:1] == ".":
        if aa:
            if not (ll):
                print(i, end="   ")
                rett += i + "   "
                in_l += 1
            else:
                print(i)
                rett += i
                in_l += 1
    else:
        if not (ll):
            print(i, end="   ")
            rett += i + "   "
            in_l += 1
        else:
            print(i)
            rett += i
            in_l += 1
if not (ll):
    print("\n", end="")
    rett += "\n"
ljinux.based.user_vars["return"] = rett
