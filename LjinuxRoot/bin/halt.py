vr("Exit_code", 245, pid=0)
vr("Exit", True, pid=0)
term.nwrite("System halted, press Ctrl+C to restart.")
try:
    while not term.is_interrupted():
        ljinux.io.ledset(2)
        sleep(0.1)
        ljinux.io.ledset(0)
        sleep(0.9)
except KeyboardInterrupt:
    term.write()
