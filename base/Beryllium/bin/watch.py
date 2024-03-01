rename_process("watch")
vr("opts", be.api.xarg())
vr("fw", vr("opts")["hw"] + vr("opts")["w"])

# Get time
vr("tts", 2.0)
if "n" in vr("opts")["o"]:
    vr("tts", float(vr("opts")["o"]["n"]))
    pv[get_pid()]["fw"].pop(vr("fw").index(vr("opts")["o"]["n"]))

# Get wordlist
vr("cmd", " ".join(vr("fw")))
vrd("fw")

# Do it
try:
    while not term.is_interrupted():
        term.hold_stdout = True
        term.clear()
        if "s" not in vr("opts")["o"]:
            term.write("Every {}s: {}".format(vr("tts"), vr("cmd")))
        be.based.run(vr("cmd"))
        term.hold_stdout = False
        term.flush_writes()
        be.io.ledset(1)
        time.sleep(vr("tts"))
except KeyboardInterrupt:
    pass
term.hold_stdout = False
term.clear()
term.flush_writes()
