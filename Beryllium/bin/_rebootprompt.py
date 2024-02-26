if getmount("/").label == "CIRCUITPY":
    term.write(
        colors.red_t
        + "\nPlease unplug the microcontroller, and plug it back in to continue."
        + "\nThis is required in order to run the boot code.\n"
        + colors.endc
    )
    vr("Exit", True, pid=0)
    vr("Exit_code", 0, pid=0)
