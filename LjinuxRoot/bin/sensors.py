rename_process("sensors")
vr("no", True)
if cpu.temperature is not None:
    vr("no", False)
    term.write(
        "cpu_thermal\nAdapter: Cpu device\ntemp1: +" + str(cpu.temperature)[:5] + "°C"
    )

if cpu.voltage is not None:
    vr("no", False)
    term.write("voltage1: " + str(cpu.voltage) + "V")

if vr("no"):
    term.write("No sensors detected!")
