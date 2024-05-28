from os import uname, system, environ
from time import sleep

running_under_spyware = "WSL2" in uname().machine

if running_under_spyware or 1:
    print(
        "Ew WSL.\n"
        + "Well, I am not going to touch this, mount the board yourself.\n"
        + "This is commonly done by running:\n\n"
        + "    sudo mkdir /mnt/D\n"
        + "    sudo mount -t drvfs D: /mnt/D\n\n"
        + "Where D is the CIRCUITPY drive letter.\n"
        + "Here have a shell, exit when you're done.\n"
    )
    system("bash")
    print("Alright, now whats the mount path (/mnt/D)?")
    path = input("> ")
    print("Running the rest of the installation in 3 seconds..\n" + "")
    with open("/tmp/CUSTOMBOARDPATH", "w") as f:
        f.write(path)
    sleep(3)
