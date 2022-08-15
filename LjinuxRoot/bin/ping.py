args = ljinux.based.user_vars["argj"].split()[1:]
argl = len(args)
if "network" in ljinux.modules and ljinux.modules["network"].connected == True:
    if argl > 0:
        ljinux.based.user_vars["return"] = "0"
        domain = args[0]
        n = None
        if argl > 1 and args[1].startswith("n="):
            try:
                n = int(args[1][2:])
                if n < 1:
                    raise IndexError
            except:
                ljinux.based.error(1)
                ljinux.based.user_vars["return"] = "1"

        if ljinux.based.user_vars["return"] == "0":
            print(f"PING {domain} ({domain}) data.")
            done = 0
            good = 0
            bads = 0
            timetab = list()
            try:
                while True:
                    done += 1
                    a = ljinux.modules["network"].ping(domain)
                    if a is not None:
                        timetab.append(a)
                        good += 1
                        print(
                            f"PING from {domain}: icmp_seq={done} time={round(a*1000,1)} ms"
                        )
                    else:
                        bads += 1
                    del a
                    sleep(0.9)
                    if n is not None and n is done:
                        break
            except KeyboardInterrupt:
                print("^C")
            print(f"--- {domain} ping statistics ---")
            print(f"{done} packets transmitted, {good} received, {bads} lost")
            minn = round(min(timetab) * 1000, 1) if good else 0
            avgg = round((sum(timetab) / good) * 1000, 1) if good else 0
            maxx = round(max(timetab) * 1000, 1) if good else 0
            from ulab.numpy import std

            mdev = round(std(timetab) * 1000, 1) if good else 0
            print(f"rtt min/avg/max/mdev = {minn}/{avgg}/{maxx}/{mdev} ms")
            del done, good, bads, timetab, minn, avgg, maxx, mdev, std
        del domain, n
    else:
        ljinux.based.error(1)
        ljinux.based.user_vars["return"] = "1"
else:
    ljinux.based.error(5)
    ljinux.based.user_vars["return"] = "1"

del args, argl
