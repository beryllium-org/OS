rename_process("dmesg")
for pv[get_pid()]["i"] in vr("dmesg", pid=0):
    term.write(vr("i"))
