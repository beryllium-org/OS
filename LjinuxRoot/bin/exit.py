global Exit
global Exit_code
term.write("Bye")
if hasattr(term.console, "disconnect"):
    # We are running on a remote shell
    term.console.disconnect()
else:
    Exit = True
    try:
        Exit_code = int(ljinux.based.user_vars["argj"].split()[1])
    except IndexError:
        pass
