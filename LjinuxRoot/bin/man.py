manls = listdir("/LjinuxRoot/usr/share/man")
manpages = set()
for manpage in manls:
    if manpage.endswith(".man"):
        manpages.add(manpage[:-4])
    del manpage
del manls

opts = ljinux.api.xarg()

if len(opts["w"]) is 1:
    page_dayo = opts["w"][0]
    if page_dayo in manpages:
        ljinux.api.var("argj", f"a /LjinuxRoot/usr/share/man/{page_dayo}.man")
        ljinux.based.command.fpexecc([None, "/bin/less.py"])
    else:
        print(f"{colors.red_t}MAN-DB Error{colors.endc}: No such manual page found.")
        ljinux.api.var("return", "1")
    del page_dayo
else:
    ljinux.based.error(9)
    ljinux.api.var("return", "1")

ljinux.api.var("return", "0")
del opts
