"""
JPKG automatic list loader

TO BE USED AS A SUBSCRIPT

Returns in vr("pklist") a dict with every package name and its deps / conflicts
{package: [list(deps), list(conflicts)]}
"""

term.nwrite("Generating package list.. 0%")
vr("listing", listdir(pv[0]["root"] + "/etc/jpkg/installed/"))
vr("pkc", len(vr("listing")))  # package count
vr("pkl", 0)  # packages loaded
vr("cc", 2)  # currently displayed characters

vr("installed", {})  # All packages
vr("dependencies", set())  # All dependencies
vr("conflicts", set())  # All conflicts

from json import load

for pv[get_pid()]["package"] in vr("listing"):
    vr("name", vr("package")[:-5])  # remove ".json"
    vr(
        "omit",
        ([] if "omit" not in be.based.user_vars.keys() else be.api.getvar("omit")),
    )
    with be.api.fopen("/etc/jpkg/installed/" + vr("package")) as pv[get_pid()][
        "conf_f"
    ]:
        vr("manifest", load(vr("conf_f")))
        if vr("name") not in vr("omit"):
            vr("installed")[vr("name")] = [
                vr("manifest")["version"],
                vr("manifest")["dependencies"],
                vr("manifest")["conflicts"],
            ]
            for pv[get_pid()]["dependency"] in vr("manifest")["dependencies"]:
                vr("dependencies").add(vr("dependency"))
            for pv[get_pid()]["conflict"] in vr("manifest")["conflicts"]:
                conflicts.add(vr("conflict"))
        vrd("manifest")
    term.nwrite("\010 \010" * vr("cc"))
    vrp("pkl")
    vr("prc", str(int(vr("pkl") * 100 / vr("pkc"))))
    vr("cc", len(vr("prc")) + 1)
    term.nwrite(vr("prc") + "%")
    vrd("prc")

del load
term.write(("\010 \010" * vr("cc")) + "100%")
vr("pklist", [vr("installed"), vr("dependencies"), vr("conflicts")])
vrd("cc")
vrd("pkl")
vrd("pkc")
vrd("listing")
vrd("installed")
vrd("dependencies")
vrd("conflicts")
