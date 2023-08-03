rename_process("touch")
try:
    with ljinux.api.fopen(ljinux.based.user_vars["argj"].split()[1], "r"):
        ljinux.based.error(10)
except OSError:
    with ljinux.api.fopen(ljinux.based.user_vars["argj"].split()[1], "w") as pv[
        get_pid()
    ]["f"]:
        if pv[get_pid()]["f"] is None:
            ljinux.based.error(7)
