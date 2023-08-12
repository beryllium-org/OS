rename_process("exit")
term.write("Bye")
if hasattr(term.console, "disconnect"):
    # We are running on a remote shell
    term.console.disconnect()
else:
    vr("Exit", True, pid=0)
    try:
        vr("Exit_code", int(ljinux.based.user_vars["argj"].split()[1]), pid=0)
    except IndexError:
        pass
