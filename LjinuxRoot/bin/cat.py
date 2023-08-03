rename_process("cat")
pv[get_pid()]["inpt"] = ljinux.based.user_vars["argj"].split()

try:
    with ljinux.api.fopen(pv[get_pid()]["inpt"][1], "r") as pv[get_pid()]["f"]:
        for pv[get_pid()]["line"] in pv[get_pid()]["f"]:
            term.nwrite(pv[get_pid()]["line"])
            del pv[get_pid()]["line"]
    ljinux.api.setvar("return", "0")

except OSError:
    ljinux.based.error(4, inpt[1])
    ljinux.api.setvar("return", "1")

except IndexError:
    ljinux.based.error(1)
    ljinux.api.setvar("return", "1")
