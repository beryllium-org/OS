rename_process("iwctl")
ljinux.api.setvar("return", "0")
vr("args", ljinux.based.user_vars["argj"].split()[1:])
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
ljinux.api.setvar("return", str(int(not vr("res"))))
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
    ljinux.devices["network"][0].connect(
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
        ljinux.devices["network"][0].hw_name
        if (
            "network" in ljinux.devices
            and ljinux.devices["network"][0].interface_type == "wifi"
        )
        else None
    ),
)

if vr("argl") is 0:
    ljinux.api.subscript("/bin/iwctl/interactive.py")
else:
    ljinux.api.subscript("/bin/iwctl/headless.py")
