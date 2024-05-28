from os import uname, system, environ, path, listdir
from time import sleep

running_under_spyware = "WSL2" in uname().machine

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
        + "Where D is the CIRCUITPY drive letter.\n"
        + "Here have a shell, exit when you're done.\n"
    )
    while True:
        system("bash")
        print("Alright, now whats the mount path (/mnt/D)?")
        bpath = input("> ")
        try:
            if path.exists(bpath) and "boot_out.txt" in listdir(bpath):
                break
        except:
            pass
        print("Path invalid.")
    with open("/tmp/CUSTOMBOARDPATH", "w") as f:
        f.write(path if len(path) else "/mnt/D")
    print("Running the rest of the installation in 3 seconds..\n" + "")
    sleep(3)
