rename_process("watch")
pv[get_pid()]["opts"] = ljinux.api.xarg()
pv[get_pid()]["fw"] = pv[get_pid()]["opts"]["hw"] + pv[get_pid()]["opts"]["w"]

# Get time
pv[get_pid()]["tts"] = 2.0
if "n" in pv[get_pid()]["opts"]["o"]:
    pv[get_pid()]["tts"] = float(pv[get_pid()]["opts"]["o"]["n"])
    pv[get_pid()]["fw"].pop(pv[get_pid()]["fw"].index(pv[get_pid()]["opts"]["o"]["n"]))

# Get wordlist
pv[get_pid()]["cmd"] = " ".join(pv[get_pid()]["fw"])
del pv[get_pid()]["fw"]

# Do it
try:
    while not term.is_interrupted():
        term.hold_stdout = True
        term.clear()
        if "s" not in pv[get_pid()]["opts"]["o"]:
            term.write(
                "Every {}s: {}".format(pv[get_pid()]["tts"], pv[get_pid()]["cmd"])
            )
        ljinux.based.run(pv[get_pid()]["cmd"])
        term.hold_stdout = False
        term.flush_writes()
        ljinux.io.ledset(1)
        time.sleep(pv[get_pid()]["tts"])
except KeyboardInterrupt:
    pass
term.hold_stdout = False
term.clear()
term.flush_writes()
