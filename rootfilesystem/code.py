from sys import exit
from time import sleep

jrub = lambda text: print(f"jrub> {text}")

try:
    from ljinux import ljinux

    # if you touch this line or line 14 ever again, I will break your legs
    jrub("Ljinux basic init done")
except ImportError:
    jrub("Ljinux wanna-be kernel binary not found, cannot continue..")
    exit(1)

oss = ljinux()

jrub("Ljinux object init complete")

oss.farland.setup()

jrub("Display init complete")

oss.io.init_net()

jrub("Net init complete")

if oss.io.network_online:
    jrub("Network up")
    oss.networking.timeset()
    jrub("Time set complete")
else:
    jrub("Network down")

oss.farland.frame()

jrub("Running Ljinux autorun..")

try:
    Exit_code = oss.based.autorun()
    jrub(f"Shell exited with exit code {Exit_code}")

except EOFError:
    jrub("\nAlert: Serial Ctrl + D caught, exiting\n")
    exit_l[0]()

except Exception as err:
    print(f"\n\nLjinux crashed with:\n\t{str(type(err))[8:-2]}: {str(err)}")
    del err
    exit_l[1]()

oss.io.ledset(0)  # idle

oss.farland.clear()
jrub("Cleared display")

oss.history.save(oss.based.user_vars["history-file"])
jrub("History flushed")

from os import chdir, sync

chdir("/")
jrub("Switched to Picofs")

sync()
jrub("Synced all volumes")

oss.io.led.value = True
try:
    oss.io.led.value = False
    from storage import umount

    umount("/ljinux")
    jrub("Unmounted /ljinux")
    oss.io.led.value = True

except OSError:
    jrub("Could not unmount /ljinux")

jrub("Reached target: Quit")
oss.io.led.value = False
del oss

from microcontroller import reset, RunMode, on_next_reset

exit_l = {
    0: lambda: (jrub("Exiting"), exit(0)),
    1: lambda: (jrub("Exiting due to error"), exit(1)),
    241: lambda: (on_next_reset(RunMode.UF2), reset()),
    242: lambda: (on_next_reset(RunMode.SAFE_MODE), reset()),
    243: lambda: (on_next_reset(RunMode.BOOTLOADER), reset()),
    244: lambda: (jrub("Reached target: Halt"), sleep(36000)),
    245: lambda: reset(),
}

exit_l[Exit_code]()
exit(Exit_code)
