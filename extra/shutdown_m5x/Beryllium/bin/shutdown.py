rename_process("m5x-shutdown")
be.io.ledset(1)
be.deinit_consoles()
be.based.run("gp#BAT_HOLD = 0")
print("You can safely disconnect the board from power")
while True:
    try:
        try:
            sleep(100)
        except KeyboardInterrupt:
            pass
    except KeyboardInterrupt:
        pass
