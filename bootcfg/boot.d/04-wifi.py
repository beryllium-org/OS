# Initialize wifi and configure background task to auto-connect
be.based.run("modprobe driver_wifi as network")
be.based.run("iwctl station wifi disconnect")


def _autocon() -> None:
    if not (
        be.devices["network"][0].connected or be.devices["network"][0].ap_connected
    ):
        systemprints(2, "Connecting wifi")
        be.based.run(
            "iwctl station wifi auto"
        )  # Configure connections in &/settings.toml
        systemprints(1, "Connecting wifi")
        be.based.run("timesync")
        if "ttyTELNET0" in pv[0]["consoles"]:
            be.based.run("telnet deinit")
            be.based.run("telnet setup -q")
    vr("tm", time.monotonic())


def _checker() -> bool:
    return time.monotonic() - vr("tm") > 10


vr("task", be.api.tasks.add("wifi_scheduler", 30, _checker, _autocon))
pid_activate(vr("task"))  # Now running under the wifi scheduler task
_autocon()
pid_deactivate()  # back to our task
del _checker, _autocon
