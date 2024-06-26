from os import uname, system, environ, path, listdir

running_under_spyware = "WSL2" in uname().release

board_set = False
try:
    environ["BOARD"]
    board_set = True
except KeyError:
    pass

if running_under_spyware and not board_set:
    print(
        "Ew WSL.\n"
        + "Well, I am not going to touch this, mount the board yourself.\n"
        + "This is commonly done by running:\n\n"
        + "    sudo mkdir /mnt/D\n"
        + "    sudo mount -t drvfs D: /mnt/D\n\n"
        + 'With "D" is the CIRCUITPY drive letter.\n'
        + "Here have a shell.\n"
    )
    while True:
        print("(The program is still running, exit this shell to continue)")
        system("bash")
        print("Alright, now whats the mount path (/mnt/D)?")
        bpath = input("> ")
        if not len(bpath):
            bpath = "/mnt/D"
        try:
            if path.exists(bpath) and "boot_out.txt" in listdir(bpath):
                break
        except:
            pass
        print("Path invalid.")
    with open("/tmp/CUSTOMBOARDPATH", "w") as f:
        f.write(bpath)
    print("Board path valid!\nRunning installation..\n")
