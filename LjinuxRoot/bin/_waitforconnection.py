rename_process("waitforconnection")
while True:
    for pv[get_pid()]["i"] in range(2):
        ljinux.io.ledset(7)
        sleep(0.1)
        ljinux.io.ledset(4)
        sleep(0.1)
    if ljinux.api.console_connected():
        break
    ljinux.io.ledset(4)
    time.sleep(0.2)
time.sleep(0.2)  # Delay for the terminal to get used to it.
term.clear_line()
