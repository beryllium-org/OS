from sys import exit
from sys import path as syspath
from time import sleep
from microcontroller import reset, RunMode, on_next_reset
from supervisor import reload
from os import chdir, sync

exit_l = {
    0: lambda: (jrub("Exiting"), chdir("/"), exit(0)),
    1: lambda: (jrub("Exiting due to error"), chdir("/"), exit(1)),
    241: lambda: (on_next_reset(RunMode.UF2), reset()),
    242: lambda: (on_next_reset(RunMode.SAFE_MODE), reset()),
    243: lambda: (on_next_reset(RunMode.BOOTLOADER), reset()),
    244: lambda: (chdir("/"), reload()),
    245: lambda: reset(),
}

jrub = lambda text: print(f"jrub> {text}")

syspath.append("/Beryllium/lib")

try:
    from be import be

    jrub("Beryllium init complete")
except ImportError:
    jrub("Beryllium binary not found, cannot continue..")
    exit_l[1]()

oss = be()

jrub("Running Beryllium autorun..")

try:
    Exit_code = oss.based.autorun()
    jrub(f"Program exited with exit code {Exit_code}")
except EOFError:
    jrub("\nAlert: Ctrl + D caught, exiting\n")
    exit_l[0]()
except Exception as err:
    from traceback import print_exception

    print(f"\n\nBeryllium crashed with:\n")
    print_exception(err)
    print()
    del err
    exit_l[1]()

oss.io.ledset(0)  # idle

oss.history.save(oss.based.user_vars["history-file"])
jrub("History flushed")

sync()
jrub("Synced all volumes")
oss.io.ledset(1)

jrub("Reached target: Quit")
oss.io.ledset(0)
del oss

try:
    exit_l[Exit_code]()
except ValueError:
    exit_l[245]()
