rename_process("dmesg")
for pv[get_pid()]["i"] in pv[0]["dmesg"]:
    term.write(pv[get_pid()]["i"])
