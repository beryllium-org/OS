rename_process("iwctl")
be.api.setvar("return", "0")
vr("args", be.based.user_vars["argj"].split()[1:])
vr("argl", len(vr("args")))
vr("pr", False)

vr(
    "wifi_connect_msg",
    """if not vr("res"):
    dmtex("IWD: Connected to network successfully.")
    if vr("pr"):
        term.write("\\nConnected successfully.")
else:
    dmtex("IWD: Connection to network failed.")
    if vr("pr"):
        term.write("\\nConnection failed.")
be.api.setvar("return", str(int(not vr("res"))))
""",
)
try:
    vr("wifi_connect_msg", compile(vr("wifi_connect_msg"), "driver_wifi", "exec"))
except NameError:
    pass

vr(
    "wifi_best",
    """vr(
    "res",
    be.devices["network"][0].connect(
        vr("best"), cptoml.fetch(vr("best"), subtable="IWD")
    ),
)
if vr("res"):
    dmtex(
        "IWD: Connected to network {} successfully.".format(
            vr("best")
        )
    )
else:
    dmtex(
        "IWD: Connection to network {} failed.".format(
            vr("best")
        )
    )
""",
)
try:
    vr("wifi_best", compile(vr("wifi_best"), "driver_wifi", "exec"))
except NameError:
    pass

vr(
    "wifi_ap_msg",
    """if vr("res"):
    dmtex("IWD: AP started successfully.")
    if vr("pr"):
        term.write("\\nIWD: AP started successfully.")
else:
    dmtex("IWD: AP creation failed.")
    if vr("pr"):
        term.write("\\nIWD: AP creation failed.")
""",
)
try:
    vr("wifi_ap_msg", compile(vr("wifi_ap_msg"), "driver_wifi", "exec"))
except NameError:
    pass


vr(
    "device_n",
    (
        be.devices["network"][0].hw_name
        if (
            "network" in be.devices
            and be.devices["network"][0].interface_type == "wifi"
        )
        else None
    ),
)

if vr("argl") is 0:
    be.api.subscript("/bin/iwctl/interactive.py")
else:
    be.api.subscript("/bin/iwctl/headless.py")
