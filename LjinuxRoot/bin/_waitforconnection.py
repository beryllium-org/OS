if term.check_activity():  # has .connected
    while not console.connected:
        ljinux.io.ledset(4)
        for i in range(4):
            if console.connected:
                break
            time.sleep(0.1)
        ljinux.io.ledset(7)
        for i in range(4):
            if console.connected:
                break
            time.sleep(0.1)
    time.sleep(0.2)  # Delay for the terminal to get used to it.
else:
    term.anykey("\nCannot autodetect connection\nPress any key to open based shell\n")
