if hasattr(term.console, "disconnect"):
    term.console.disconnect()
elif term._active == False:  # Can be None
    # We want to disconnect from a passive console.
    ljinux.based.command.exec("/LjinuxRoot/bin/_waitforconnection.lja")
    term.clear_line()
else:
    term.write("This console does not support disconnection.")
