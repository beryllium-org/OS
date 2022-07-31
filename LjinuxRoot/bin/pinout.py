try:
    with open(
        ljinux.based.fn.betterpath("/bin/pinouts/pinout-" + board.board_id + ".map"), "r"
    ) as f:
        for line in f:
            print(line, end="")
            del line
        del f
    gc.collect()
    gc.collect()
    ljinux.based.user_vars["return"] = "0"
except OSError:
    print("Board id does not match any known ones.. sus.")
    ljinux.based.user_vars["return"] = "1"
