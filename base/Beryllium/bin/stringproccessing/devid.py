vr("dev_name", "")
vr("devid_curr", 0)
try:
    while True:
        if (vr("node").rfind("_") != -1) and (
            vr("node")[vr("node").rfind("_") - 1].isdigit()
        ):
            if vr("node").rfind("_") == vr("devid_curr"):
                break
        else:
            if vr("node")[vr("devid_curr")].isdigit() or vr("devid_curr") == len(
                vr("node")
            ):
                break
        vrp("dev_name", vr("node")[vr("devid_curr")])
        vrp("devid_curr")
    if vr("node")[vr("devid_curr")] == "_":
        vrp("devid_curr")
    vr("dev_id", "")
    while vr("devid_curr") < len(vr("node")):
        vrp("dev_id", vr("node")[vr("devid_curr")])
        vrp("devid_curr")
    vr("dev_id", int(vr("dev_id")))
    vr("ok", True)
except IndexError:
    pass
