# Initialize wifi and configure background task to auto-connect
be.based.run("modprobe driver_wifi as network")


def _autocon() -> None:
    if not be.devices["network"][0].connected:
        systemprints(2, "Connecting wifi")
        be.based.run(
            "iwctl station wifi auto"
        )  # Configure connections in &/settings.toml
        systemprints(1, "Connecting wifi")
        be.based.run("timesync")
    vr("tm", time.monotonic())


def _checker() -> bool:
    return time.monotonic() - vr("tm") > 10


vr("task", be.api.tasks.add("wifi_scheduler", 30, _checker, _autocon))
pid_activate(vr("task"))  # Now running under the wifi scheduler task
_autocon()
pid_deactivate()  # back to our task
del _checker, _autocon
