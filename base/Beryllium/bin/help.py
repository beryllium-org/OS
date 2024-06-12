rename_process("help")
term.write(
    f"LNL {colors.magenta_t}based{colors.endc}\nThese shell commands are defined internally or are in PATH.\nType 'help' to see this list.\n{colors.green_t}"
)

vr("lt", set(be.based.get_bins() + be.based.get_internal()))
vr("l", [])
vr("lenn", 0)
for pv[get_pid()]["i"] in vr("lt"):
    if not vr("i").startswith("_"):
        vr("l").append(vr("i"))
        if len(vr("i")) > vr("lenn"):
            vr("lenn", len(vr("i")))

vrp("lenn", 2)
vr("l").sort()

for pv[get_pid()]["index"], pv[get_pid()]["tool"] in enumerate(vr("l")):
    term.write(vr("tool"), end=(" " * vr("lenn")).replace(" ", "", len(vr("tool"))))
    if vr("index") % 4 == 3:
        term.write()
term.write(colors.endc)
