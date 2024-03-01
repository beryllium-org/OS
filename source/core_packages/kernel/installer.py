for pv[get_pid()]["filee"] in [
    "be.mpy",
    "lj_colours.mpy",
    "lj_colours_placebo.mpy",
    "neopixel_colors.mpy",
]:
    be.based.run("cp " + vr("filee") + " /lib/" + vr("filee"))

be.api.setvar("return", "0")
