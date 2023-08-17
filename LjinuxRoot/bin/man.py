rename_process("man")
vr("manls", listdir("/LjinuxRoot/usr/share/man"))
vr("manpages", set())
for pv[get_pid()]["manpage"] in vr("manls"):
    if vr("manpage").endswith(".man"):
        pv[get_pid()]["manpages"].add(vr("manpage")[:-4])

vr("opts", ljinux.api.xarg())

if len(vr("opts")["w"]) is 1:
    vr("page_dayo", vr("opts")["w"][0])
    if vr("page_dayo") in vr("manpages"):
        ljinux.based.run(
            "less",
            ["/LjinuxRoot/usr/share/man/{}.man".format(vr("page_dayo"))],
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
