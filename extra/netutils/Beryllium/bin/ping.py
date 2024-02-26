rename_process("ping")
vr("args", be.based.user_vars["argj"].split()[1:])
vr("argl", len(vr("args")))
if "network" in be.devices and be.devices["network"][0].connected:
    if vr("argl") > 0:
        be.api.setvar("return", "0")
        vr("domain", vr("args")[0])
        if vr("argl") > 1 and vr("args")[1].startswith("n="):
            try:
                vr("n", int(vr("args")[1][2:]))
                if vr("n") < 1:
                    raise IndexError
            except:
                be.based.error(1)
                be.api.setvar("return", "1")

        if be.api.getvar("return") == "0":
            vr("resolved", vr("domain"))
            try:
                vr("resolved", be.devices["network"][0].resolve(vr("domain")))
                term.write("PING {} ({}) data.".format(vr("domain"), vr("resolved")))
                vr("done", 0)
                vr("good", 0)
                vr("bads", 0)
                vr("timetab", [])
                try:
                    while not term.is_interrupted():
                        be.io.ledset(3)
                        vrp("done")
                        vr("a", be.devices["network"][0].ping(vr("domain")))
                        if vr("a") is not None:
                            vra("timetab", float(vr("a")))
                            vrp("good")
                            term.write(
                                "PING from {}: icmp_seq={} time={} ms".format(
                                    vr("domain"),
                                    vr("done"),
                                    round(vr("a") * 1000, 1),
                                )
                            )
                        else:
                            vrp("bads")
                        be.io.ledset(2)
                        sleep(0.9)
                        if "n" in pv[get_pid()].keys() and vr("n") is vr("done"):
                            break
                except KeyboardInterrupt:
                    term.write("^C")
                term.write(
                    "--- {} ping statistics ---\n{} packets transmitted, {} received, {} lost".format(
                        vr("domain"),
                        vr("done"),
                        vr("good"),
                        vr("bads"),
                    )
                )

                vr("minn", (round(min(vr("timetab")) * 1000, 1) if vr("good") else 0))
                vr(
                    "avgg",
                    (
                        round(
                            (sum(vr("timetab")) / vr("good")) * 1000,
                            1,
                        )
                        if vr("good")
                        else 0
                    ),
                )
                vr("maxx", (round(max(vr("timetab")) * 1000, 1) if vr("good") else 0))
                from ulab.numpy import std

                vr("mdev", (round(std(vr("timetab")) * 1000, 1) if vr("good") else 0))
                term.write(
                    "rtt min/avg/max/mdev = {}/{}/{}/{} ms".format(
                        vr("minn"),
                        vr("avgg"),
                        vr("maxx"),
                        vr("mdev"),
                    )
                )
                del std
            except ConnectionError:
                term.write("Domain could not be resolved.")
    else:
        be.based.error(1)
        be.api.setvar("return", "1")
else:
    be.based.error(5)
    be.api.setvar("return", "1")
