rename_process("man")
vr("manls", listdir(pv[0]["root"] + "/usr/share/man"))
vr("manpages", set())
for pv[get_pid()]["manpage"] in vr("manls"):
    if vr("manpage").endswith(".man"):
        vr("manpages").add(vr("manpage")[:-4])

vr("opts", be.api.xarg())

if len(vr("opts")["w"]) is 1:
    vr("page_dayo", vr("opts")["w"][0])
    if vr("page_dayo") in vr("manpages"):
        be.based.run(
            "less /usr/share/man/{}.man".format(vr("page_dayo")),
        )
    else:
        term.write(
            f"{colors.red_t}MAN-DB Error{colors.endc}: No such manual page found."
        )
        be.api.setvar("return", "1")
else:
    be.based.error(9)
    be.api.setvar("return", "1")

be.api.setvar("return", "0")
