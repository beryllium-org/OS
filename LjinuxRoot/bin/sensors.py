term.write(
    "cpu_thermal\nAdapter: Cpu device\ntemp1: +"
    + str(cpu.temperature)[:5]
    + "°C"
    + ("\nvoltage1: " + str(cpu.voltage) + "v" if cpu.voltage is not None else "")
)
