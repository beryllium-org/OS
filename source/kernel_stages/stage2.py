# Allocate kernel task
launch_process("kernel", "root", True)  # pid will always be 0
vr("Version", "0.5.0")

vr("dmesg", [])
vr("access_log", [])
vr("consoles", {})
vr("console_active", None)
vr("ndmesg", False)  # disable dmesg for ram
# run _ndmesg from the shell to properly trigger it
vr("root", "/Beryllium")
vr("mounts", {0: "/"})

# Core board libs
try:
    import gc

    gc.enable()

    from sys import implementation, platform, modules, exit

    import busio
    from microcontroller import cpu
    from storage import remount, VfsFat, mount, getmount
    from os import chdir, rmdir, mkdir, sync, getcwd, listdir, remove, sync, stat
    from math import trunc
    import time

    from jcurses import jcurses
    import cptoml
    from lj_colours import lJ_Colours as colors
    from traceback import format_exception
except ImportError:
    print("FATAL: Core libraries loading failed")

    from sys import exit

    exit(1)

global console
try:
    from usb_cdc import console

    pv[0]["consoles"]["ttyUSB0"] = console
    vr("console_active", "ttyUSB0")
except ImportError:
    try:
        global virtUART
        from virtUART import virtUART

        console = virtUART()
        pv[0]["consoles"]["ttyUART0"] = console
        vr("console_active", "ttyUART0")
    except ImportError:
        from sys import exit

        exit(1)

print("[    0.00000] Core modules loaded")
pv[0]["dmesg"].append("[    0.00000] Core modules loaded")

vr("digitalio_store", {})

# Exit code holder, has to be global for everyone to be able to see it.
vr("Exit", False)
vr("Exit_code", 0)

# Hardware autodetect vars, starts assuming everything is missing
vr("sdcard_fs", False)

vr("uptimee", -time.monotonic())
# using uptimee as an offset, this way uptime + time.monotonic = 0 at this very moment and it goes + from here on out
print("[    0.00000] Timings reset")
pv[0]["dmesg"].append("[    0.00000] Timings reset")

# dmtex previous end holder
pv[0]["oend"] = "\n"  # needed to mask print

# Script break to replace python break statement
pv[0]["Break"] = False

try:
    term = jcurses()  # the main curses entity, used primarily for based.shell()
    term.hold_stdout = True  # set it to buffered by default
    term.console = console
    term.nwrite(colors.reset_s_format)
    print("[    0.00000] Jcurses init complete")
    pv[0]["dmesg"].append("[    0.00000] Jcurses init complete")
except ImportError:
    print("FATAL: FAILED TO INIT JCURSES")
    exit(0)


def dmtex(
    texx: str = None, end: str = "\n", timing: bool = True, force: bool = False
) -> None:
    # Persistent offset, Print "end=" preserver

    # current time since kernel start rounded to 5 digits
    ct = "%.5f" % (pv[0]["uptimee"] + time.monotonic())

    # used to disable the time print
    strr = "[{}{}] {}".format((11 - len(ct)) * " ", str(ct), texx) if timing else texx

    if (not term.dmtex_suppress) or force:
        term.write(strr, end=end)  # using the provided end

    """
    if the oend of the last print is a newline we add a new entry
    otherwise we go to the last one and we add it along with the old oend
    """

    if not pv[0]["ndmesg"]:
        if "\n" == pv[0]["oend"]:
            pv[0]["dmesg"].append(strr)
        elif (len(pv[0]["oend"].replace("\n", "")) > 0) and (
            "\n" in pv[0]["oend"]
        ):  # there is hanging text in old oend
            pv[0]["dmesg"][-1] += pv[0]["oend"].replace("\n", "")
            pv[0]["dmesg"].append(strr)
        else:
            pv[0]["dmesg"][-1] += pv[0]["oend"] + strr
        pv[0]["oend"] = end  # oend for next


# From now on use dmtex
dmtex("Dmesg ready")

use_compiler = False
try:
    compile("", "", "exec")

    use_compiler = True
    dmtex("Kernel compiler enabled")
except NameError:
    dmtex("Kernel compiler disabled")

try:
    from neopixel_write import neopixel_write
except ImportError:
    pass  # no big deal, this just isn't a neopixel board

# Board specific configurations
defaultoptions = {  # default configuration, in line with the manual (default value, type, allocates pin bool)
    "led": ("LED", str),
    "ledtype": ("generic", str),
    "serial_console_enabled": (True, bool),
    "usb_msc_available": (False, bool),
    "usb_hid_available": (False, bool),
    "usb_midi_available": (False, bool),
    "wifi_available": (False, bool),
    "ble_available": (False, bool),
    "blc_available": (False, bool),
    "usb_msc_enabled": (False, bool),
    "usb_hid_enabled": (False, bool),
    "usb_midi_enabled": (False, bool),
    "fs_label": ("BERYLLIUM", str),
    "DEBUG": (False, bool),
}

# General options
dmtex("Options loaded:")
for optt in list(defaultoptions.keys()):
    optt_dt = cptoml.fetch(optt, "BERYLLIUM")
    try:
        if isinstance(optt_dt, defaultoptions[optt][1]):
            dmtex(
                "\t"
                + colors.green_t
                + "√"
                + colors.endc
                + " "
                + optt
                + "="
                + str(optt_dt),
                timing=False,
            )
        else:
            raise KeyError
    except KeyError:
        try:
            remount("/", False)
            optt_dt = defaultoptions[optt][0]
            cptoml.put(optt, optt_dt, "BERYLLIUM")
            dmtex(
                colors.green_t + "Updated: " + colors.endc + optt + "=" + str(optt_dt),
                timing=False,
            )
            remount("/", True)
        except RuntimeError:
            dmtex("Could not update /settings.toml, usb access is enabled.")
            term.hold_stdout = True  # set it to buffered by default
            term.flush_writes()
            exit(0)
    del optt, optt_dt

del defaultoptions
gc.collect()
gc.collect()

dmtex(f"Board memory: " + str(gc.mem_alloc() + gc.mem_free()) + " bytes")
dmtex(f"Memory free: " + str(gc.mem_free()) + " bytes")


def systemprints(mod: int, tx1: str, tx2: str = None) -> None:
    dmtex(colors.white_t + "[ " + colors.endc, timing=False, end="")

    mods = {
        1: lambda: dmtex(colors.green_t + "OK", timing=False, end=""),
        2: lambda: dmtex(colors.magenta_t + "..", timing=False, end=""),
        3: lambda: dmtex(colors.red_t + "FAILED", timing=False, end=""),
        4: lambda: dmtex(colors.red_t + "EMERG", timing=False, end=""),
        5: lambda: dmtex(colors.white_t + "SKIP", timing=False, end=""),
    }
    mods[mod]()
    dmtex(colors.white_t + " ] " + colors.endc + tx1, timing=False)
    if tx2 is not None:
        dmtex("    -> ", timing=False, end="")
        dmtex(tx2, timing=False)
