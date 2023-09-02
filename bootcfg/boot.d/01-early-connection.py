# Detect early serial connections and make logging immediately available
rename_process("earlyconnection")
vr("found", False)
for pv[get_pid()]["i"] in pv[0]["consoles"].keys():
    if hasattr(vr("consoles", pid=0)[vr("i")], "connected"):
        if vr("consoles", pid=0)[vr("i")].connected:
            term.console = vr("consoles", pid=0)[vr("i")]
            vr("console_active", vr("i"), pid=0)
            vr("found", True)
            break
    else:
        if vr("consoles", pid=0)[vr("i")].in_waiting:
            term.console = pv[0]["consoles"][pv[get_pid()]["i"]]
            term.console = vr("consoles", pid=0)[vr("i")]
            vr("console_active", vr("i"), pid=0)
            vr("consoles", pid=0)[vr("i")].reset_input_buffer()
            vr("found", True)
            break
if pv[get_pid()]["found"]:
    term.hold_stdout = False
    term.flush_writes()
    systemprints(1, "Detected early serial connection")
    systemprints(1, "Dmesg flush")
