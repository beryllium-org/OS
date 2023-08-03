rename_process("sleep")
try:
    pv[get_pid()]["t"] = int(ljinux.based.user_vars["argj"].split()[1]) * 2
    while pv[get_pid()]["t"] > 1:
        if not term.is_interrupted():
            time.sleep(0.5)
            pv[get_pid()]["t"] -= 1
        else:
            raise KeyboardInterrupt
    ljinux.api.setvar("return", "0")
except IndexError:
    time.sleep(1)
    ljinux.api.setvar("return", "0")
except KeyboardInterrupt:
    ljinux.api.setvar("return", "1")
