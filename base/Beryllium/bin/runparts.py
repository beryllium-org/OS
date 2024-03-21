rename_process("runparts")
vr("opts", be.api.xarg())
for pv[get_pid()]["i"] in vr("opts")["w"]:
    if be.api.isdir(vr("i")) != 1:
        be.based.error(17)
        be.api.setvar("return", "1")
        break
    vr("drl", listdir(be.api.fs.resolve(vr("i"))))
    pv[get_pid()]["drl"].sort()
    for pv[get_pid()]["j"] in vr("drl"):
        if vr("j").endswith(".py"):
            be.based.command.fpexec(vr("i") + "/" + vr("j"))
        elif vr("j").endswith(".lja"):
            be.based.command.exec(vr("i") + "/" + vr("j"))
