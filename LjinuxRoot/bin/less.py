try:
    with open(
        ljinux.based.fn.betterpath(ljinux.based.user_vars["argj"].split()[1]), "r"
    ) as f:

        # prep work
        lines = f.readlines()
        lines1 = []
        for i in lines:
            lines1.append(i.replace("\n", "") if i != "\n" else i)
        del lines
        gc.collect()
        gc.collect()
        sizee = term.detect_size()  # get the terminal size

        # line splitting
        ljinux.based.user_vars["input"] = lines1
        del lines1
        ljinux.based.command.fpexecc(
            ["fpexec", "-n", "/LjinuxRoot/bin/stringproccessing/line_wrap.py"]
        )
        del ljinux.based.user_vars["input"]
        gc.collect()
        gc.collect()
        
        lines3 = ljinux.based.user_vars["output"]
        del ljinux.based.user_vars["output"]
        gc.collect()
        gc.collect()
        
        term_old = term.trigger_dict
        term.trigger_dict = {
            "inp_type": "prompt",
            "ctrlC": 1,
            "q": 1,
            "up": 2,
            "down": 3,
            "rest": "ignore",
            "echo": "none",
        }

        # The real work
        lc = len(lines3)
        target = (sizee[0] - 1) if (lc > sizee[0] - 1) else (lc - 1) # no of lines we have to display in the screen
        pos = 0 # holds scroll offset
        ctl = [0, None]
        while ctl[0] != 1:
            term.trigger_dict["prefix"] = f"{colors.white_bg_black_bg}lines {str(target+pos)}/{str(lc)} {str(int((float(target+pos) / float(lc)) * 100))}%{" (END)" if pos == lc-target else ""}{colors.endc}"
            for i in range(0, target):
                stdout.write(lines3[i+pos] + "\n" if lines3[i+pos] != "\n" else "\n")
                # yes this may not make much sense, but it's correct. Try removing it :)
            ctl = term.program()
            if ctl[0] == 2:
                if pos > 0:
                    pos -= 1
            elif ctl[0] == 3:
                if pos < lc-target:
                    pos += 1
            term.clear()
        del target, pos, lines3, lc
    ljinux.based.user_vars["return"] += "0"
    stdout.write("\n")
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
