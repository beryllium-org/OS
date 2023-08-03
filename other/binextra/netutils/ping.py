rename_process("ping")
pv[get_pid()]["args"] = ljinux.based.user_vars["argj"].split()[1:]
pv[get_pid()]["argl"] = len(pv[get_pid()]["args"])
if "network" in ljinux.modules and ljinux.modules["network"].connected:
    if pv[get_pid()]["argl"] > 0:
        ljinux.api.setvar("return", "0")
        pv[get_pid()]["domain"] = pv[get_pid()]["args"][0]
        if pv[get_pid()]["argl"] > 1 and pv[get_pid()]["args"][1].startswith("n="):
            try:
                pv[get_pid()]["n"] = int(pv[get_pid()]["args"][1][2:])
                if pv[get_pid()]["n"] < 1:
                    raise IndexError
            except:
                ljinux.based.error(1)
                ljinux.api.setvar("return", "1")

        if ljinux.api.getvar("return") == "0":
            pv[get_pid()]["resolved"] = pv[get_pid()]["domain"]
            try:
                pv[get_pid()]["resolved"] = ljinux.modules["network"].resolve(
                    pv[get_pid()]["domain"]
                )
                term.write(
                    "PING {} ({}) data.".format(
                        pv[get_pid()]["domain"], pv[get_pid()]["resolved"]
                    )
                )
                pv[get_pid()]["done"] = 0
                pv[get_pid()]["good"] = 0
                pv[get_pid()]["bads"] = 0
                pv[get_pid()]["timetab"] = []
                try:
                    while not term.is_interrupted():
                        ljinux.io.ledset(3)
                        pv[get_pid()]["done"] += 1
                        pv[get_pid()]["a"] = ljinux.modules["network"].ping(
                            pv[get_pid()]["domain"]
                        )
                        if pv[get_pid()]["a"] is not None:
                            pv[get_pid()]["timetab"].append(pv[get_pid()]["a"])
                            pv[get_pid()]["good"] += 1
                            term.write(
                                "PING from {}: icmp_seq={} time={} ms".format(
                                    pv[get_pid()]["domain"],
                                    pv[get_pid()]["done"],
                                    round(pv[get_pid()]["a"] * 1000, 1),
                                )
                            )
                        else:
                            pv[get_pid()]["bads"] += 1
                        ljinux.io.ledset(2)
                        sleep(0.9)
                        if (
                            "n" in pv[get_pid()].keys()
                            and pv[get_pid()]["n"] is pv[get_pid()]["done"]
                        ):
                            break
                except KeyboardInterrupt:
                    term.write("^C")
                term.write(
                    "--- {} ping statistics ---\n{} packets transmitted, {} received, {} lost".format(
                        pv[get_pid()]["domain"],
                        pv[get_pid()]["done"],
                        pv[get_pid()]["good"],
                        pv[get_pid()]["bads"],
                    )
                )

                pv[get_pid()]["minn"] = (
                    round(min(pv[get_pid()]["timetab"]) * 1000, 1)
                    if pv[get_pid()]["good"]
                    else 0
                )
                pv[get_pid()]["avgg"] = (
                    round(
                        (sum(pv[get_pid()]["timetab"]) / pv[get_pid()]["good"]) * 1000,
                        1,
                    )
                    if pv[get_pid()]["good"]
                    else 0
                )
                pv[get_pid()]["maxx"] = (
                    round(max(pv[get_pid()]["timetab"]) * 1000, 1)
                    if pv[get_pid()]["good"]
                    else 0
                )
                from ulab.numpy import std

                pv[get_pid()]["mdev"] = (
                    round(std(pv[get_pid()]["timetab"]) * 1000, 1)
                    if pv[get_pid()]["good"]
                    else 0
                )
                term.write(
                    "rtt min/avg/max/mdev = {}/{}/{}/{} ms".format(
                        pv[get_pid()]["minn"],
                        pv[get_pid()]["avgg"],
                        pv[get_pid()]["maxx"],
                        pv[get_pid()]["mdev"],
                    )
                )
                del std
            except ConnectionError:
                term.write("Domain could not be resolved.")
    else:
        ljinux.based.error(1)
        ljinux.api.setvar("return", "1")
else:
    ljinux.based.error(5)
    ljinux.api.setvar("return", "1")
