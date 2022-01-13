# -----------------
# Ljinux launcher by bill88t
# Coded on a Raspberry Pi 400
# Ma'am I swear this project is real
# -----------------

import os
import storage
import microcontroller
import time
import sys
def jrub(texx=None):
    print("jrub> ", texx)
jrub("Basic loading complete")
from ljinux import ljinux
jrub("Ljinux basic init done")
oss = ljinux()
jrub("Ljinux object init complete")
oss.farland.setup()
jrub("Display init complete")
oss.io.init_net()
jrub("Net init complete")
if oss.io.network_online:
    jrub("Network up")
else:
    jrub("Network down")
oss.farland.frame()
jrub("Running Ljinux autorun..")
time.sleep(.4)
try:
    Exit_code = oss.based.autorun()
    jrub("Shell exited with exit code " + str(Exit_code))
except EOFError:
    jrub("\nAlert: Serial Ctrl + D caught, exiting\n")
    Exit_code = 0
oss.io.led.value = False
oss.farland.clear()
jrub("Cleared display")
oss.history.save(ljinux.based.user_vars["history-file"])
jrub("History flushed")
os.chdir("/")
jrub("Switched to Picofs")
os.sync()
jrub("Synced all volumes")
oss.io.led.value = True
try:
    oss.io.led.value = False
    storage.umount("/ljinux")
    jrub("Unmounted /ljinux")
    oss.io.led.value = True
except OSError:
    pass
jrub("Reached target: Quit")
oss.io.led.value = False
if (Exit_code == 245):
    microcontroller.reset()
elif (Exit_code == 244):
    print("[ OK ] Reached target: Halt")
    while True:
        time.sleep(3600)
else:
    sys.exit(Exit_code)
