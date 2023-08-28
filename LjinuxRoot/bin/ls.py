rename_process("ls")
vr("opts", ljinux.api.xarg())
vr("li", vr("opts")["hw"] + vr("opts")["w"])
vr("co", "".join(vr("opts")["o"]))

vr("sps", "   ")
vr("path", "./")

if len(vr("li")):
    if ljinux.api.isdir(vr("li")[0]) is 1:
        vr("path", vr("li")[0])
        if not vr("path").endswith("/"):
            vrp("path", "/")
    else:
        ljinux.based.error(2)

vr("directory_listing", listdir(ljinux.api.betterpath(vr("path"))))
pv[get_pid()]["directory_listing"].sort()

if "l" in vr("co"):
    vr("sps", "\n")

if "a" in vr("co"):
    term.write(colors.green_t + "." + colors.endc, end=vr("sps"))
    if not (vr("path") == "/" or (vr("path") == "./" and getcwd() == "/")):
        term.write(colors.green_t + ".." + colors.endc, end=vr("sps"))

if vr("directory_listing") is not None:
    for pv[get_pid()]["dirr"] in vr("directory_listing"):
        vr("col", "")
        if not ljinux.api.isdir(vr("dirr"), vr("path")):
            if vr("dirr").startswith("."):
                vr("col", colors.green_t)
        else:
            vr("col", colors.okcyan)
        if vr("dirr")[:1] == "." and not "a" in vr("co"):
            continue
        else:
            term.write(
                vr("col") + vr("dirr") + colors.endc,
                end=vr("sps"),
            )

if not "l" in vr("co"):
    term.write()

ljinux.api.setvar("return", "0")
