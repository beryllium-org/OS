from os import remove

try:
    remove("/tmp/CUSTOMBOARDPATH")
    print(
        "Remember to umount from inside of WSL too..\n\n"
        + "    sudo umount /mnt/D\n"
        + "    sudo rmdir /mnt/D"
    )
except FileNotFoundError:
    pass
