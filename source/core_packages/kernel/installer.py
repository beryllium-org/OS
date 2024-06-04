for pv[get_pid()]["filee"] in [
    "be.mpy",
    "lj_colours.mpy",
    "lj_colours_placebo.mpy",
    "neopixel_colors.mpy",
]:
    be.based.run("cp " + vr("filee") + " /lib/" + vr("filee"))
be.based.run("cp stage1.py /usr/lib/kernel/stage1.py")
be.based.run("cp stage2.py /usr/lib/kernel/stage2.py")

be.api.setvar("return", "0")
