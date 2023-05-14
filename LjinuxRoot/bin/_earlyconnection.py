if term.check_activity() and console.connected:
    term.hold_stdout = False
    term.flush_writes()
    systemprints(1, "Detected early serial connection")
    systemprints(1, "Dmesg flush")
