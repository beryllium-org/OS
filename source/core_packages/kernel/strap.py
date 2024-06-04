for i in ["be.mpy", "lj_colours.mpy", "lj_colours_placebo.mpy", "neopixel_colors.mpy"]:
    shutil.copyfile(i, path.join(root, "lib", i))

for i in range(1, 3):
    shutil.copyfile(f"stage{i}.py", path.join(root, f"usr/lib/kernel/stage{i}.py"))
