cont = True
while cont:
    for i in consoles.keys():
        ljinux.io.ledset(4)
        time.sleep(0.1)
        if hasattr(consoles[i], "connected"):
            if consoles[i].connected:
                term.console = consoles[i]
                globals()["console_active"] = i
                cont = False
            else:
                ljinux.io.ledset(7)
                time.sleep(0.1)
        else:
            if consoles[i].in_waiting:
                term.console = consoles[i]
                globals()["console_active"] = i
                consoles[i].reset_input_buffer()
                cont = False
            else:
                consoles[i].write(
                    b"\nCannot autodetect connection\nPress any key to continue\n"
                )
                ljinux.io.ledset(7)
                time.sleep(0.3)  # Reduced spam
        del i
del cont
time.sleep(0.2)  # Delay for the terminal to get used to it.
