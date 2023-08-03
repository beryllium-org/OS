rename_process("m5x-shutdown")
ljinux.io.ledset(1)
ljinux.deinit_consoles()
vr("a", digitalio.DigitalInOut(board.BAT_HOLD))
pv[get_pid()]["a"].switch_to_output()
pv[get_pid()]["a"].value = 0
while True:
    try:
        try:
            sleep(100)
        except KeyboardInterrupt:
            pass
    except KeyboardInterrupt:
        pass
