rename_process("gpio init")
systemprints(2, "Setting up gpio")
ljinux.based.run("modprobe gpiochip")
systemprints(1, "Setting up gpio")
