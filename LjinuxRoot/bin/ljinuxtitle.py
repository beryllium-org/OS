temp = (
    "a "
    + ljinux.based.system_vars["USER"]
    + "@"
    + ljinux.based.system_vars["HOSTNAME"]
    + ": "
    + ljinux.based.fn.betterpath()
)
ljinux.based.user_vars["argj"] = temp
ljinux.based.command.fpexecc([None, "/bin/title.py"])
del temp
