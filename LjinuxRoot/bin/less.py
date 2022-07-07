try:
    with open(
        ljinux.based.fn.betterpath(ljinux.based.user_vars["argj"].split()[1]), "r"
    ) as f:

        sizee = term.detect_size()  # get the terminal size

        # line splitting
        ljinux.based.user_vars["input"] = [ 
            line.replace('\n', '') for line in f if line != '\n' else line
        ]   
        
        ljinux.based.command.fpexecc(
            ["fpexec", "-n", "/LjinuxRoot/bin/stringproccessing/line_wrap.py"]
        )
        
        del ljinux.based.user_vars["input"]


        lines3 = ljinux.based.user_vars["output"]
        del ljinux.based.user_vars["output"]

        term_old = term.trigger_dict
        term.trigger_dict = {
            "inp_type": "prompt",
            "ctrlC": 1,
            "q": 1,
            "up": 2,
            "down": 3,
            "pgup": 4,
            "pgdw": 5,
            "home": 6,
            "end": 7,
            "rest": "ignore",
            "echo": "none",
        }

        # The real work
        lc = len(lines3)
        target = (
            (sizee[0] - 1) if (lc > sizee[0] - 1) else lc
        )  # no of lines we have to display in the screen
        pos = 0  # holds scroll offset
        ctl = [0, None]
        endt = " (END)"
        blank = ""
        term.clear()
        
        while ctl[0] != 1:
            term.trigger_dict[
                "prefix"
            ] = f"{colors.white_bg_black_bg}lines {pos}-{target+pos}/{lc} {int(target+pos*100/lc)}%{endt if pos == lc-target else blank}{colors.endc}"
            
            for i in range(target):
                stdout.write(
                    lines3[i + pos] + "\n" if lines3[i + pos] != "\n" else "\n"
                )

            ctl = term.program()
            if ctl[0] == 2:
                if pos > 0:
                    pos -= 1
            elif ctl[0] == 3:
                if pos < lc - target:
                    pos += 1
            elif ctl[0] == 4:
                if pos > target:
                    pos -= target
                else:
                    pos = 0
            elif ctl[0] == 5:
                if pos < lc - 2 * target:
                    pos += target
                else:
                    pos = lc - target
            elif ctl[0] == 6:
                pos = 0  # ez -- blade 2020
            elif ctl[0] == 7:
                pos = lc - target
            term.clear()
        del target, pos, lines3, lc, blank, endt
    ljinux.based.user_vars["return"] += "0"
    term.trigger_dict = term_old
    del term_old
    gc.collect()
    gc.collect()

except OSError:
    ljinux.based.error(4, ljinux.based.user_vars["argj"].split()[1])
    ljinux.based.user_vars["return"] = "1"

except IndexError:
    ljinux.based.error(1)
    ljinux.based.user_vars["return"] = "1"
