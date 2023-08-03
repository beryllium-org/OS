ljinux.api.setvar(
    "argj",
    (
        "a "
        + ljinux.based.system_vars["USER"]
        + "@"
        + ljinux.based.system_vars["HOSTNAME"]
        + ": "
        + ljinux.api.betterpath()
    ),
)
ljinux.based.command.fpexec("/bin/title.py")
