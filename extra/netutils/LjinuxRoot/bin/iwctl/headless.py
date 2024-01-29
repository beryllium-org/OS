vr("passwd", None)
vr("inc", 1)
if vr("args")[0] == "--passphrase":
    if vr("args")[1].startswith('"'):
        while True:
            if vr("args")[vr("inc")].endswith('"'):
                break
            elif vr("inc") < vr("argl"):
                vrp("inc")
            else:
                ljinux.based.error(1)
                vrm("inc")
        if vr("inc") is not -1:
            vr("passwd", vr("args")[1] + " ")
            for pv[get_pid()]["i"] in range(2, vr("inc") + 1):
                vrp("passwd", vr("args")[vr("i")] + " ")
            vr("passwd", vr("passwd")[1:-2])
    else:
        vr("passwd", vr("args")[1])
else:
    vr("inc", None)
if vr("inc") is not None:
    vrp("inc")
    vr("args", vr("args")[vr("inc") :])
    vrm("argl", vr("inc"))

if vr("argl") > 2 and vr("args")[0] == "station" and vr("args")[1] == vr("device_n"):
    if vr("argl") > 3 and vr("args")[2] == "connect":
        vr("networks", ljinux.devices["network"][0].scan())
        if vr("args")[3] in vr("networks"):
            vr("res", False)
            if vr("networks")[vr("args")[3]][0] != "OPEN":
                vr("tpd", cptoml.fetch(vr("args")[3], subtable="IWD"))
                if vr("passwd") is not None:
                    ljinux.devices["network"][0].disconnect()
                    ljinux.devices["network"][0].disconnect_ap()
                    dmtex('IWD: Connecting to: "{}"'.format(vr("args")[3]))
                    vr(
                        "res",
                        ljinux.devices["network"][0].connect(
                            vr("args")[3], vr("passwd")
                        ),
                    )
                elif vr("tpd") is not None:
                    ljinux.devices["network"][0].disconnect()
                    ljinux.devices["network"][0].disconnect_ap()
                    dmtex(
                        'IWD: Connecting to: "{}" with stored password.'.format(
                            vr("args")[3]
                        )
                    )
                    vr(
                        "res",
                        ljinux.devices["network"][0].connect(vr("args")[3], vr("tpd")),
                    )
                else:
                    term.write("Error: No password specified")
            else:
                ljinux.devices["network"][0].disconnect()
                ljinux.devices["network"][0].disconnect_ap()
                dmtex('IWD: Connecting to: "{}"'.format(vr("args")[3]))
                vr("res", ljinux.devices["network"][0].connect(vr("args")[3]))
            exec(vr("wifi_connect_msg"))
            if (
                vr("res")
                and (
                    vr("args")[3] not in cptoml.keys("IWD")
                    or cptoml.fetch(vr("args")[3], subtable="IWD") != vr("passwd")
                )
            ) and vr("passwd") is not None:
                # Store this network
                cptoml.put(vr("args")[3], vr("passwd"), subtable="IWD")
            ljinux.api.setvar("return", str(int(not vr("res"))))
        else:
            term.write("Network not found")
            ljinux.api.setvar("return", "1")
    elif vr("args")[2] == "ap_mode" and vr("argl") > 3:
        if hasattr(ljinux.devices["network"][0], "connect_ap"):
            vr(
                "res",
                ljinux.devices["network"][0].connect_ap(vr("args")[3], vr("passwd")),
            )
            exec(vr("wifi_ap_msg"))
            ljinux.api.setvar("return", str(int(not vr("res"))))
        else:
            dmtex("IWD: This interface does not support AP.")
    elif vr("args")[2] == "auto":
        if not ljinux.devices["network"][0].connected:
            # We don't need to run on an already connected interface
            vr("stored_networks", cptoml.keys("IWD"))
            if len(vr("stored_networks")):
                vr("scanned_networks", ljinux.devices["network"][0].scan())
                vr("best", None)  # The best network to connect to
                vr("best_alt", None)  # An alternative, just in case.
                vr("best_index", None)  # Rating
                vr("best_alt_index", None)  # Rating for alt
                for pv[get_pid()]["i"] in vr("scanned_networks"):
                    if vr("i") in vr("stored_networks"):
                        if vr("best") is None:  # We have no alternative
                            vr("best", vr("i"))
                            vr("best_index", vr("stored_networks").index(vr("i")))
                        else:  # We already have a network we can use
                            vr(
                                "cind", vr("stored_networks").index(vr("i"))
                            )  # To test if it's better
                            if vr("best_index") > vr("cind"):
                                # It's a better network
                                vr("best_alt", vr("best"))
                                vr("best_alt_index", vr("best_index"))
                                vr("best", vr("i"))
                                vr("best_index", vr("cind"))
                            elif vr("best_alt") is None or vr("best_alt_index") > vr(
                                "cind"
                            ):
                                vr("best_alt", vr("i"))
                                vr("best_alt_index", vr("cind"))
                if vr("best") is not None:  # We can connect
                    exec(vr("wifi_best"))
                    if not vr("res"):
                        if vr("best_alt") is not None:
                            vr("best", vr("best_alt"))
                            exec(vr("wifi_best"))
                        else:
                            dmtex(f"IWD: No available alternative networks. ABORT.")
                            vr("best", None)
                if (
                    vr("best") is None
                ):  # We have to create a hotspot based on toml settings.
                    vr("apssid", cptoml.fetch("SSID", subtable="IWD-AP"))
                    vr("appasswd", cptoml.fetch("PASSWD", subtable="IWD-AP"))
                    if vr("apssid") is not None:
                        vr(
                            "res",
                            ljinux.devices["network"][0].connect_ap(
                                vr("apssid"), vr("appasswd")
                            ),
                        )
                        exec(vr("wifi_ap_msg"))
    elif vr("args")[2] == "disconnect":
        ljinux.devices["network"][0].disconnect()
        ljinux.devices["network"][0].disconnect_ap()
        ljinux.api.setvar("return", "0")
    else:
        ljinux.based.error(1)
else:
    ljinux.based.error(1)
