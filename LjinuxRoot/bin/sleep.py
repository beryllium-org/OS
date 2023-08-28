rename_process("sleep")
try:
    vr("t", int(ljinux.based.user_vars["argj"].split()[1]) * 2)
    while vr("t") > 1:
        if not term.is_interrupted():
            time.sleep(0.5)
            vrm("t", 1)
        else:
            raise KeyboardInterrupt
    ljinux.api.setvar("return", "0")
except IndexError:
    time.sleep(1)
    ljinux.api.setvar("return", "0")
except KeyboardInterrupt:
    ljinux.api.setvar("return", "1")
