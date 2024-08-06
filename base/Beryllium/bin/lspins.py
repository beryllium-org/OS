rename_process("lspins")
for pv[get_pid()]["i"] in range(len(be.devices["gpiochip"])):
    term.write("gpiochip" + str(vr("i")) + ":")
    vr("cpins", be.devices["gpiochip"][vr("i")].pins)
    for pv[get_pid()]["j"] in vr("cpins"):
        term.write(" " * 4 + vr("j"))
be.api.setvar("return", "0")
