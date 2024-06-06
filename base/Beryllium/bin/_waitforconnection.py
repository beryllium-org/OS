rename_process("waitforconnection")
while True:
    for pv[get_pid()]["i"] in range(2):
        be.io.ledset(7)
        sleep(0.1)
        be.io.ledset(4)
        sleep(0.1)
    if be.api.console_connected():
        break
    be.io.ledset(4)
    be.api.tasks.run()
    time.sleep(0.2)
time.sleep(0.2)  # Delay for the terminal to get used to it.
term.clear_line(True)
term.clear_buffer()
# Switch to tiny shell prefix if the terminal is too narrow
vr("sz", term.detect_size())
if vr("sz") is not False:
    if vr("sz")[1] < 60:
        be.api.setvar("PSA", "2")
    else:
        be.api.setvar("PSA", "1")
term.hold_stdout = False
