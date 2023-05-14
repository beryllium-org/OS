if term.check_activity():
    while not console.connected:
        ljinux.io.ledset(4)
        time.sleep(0.4)
        ljinux.io.ledset(7)
        time.sleep(0.4)
    time.sleep(0.6)
else:
    term.anykey("\nCannot autodetect connection\nPress any key to open based shell\n")
