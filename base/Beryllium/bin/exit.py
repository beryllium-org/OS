rename_process("exit")
if hasattr(term.console, "disconnect"):
    # Console can kick
    term.write("Bye")
    term.console.disconnect()
    be.based.run("runparts /etc/hooks/disconnect.d/")
else:
    # Console can't kick

    if hasattr(term.console, "connected"):
        if term.console.connected:
            term.write("You can safely disconnect from the console.")
        while term.console.connected:
            time.sleep(0.1)
            be.based.run("runparts /etc/hooks/disconnect.d/")
    else:
        term.write("You can safely disconnect from the console.")
        while term.detect_size() != False:
            try:
                time.sleep(2)
            except KeyboardInterrupt:
                pass
            be.based.run("runparts /etc/hooks/disconnect.d/")
be.based.command.exec(pv[0]["root"] + "/bin/_waitforconnection.lja")
