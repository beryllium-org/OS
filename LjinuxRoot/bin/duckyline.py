try:
    tmpp = ljinux.based.user_vars["argj"].split()[1:]
    lineee = ""
    for i in tmpp:
        lineee += i + " "
    del tmpp
    lineee = lineee[:-1]
    from usb_hid import devices
    from adafruit_hid.keyboard import Keyboard
    from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
    from adafruit_hid.keycode import Keycode
    from time import sleep
    from sys import modules

    duckyCommands = {
        "WINDOWS": Keycode.WINDOWS,
        "GUI": Keycode.GUI,
        "APP": Keycode.APPLICATION,
        "MENU": Keycode.APPLICATION,
        "SHIFT": Keycode.SHIFT,
        "ALT": Keycode.ALT,
        "CONTROL": Keycode.CONTROL,
        "CTRL": Keycode.CONTROL,
        "DOWNARROW": Keycode.DOWN_ARROW,
        "DOWN": Keycode.DOWN_ARROW,
        "LEFTARROW": Keycode.LEFT_ARROW,
        "LEFT": Keycode.LEFT_ARROW,
        "RIGHTARROW": Keycode.RIGHT_ARROW,
        "RIGHT": Keycode.RIGHT_ARROW,
        "UPARROW": Keycode.UP_ARROW,
        "UP": Keycode.UP_ARROW,
        "BREAK": Keycode.PAUSE,
        "PAUSE": Keycode.PAUSE,
        "CAPSLOCK": Keycode.CAPS_LOCK,
        "DELETE": Keycode.DELETE,
        "END": Keycode.END,
        "ESC": Keycode.ESCAPE,
        "ESCAPE": Keycode.ESCAPE,
        "HOME": Keycode.HOME,
        "INSERT": Keycode.INSERT,
        "NUMLOCK": Keycode.KEYPAD_NUMLOCK,
        "PAGEUP": Keycode.PAGE_UP,
        "PAGEDOWN": Keycode.PAGE_DOWN,
        "PRINTSCREEN": Keycode.PRINT_SCREEN,
        "ENTER": Keycode.ENTER,
        "SCROLLLOCK": Keycode.SCROLL_LOCK,
        "SPACE": Keycode.SPACE,
        "TAB": Keycode.TAB,
        "BACKSPACE": Keycode.BACKSPACE,
        "F1": Keycode.F1,
        "F2": Keycode.F2,
        "F3": Keycode.F3,
        "F4": Keycode.F4,
        "F5": Keycode.F5,
        "F6": Keycode.F6,
        "F7": Keycode.F7,
        "F8": Keycode.F8,
        "F9": Keycode.F9,
        "F10": Keycode.F10,
        "F11": Keycode.F11,
        "F12": Keycode.F12,
        "A": Keycode.A,
        "B": Keycode.B,
        "C": Keycode.C,
        "D": Keycode.D,
        "E": Keycode.E,
        "F": Keycode.F,
        "G": Keycode.G,
        "H": Keycode.H,
        "I": Keycode.I,
        "J": Keycode.J,
        "K": Keycode.K,
        "L": Keycode.L,
        "M": Keycode.M,
        "N": Keycode.N,
        "O": Keycode.O,
        "P": Keycode.P,
        "Q": Keycode.Q,
        "R": Keycode.R,
        "S": Keycode.S,
        "T": Keycode.T,
        "U": Keycode.U,
        "V": Keycode.V,
        "W": Keycode.W,
        "X": Keycode.X,
        "Y": Keycode.Y,
        "Z": Keycode.Z,
        "a": Keycode.A,
        "b": Keycode.B,
        "c": Keycode.C,
        "d": Keycode.D,
        "e": Keycode.E,
        "f": Keycode.F,
        "g": Keycode.G,
        "h": Keycode.H,
        "i": Keycode.I,
        "j": Keycode.J,
        "k": Keycode.K,
        "l": Keycode.L,
        "m": Keycode.M,
        "n": Keycode.N,
        "o": Keycode.O,
        "p": Keycode.P,
        "q": Keycode.Q,
        "r": Keycode.R,
        "s": Keycode.S,
        "t": Keycode.T,
        "u": Keycode.U,
        "v": Keycode.V,
        "w": Keycode.W,
        "x": Keycode.X,
        "y": Keycode.Y,
        "z": Keycode.Z,
        "0": Keycode.ZERO,
        "1": Keycode.ONE,
        "2": Keycode.TWO,
        "3": Keycode.THREE,
        "4": Keycode.FOUR,
        "5": Keycode.FIVE,
        "6": Keycode.SIX,
        "7": Keycode.SEVEN,
        "8": Keycode.EIGHT,
        "9": Keycode.NINE,
    }

    kbd = Keyboard(devices)
    del devices
    layout = KeyboardLayoutUS(kbd)
    defaultDelay = 60

    ljinux.based.user_vars["return"] = "0"
    cmd = (
        lineee[: lineee.find(" ", 0)].upper()
        if lineee.find(" ", 0) != -1
        else lineee.upper()
    )
    args = lineee[lineee.find(" ", 0) + 1 :]
    del lineee
    if cmd == "STRING":
        layout.write(args)
    elif cmd in duckyCommands:
        stack = [cmd] + args.split()
        for i in stack:
            if i.upper() in duckyCommands:
                kbd.press(duckyCommands[i.upper()])
            else:
                print(f'Error: Key "{i}" not found')
                ljinux.based.user_vars["return"] = "1"
                break
        del stack
        kbd.release_all()
    else:
        print(f'Error: Command "{cmd}" not found')
        ljinux.based.user_vars["return"] = "1"

    del cmd, args
    del duckyCommands, kbd, layout
    del KeyboardLayoutUS, Keycode, defaultDelay

except IndexError:
    ljinux.based.error(1)
