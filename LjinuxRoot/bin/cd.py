rename_process("cd")
vr("capdir", getcwd())
vr("opts", ljinux.api.xarg())
if len(vr("opts")["w"]):
    vr("target", vr("opts")["w"][0])
    if vr("target") == "-":
        vr("target", ljinux.based.user_vars["prevdir"])
else:
    vr("target", "~")
vr("dr", ljinux.api.isdir(vr("target")))
if vr("dr") == 1:
    chdir(ljinux.api.betterpath(vr("target")))
    if vr("capdir") != getcwd():
        ljinux.api.setvar("prevdir", vr("capdir"))
        ljinux.based.olddir = getcwd()
elif not vr("dr"):
    ljinux.based.error(14, "cd")
else:
    ljinux.based.error(17, "cd")
