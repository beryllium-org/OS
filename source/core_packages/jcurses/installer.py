for pv[get_pid()]["filee"] in ["jcurses.mpy", "jcurses_data.mpy"]:
    be.based.run("cp " + vr("filee") + " /lib/" + vr("filee"))

be.api.setvar("return", "0")
