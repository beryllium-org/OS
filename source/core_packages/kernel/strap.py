for i in ["be.mpy", "lj_colours.mpy", "lj_colours_placebo.mpy", "neopixel_colors.mpy"]:
    shutil.copyfile(i, path.join(root, "lib", i))
