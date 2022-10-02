"""
JPKG automatic list loader

Returns in user_vars["return"] a dict with every package name and its deps / conflicts
{package: [list(deps), list(conflicts)]}
"""

stdout.write("Generating package list.. 0%")
listing = listdir("/LjinuxRoot/etc/dpkg/installed")
pkc = len(a)
pkl = 0
cc = 2

installed = dict()

for i in listing:
    name = i[:-5]  # remove ".json"
    conf = None
    with ljinux.based.fn.fopen("/etc/jpkg/installed/" + i) as conf_f:
        conf = json.load(conf_f)
    installed.update({name: [conf["dependencies"], conf["conflicts"]]})
    stdout.write("\010 \010" * cc)
    pkl += 1
    prc = int(pkl * 100 / pkc)
    cc = len(prc) + 1
    stdout.write(str(prc) + "%")
    del prc

stdout.write(("\010 \010" * cc) + "100%\n")
ljinux.based.user_vars["return"] = installed
del cc, pkl, pkc, listing, installed
