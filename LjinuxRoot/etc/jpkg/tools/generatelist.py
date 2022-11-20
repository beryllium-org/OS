"""
JPKG automatic list loader

Returns in user_vars["return"] a dict with every package name and its deps / conflicts
{package: [list(deps), list(conflicts)]}
"""

stdout.write("Generating package list.. 0%")
listing = listdir("/LjinuxRoot/etc/jpkg/installed/")
pkc = len(listing)  # package count
pkl = 0  # packages loaded
cc = 2  # currently displays characters

installed = dict()  # All packages
dependencies = set()  # All dependencies
conflicts = set()  # All conflicts

for package in listing:
    name = package[:-5]  # remove ".json"
    omit = (
        []
        if "omit" not in ljinux.based.user_vars.keys()
        else ljinux.based.user_vars["omit"]
    )
    with ljinux.api.fopen("/etc/jpkg/installed/" + package) as conf_f:
        manifest = json.load(conf_f)
        if name not in omit:
            installed.update(
                {
                    name: [
                        manifest["version"],
                        manifest["dependencies"],
                        manifest["conflicts"],
                    ]
                }
            )
            for dependency in manifest["dependencies"]:
                dependencies.add(dependency)
                del dependency
            for conflict in manifest["conflicts"]:
                conflicts.add(conflict)
                del conflict
        del manifest
    del omit
    stdout.write("\010 \010" * cc)
    pkl += 1
    prc = str(int(pkl * 100 / pkc))
    cc = len(prc) + 1
    stdout.write(prc + "%")
    del prc, package

stdout.write(("\010 \010" * cc) + "100%\n")
ljinux.api.setvar("return", [installed, dependencies, conflicts])
del cc, pkl, pkc, listing, installed, dependencies, conflicts
