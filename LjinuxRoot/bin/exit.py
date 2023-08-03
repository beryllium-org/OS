rename_process("exit")
term.write("Bye")
if hasattr(term.console, "disconnect"):
    # We are running on a remote shell
    term.console.disconnect()
else:
    pv[0]["Exit"] = True
    try:
        pv[0]["Exit_code"] = int(ljinux.based.user_vars["argj"].split()[1])
    except IndexError:
        pass
