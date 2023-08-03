rename_process("ls")
pv[get_pid()]["opts"] = ljinux.api.xarg()
pv[get_pid()]["li"] = pv[get_pid()]["opts"]["hw"] + pv[get_pid()]["opts"]["w"]
pv[get_pid()]["co"] = "".join(pv[get_pid()]["opts"]["o"])

pv[get_pid()]["sps"] = "   "
pv[get_pid()]["path"] = "./"

if len(pv[get_pid()]["li"]):
    if ljinux.api.isdir(pv[get_pid()]["li"][0]) is 1:
        pv[get_pid()]["path"] = pv[get_pid()]["li"][0]
        if not pv[get_pid()]["path"].endswith("/"):
            pv[get_pid()]["path"] += "/"
    else:
        ljinux.based.error(2)

pv[get_pid()]["directory_listing"] = listdir(
    ljinux.api.betterpath(pv[get_pid()]["path"])
)
pv[get_pid()]["directory_listing"].sort()

if "l" in pv[get_pid()]["co"]:
    pv[get_pid()]["sps"] = "\n"

if "a" in pv[get_pid()]["co"]:
    term.write(colors.green_t + "." + colors.endc, end=pv[get_pid()]["sps"])
    if not (
        pv[get_pid()]["path"] == "/"
        or (pv[get_pid()]["path"] == "./" and getcwd() == "/")
    ):
        term.write(colors.green_t + ".." + colors.endc, end=pv[get_pid()]["sps"])

if pv[get_pid()]["directory_listing"] is not None:
    for pv[get_pid()]["dirr"] in pv[get_pid()]["directory_listing"]:
        pv[get_pid()]["col"] = ""
        if not ljinux.api.isdir(pv[get_pid()]["dirr"], pv[get_pid()]["path"]):
            if pv[get_pid()]["dirr"].startswith("."):
                pv[get_pid()]["col"] = colors.green_t
        else:
            pv[get_pid()]["col"] = colors.okcyan
        if pv[get_pid()]["dirr"][:1] == "." and not "a" in pv[get_pid()]["co"]:
            continue
        else:
            term.write(
                pv[get_pid()]["col"] + pv[get_pid()]["dirr"] + colors.endc,
                end=pv[get_pid()]["sps"],
            )

if not "l" in pv[get_pid()]["co"]:
    term.write()

ljinux.api.setvar("return", "0")
