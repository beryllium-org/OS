if ndc and getmount("/").label == "CIRCUITPY":
    print(
        colors.red_t
        + "\nPlease unplug the microcontroller, and plug it back in to continue."
        + "\nThis is required in order to run the boot code.\n"
        + colors.endc
    )
    global Exit
    global Exit_code
    Exit = True
    Exit_code = 0