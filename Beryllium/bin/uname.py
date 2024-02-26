try:
    if be.based.user_vars["argj"].split()[1] == "-a":
        vr("tt", time.localtime())
        vr(
            "dat",
            [
                be.based.system_vars["BOARD"],
                be.based.system_vars["VERSION"],
                vr("tt").tm_year,
                vr("tt").tm_mday,
                vr("tt").tm_mon,
                vr("tt").tm_hour,
                vr("tt").tm_min,
                vr("tt").tm_sec,
            ],
        )

        for pv[get_pid()]["i"] in range(3, 8):
            pv[get_pid()]["dat"][vr("i")] = str(vr("dat")[vr("i")])
            if len(vr("dat")[vr("i")]) == 1:
                pv[get_pid()]["dat"][vr("i")] = "0" + vr("dat")[vr("i")]

        term.write(
            "Beryllium {} {} {}/{}/{} {}:{}:{} circuitpython Beryllium".format(
                vr("dat")[0],
                vr("dat")[1],
                vr("dat")[3],
                vr("dat")[4],
                vr("dat")[2],
                vr("dat")[5],
                vr("dat")[6],
                vr("dat")[7],
            )
        )
except IndexError:
    term.write("Beryllium")
be.api.setvar("return", "0")
