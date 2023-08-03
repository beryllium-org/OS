rename_process("alias")
try:
    pv[get_pid()]["inpt"] = ljinux.based.user_vars["argj"].split()
    pv[get_pid()]["eqpos"] = pv[get_pid()]["inpt"][1].find("=", 0)
    pv[get_pid()]["cmd"] = pv[get_pid()]["inpt"][1][: pv[get_pid()]["eqpos"]]
    pv[get_pid()]["alcmd"] = pv[get_pid()]["inpt"][1][pv[get_pid()]["eqpos"] + 1 :]
    pv[get_pid()]["offs"] = 1
    if pv[get_pid()]["alcmd"].startswith('"'):
        pv[get_pid()]["alcmd"] = pv[get_pid()]["alcmd"][1:]
        while not pv[get_pid()]["alcmd"].endswith('"'):
            pv[get_pid()]["offs"] += 1
            pv[get_pid()]["alcmd"] += " " + pv[get_pid()]["inpt"][pv[get_pid()]["offs"]]
        pv[get_pid()]["alcmd"] = pv[get_pid()]["alcmd"][:-1]
    else:
        raise IndexError
    ljinux.based.alias_dict[pv[get_pid()]["cmd"]] = pv[get_pid()]["alcmd"]
    ljinux.api.setvar("return", "0")
except IndexError:
    ljinux.based.error(1)
    ljinux.api.setvar("return", "1")
