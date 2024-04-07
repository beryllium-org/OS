rename_process("Runtasks")

term.write("Running background tasks. Press Ctrl + C to stop.")
while not term.is_interrupted():
    be.api.tasks.run()
