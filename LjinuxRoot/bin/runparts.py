rename_process("runparts")
vr("opts", ljinux.api.xarg())
for pv[get_pid()]["i"] in vr("opts")["w"]:
    if ljinux.api.isdir(vr("i")) != 1:
        ljinux.based.error(17)
        ljinux.api.setvar("return", "1")
        break
    vr("drl", listdir(ljinux.api.betterpath(vr("i"))))
    pv[get_pid()]["drl"].sort()
    for pv[get_pid()]["j"] in vr("drl"):
        if vr("j").endswith(".py"):
            ljinux.based.command.fpexec(vr("i") + "/" + vr("j"))
