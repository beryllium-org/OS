if (not hasattr(console, "fake")) and console.connected:
    term.hold_stdout = False
    term.flush_writes()
    systemprints(1, "Detected early serial connection")
    systemprints(1, "Dmesg flush")
