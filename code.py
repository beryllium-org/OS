# -----------------
# Ljinux launcher by bill88t
# Coded on a Raspberry Pi 400
# Ma'am I swear this project is real
# -----------------

#
# this file is used as the launcher for ljinux
# does basic init and holds the ljinux object
#

from sys import exit

try:
    from os import chdir, sync
    from storage import umount
    
    from microcontroller import (
        reset,
        RunMode,
        on_next_reset
    )
    
    from time import sleep
    
except ImportError:
    print("bootloader failure")
    exit(0)
    

def jrub(texx=None): #basic logging for the launcher
    print("jrub> ", texx)

jrub("Basic loading complete")

try:
    from ljinux import ljinux
    jrub("Ljinux basic init done")
except ImportError:
    jrub("Ljinux wanna-be kernel binary not found, cannot continue..") # anon is idot, we not gonna bother
    exit(1)

oss = ljinux()
jrub("Ljinux object init complete") # the init of the basic os structure is done then this runs too

oss.farland.setup()
jrub("Display init complete") # even if no display is attached, this init is necessary
oss.io.init_net()
jrub("Net init complete") # same goes for this, if the objects are not here, the commands will break
if oss.io.network_online:
    jrub("Network up")
    oss.networking.timeset()
    jrub("Time set complete")
else:
    jrub("Network down")

oss.farland.frame()
jrub("Running Ljinux autorun..") # the autorun is basically everything run and managed by ljinux itself
try:
    Exit_code = oss.based.autorun() # when this is done, the shell exited fully and we can pack up if exit code is something reasonable
    jrub("Shell exited with exit code " + str(Exit_code))
except EOFError:
    jrub("\nAlert: Serial Ctrl + D caught, exiting\n")
    Exit_code = 0
oss.io.led.value = False

oss.farland.clear()
jrub("Cleared display")

oss.history.save(ljinux.based.user_vars["history-file"])
jrub("History flushed")

chdir("/")
jrub("Switched to Picofs")

sync()
jrub("Synced all volumes")

oss.io.led.value = True
try:
    oss.io.led.value = False
    umount("/ljinux")
    jrub("Unmounted /ljinux")
    oss.io.led.value = True
except OSError:
    pass
jrub("Reached target: Quit")

oss.io.led.value = False
del oss

def halt():
    while True:
        sleep(3600)

exit_l = {
    241: lambda: (on_next_reset(RunMode.UF2), reset()),
    242: lambda: (on_next_reset(RunMode.SAFE_MODE), reset()),
    243: lambda: (on_next_reset(RunMode.BOOTLOADER), reset()),
    244: lambda: (print("[ OK ] Reached target: Halt"), halt()),
    245: lambda: reset()
}


exit_l[Exit_code]()
