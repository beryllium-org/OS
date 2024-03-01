rename_process("sleep")
try:
    vr("t", int(be.based.user_vars["argj"].split()[1]) * 2)
    while vr("t") > 1:
        if not term.is_interrupted():
            time.sleep(0.5)
            vrm("t", 1)
        else:
            raise KeyboardInterrupt
    be.api.setvar("return", "0")
except IndexError:
    time.sleep(1)
    be.api.setvar("return", "0")
except KeyboardInterrupt:
    be.api.setvar("return", "1")
