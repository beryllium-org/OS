from os import remove

try:
    remove("/tmp/CUSTOMBOARDPATH")
except FileNotFoundError:
    pass
