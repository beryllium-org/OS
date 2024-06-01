vr("dev_name", "")
vr("devid_curr", len(vr("node")) - 1)
try:
    while vr("devid_curr"):
        if not vr("node")[vr("devid_curr")].isdigit():
            break
        vrm("devid_curr")
    vrp("devid_curr")
    vr("dev_name", vr("node")[: vr("devid_curr")])
    if vr("dev_name")[-1] == "_":
        vr("dev_name", vr("dev_name")[:-1])
    vr("dev_id", int(vr("node")[vr("devid_curr") :]))
    vr("ok", True)
except IndexError:
    pass
