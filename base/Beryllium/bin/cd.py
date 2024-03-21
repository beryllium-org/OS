rename_process("cd")
vr("capdir", getcwd())
vr("opts", be.api.xarg())
if len(vr("opts")["w"]):
    vr("target", vr("opts")["w"][0])
    if vr("target") == "-":
        vr("target", be.based.user_vars["prevdir"])
else:
    vr("target", "~")
vr("dr", be.api.isdir(vr("target")))
if vr("dr") == 1:
    chdir(be.api.fs.resolve(vr("target")))
    if vr("capdir") != getcwd():
        be.api.setvar("prevdir", vr("capdir"))
        be.based.olddir = getcwd()
elif not vr("dr"):
    be.based.error(14, "cd")
else:
    be.based.error(17, "cd")
