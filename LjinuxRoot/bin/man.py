rename_process("man")
pv[get_pid()]["manls"] = listdir("/LjinuxRoot/usr/share/man")
pv[get_pid()]["manpages"] = set()
for pv[get_pid()]["manpage"] in pv[get_pid()]["manls"]:
    if pv[get_pid()]["manpage"].endswith(".man"):
        pv[get_pid()]["manpages"].add(pv[get_pid()]["manpage"][:-4])

pv[get_pid()]["opts"] = ljinux.api.xarg()

if len(pv[get_pid()]["opts"]["w"]) is 1:
    pv[get_pid()]["page_dayo"] = pv[get_pid()]["opts"]["w"][0]
    if pv[get_pid()]["page_dayo"] in pv[get_pid()]["manpages"]:
        ljinux.based.run(
            "less",
            ["/LjinuxRoot/usr/share/man/{}.man".format(pv[get_pid()]["page_dayo"])],
        )
    else:
        term.write(
            f"{colors.red_t}MAN-DB Error{colors.endc}: No such manual page found."
        )
        ljinux.api.setvar("return", "1")
else:
    ljinux.based.error(9)
    ljinux.api.setvar("return", "1")

ljinux.api.setvar("return", "0")
