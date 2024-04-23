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
term.flush_writes()
term.hold_stdout = False
