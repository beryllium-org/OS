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
        ljinux.api.setvar("argj", f"a /LjinuxRoot/usr/share/man/{page_dayo}.man")
        ljinux.based.command.fpexec("/bin/less.py")
    else:
        term.write(
            f"{colors.red_t}MAN-DB Error{colors.endc}: No such manual page found."
        )
        ljinux.api.setvar("return", "1")
    del page_dayo
else:
    ljinux.based.error(9)
    ljinux.api.setvar("return", "1")

ljinux.api.setvar("return", "0")
del opts
