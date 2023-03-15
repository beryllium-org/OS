# -----------------
#      Ljinux
# Coded on a Raspberry Pi 400
# "It's all bloat" - Mariospapaz 2022
# -----------------

Version = "0.3.6-dev"
Circuitpython_supported = [(8, 0), (8, 1)]
dmesg = []
ndmesg = False  # disable dmesg for ram
access_log = []

# Core board libs
try:
    import gc

    gc.enable()
    usable_ram = gc.mem_alloc() + gc.mem_free()

    import board
    import digitalio
except ImportError:
    print("FATAL: Core libraries loading failed")

    from sys import exit

    exit(1)

print("[    0.00000] Core libs loaded")
dmesg.append("[    0.00000] Core libs loaded")

# Pin allocation tables
pin_alloc = set()
gpio_alloc = {}

# Default password, aka the password if no /etc/passwd is found
dfpasswd = "Ljinux"

# Exit code holder, has to be global for everyone to be able to see it.
Exit = False
Exit_code = 0

# Hardware autodetect vars, starts assuming everything is missing
sdcard_fs = False
print("[    0.00000] Sys vars loaded")
dmesg.append("[    0.00000] Sys vars loaded")

import time

print("[    0.00000] Timing libraries done")
dmesg.append("[    0.00000] Timing libraries done")
uptimee = (
    -time.monotonic()
)  # using uptimee as an offset, this way uptime + time.monotonic = 0 at this very moment and it goes + from here on out
print("[    0.00000] Timings reset")
dmesg.append("[    0.00000] Timings reset")

# dmtex previous end holder
oend = "\n"  # needed to mask print

try:
    from jcurses import jcurses

    term = jcurses()  # the main curses entity, used primarily for based.shell()
    term.hold_stdout = True  # set it to buffered by default
    print("[    0.00000] Loaded jcurses")
    dmesg.append("[    0.00000] Loaded jcurses")
except ImportError:
    print("FATAL: FAILED TO LOAD JCURSES")
    exit(0)


def dmtex(texx=None, end="\n", timing=True, force=False):
    # Persistent offset, Print "end=" preserver

    # current time since ljinux start rounded to 5 digits
    ct = "%.5f" % (uptimee + time.monotonic())

    # used to disable the time print
    strr = "[{}{}] {}".format((11 - len(ct)) * " ", str(ct), texx) if timing else texx

    if (not term.dmtex_suppress) or force:
        term.write(strr, end=end)  # using the provided end

    global oend
    """
    if the oend of the last print is a newline we add a new entry
    otherwise we go to the last one and we add it along with the old oend
    """

    if not ndmesg:
        if "\n" == oend:
            dmesg.append(strr)
        elif (len(oend.replace("\n", "")) > 0) and (
            "\n" in oend
        ):  # there is hanging text in old oend
            dmesg[-1] += oend.replace("\n", "")
            dmesg.append(strr)
        else:
            dmesg[-1] += oend + strr
        oend = end  # oend for next

    del ct, strr


# From now on use dmtex
dmtex("Dmesg ready")

try:
    from sys import (
        implementation,
        platform,
        modules,
        exit,
        stdout,
    )

    import busio

    from microcontroller import cpu

    from storage import remount, VfsFat, mount, getmount

    from os import chdir, rmdir, mkdir, sync, getcwd, listdir, remove, sync

    from io import StringIO
    from usb_cdc import console
    from getpass import getpass
    import json
    from traceback import print_exception
    from math import trunc

    dmtex("System libraries loaded")
except ImportError:
    dmtex("FATAL: SYSTEM LIBRARIES LOAD FAILED")
    exit(0)

try:
    from neopixel_write import neopixel_write
except ImportError:
    pass  # no big deal, this just isn't a neopixel board

try:
    from lj_colours import lJ_Colours as colors

    term.write(colors.reset_s_format, end="")
    dmtex("Loaded lj_colours")
except ImportError:
    dmtex(f"{colors.error}FATAL:{colors.endc} FAILED TO LOAD LJ_COLOURS")
    dmtex(
        "If you intented to disable colors, just rename lj_colours_placebo -> lj_colours"
    )
    exit(0)

# Board specific configurations
try:
    with open("/config.json") as config_file:
        dmtex("Loaded /config.json")
        configg = json.load(config_file)
        del config_file

    for i in configg:
        if i.startswith("_"):
            del configg[i]
        del i

except (ValueError, OSError):
    configg = {}
    dmtex("Kernel config could not be found / parsed, applying defaults")

dmtex("Options applied:")

defaultoptions = {  # default configuration, in line with the manual (default value, type, allocates pin bool)
    "led": (0, int, True),
    "ledtype": ("generic", str, False),
    "SKIPCP": (False, bool, False),
    "DEBUG": (False, bool, False),
    "sd_SCLK": (-1, int, True),
    "sd_SCSn": (-1, int, True),
    "sd_MISO": (-1, int, True),
    "sd_MOSI": (-1, int, True),
}

# pintab
try:
    from pintab import pintab
except:
    dmtex(
        f"{colors.error}ERROR:{colors.endc} Board pintab cannot be loaded!\n\nCannot continue."
    )
    exit(1)

# General options
for optt in list(defaultoptions.keys()):
    try:
        if isinstance(configg[optt], defaultoptions[optt][1]):
            dmtex(
                "\t"
                + colors.green_t
                + "√"
                + colors.endc
                + " "
                + optt
                + "="
                + str(configg[optt]),
                timing=False,
            )
        else:
            raise KeyError
    except KeyError:
        configg.update({optt: defaultoptions[optt][0]})
        dmtex(
            f'Missing / Invalid value for "{optt}" applied: {configg[optt]}',
            timing=False,
        )
    if defaultoptions[optt][2]:
        pin = configg[optt]
        if pin in pin_alloc:
            dmtex("PIN ALLOCATED, EXITING")
            exit(0)
        elif pin == -1:
            pass
        else:
            pin_alloc.add(pin)
        del pin

dmtex("Total pin alloc: ", end="")
for pin in pin_alloc:
    dmtex(str(pin), timing=False, end=" ")
dmtex("", timing=False)

if configg["led"] == -1:
    boardLED = board.LED
else:
    boardLED = pintab[configg["led"]]

del defaultoptions

# basic checks
if not configg["SKIPCP"]:  # beta testing
    good = False
    for i in Circuitpython_supported:
        if implementation.version[:2] == i:
            good = True
            del i
            break
        del i
    if good:
        dmtex("Running on supported implementation")
    else:
        dmtex(
            "-" * 42
            + "\n"
            + " " * 14
            + "WARNING: Unsupported CircuitPython version\n"
            + " " * 14
            + "-" * 42
        )
        for i in range(10, 0):
            term.write(
                f"WARNING: Unsupported CircuitPython version (Continuing in {i})"
            )
            time.sleep(1)
            del i
    del good
else:
    term.write("Skipped CircuitPython version checking, happy beta testing!")

dmtex((f"Board memory: {usable_ram} bytes"))
dmtex((f"Memory free: {gc.mem_free()} bytes"))
dmtex("Basic checks done")

# audio
NoAudio = False  # used to ensure audio will NOT be used in case of libs missing
try:
    from audiomp3 import MP3Decoder
    from audiopwmio import PWMAudioOut
    from audiocore import WaveFile

    dmtex("Audio libraries loaded")
except ImportError:
    NoAudio = True
    dmtex(colors.error + "Notice: " + colors.endc + "Audio libraries loading failed")

# sd card
try:
    import adafruit_sdcard

    dmtex("TFcard libraries loaded")
except ImportError:
    dmtex(colors.error + "Notice: " + colors.endc + "TFcard libraries loading failed")

dmtex("Imports complete")


def systemprints(mod, tx1, tx2=None):
    dmtex("[ ", timing=False, end="")

    mods = {
        1: lambda: dmtex(colors.green_t + "OK", timing=False, end=""),
        2: lambda: dmtex(colors.magenta_t + "..", timing=False, end=""),
        3: lambda: dmtex(colors.red_t + "FAILED", timing=False, end=""),
        4: lambda: dmtex(colors.red_t + "EMERG", timing=False, end=""),
    }
    mods[mod]()
    dmtex(colors.endc + " ] " + tx1, timing=False)
    if tx2 is not None:
        dmtex("           -> " if mod is 3 else "       -> ", timing=False, end="")
        dmtex(tx2, timing=False)


dmtex("Additional loading done")


class ljinux:
    modules = dict()

    class api:
        def remove_ansi(text):
            result = ""
            i = 0
            while i < len(text):
                if text[i : i + 2] == "\033[":  # Skip
                    while i < len(text) and text[i] != "m":
                        i += 1
                    i += 1
                else:
                    result += text[i]
                    i += 1
            del i, text
            return result

        def getvar(var):
            """
            Get a ljinux user variable without mem leaks
            """
            if var in ljinux.based.user_vars.keys():
                return ljinux.based.user_vars[var]
            elif var in ljinux.based.system_vars.keys():
                return ljinux.based.system_vars[var]
            del var

        def setvar(var, data=None, system=False):
            """
            Set a ljinux user variable without mem leaks
            No handbreak installed.
            data=None deletes
            """
            if not system:
                if var in ljinux.based.user_vars.keys():
                    del ljinux.based.user_vars[var]
                if data is not None:
                    ljinux.based.user_vars.update({var: data})
            else:
                if var in ljinux.based.system_vars.keys():
                    del ljinux.based.system_vars[var]
                if data is not None:
                    ljinux.based.system_vars.update({var: data})
            del var, data, system

        def xarg(rinpt=None, fn=False):
            """
            Proper argument parsing for ljinux.
            Send your input stream to here and you will receive a dict in return

            The return dict contains these items:
                "w" for the words that don't belong to a specific option.
                    Example: "ls /bin", "/bin" is gonna be returned in "w"
                "hw" for the words, that were hidden due to an option.
                    Example "ls -a /bin", "/bin" is not gonna be in "w"
                    as it is a part of "o" but will be in "hw".
                "o" for all the options, with their respective values.
                    Example: "ls -a /bin", {"a": "/bin"} is gonna be in "o"
                "n" if False is passed to fn, contains the filename

            Variables automatically converted to their values.
            GPIO variables unaffected.
            """

            if rinpt is None:
                rinpt = ljinux.based.user_vars["argj"]

            inpt = rinpt.split(" ")
            del rinpt

            options = dict()
            words = list()
            hidwords = list()

            n = False  # in keyword
            s = False  # in string
            temp_s = None  # temporary string
            entry = None  # keyword

            r = 0 if fn else 1
            del fn

            for i in range(r, len(inpt)):
                if inpt[i].startswith("$"):  # variable
                    if not s:
                        inpt[i] = ljinux.api.adv_input(inpt[i][1:])
                    elif inpt[i].endswith('"'):
                        temp_s += ljinux.api.adv_input(inpt[i][:-1])
                        words.append(temp_s)
                        s = False
                    elif '"' not in inpt[i]:
                        temp_s += " " + ljinux.api.adv_input(inpt[i][1:])
                        continue
                    else:
                        temp_s += " " + ljinux.api.adv_input(
                            inpt[i][1 : inpt[i].find('"')]
                        )
                        words.append(temp_s)
                        s = False
                        inpt[i] = inpt[i][inpt[i].find('"') + 1 :]
                elif (not s) and inpt[i].startswith('"$'):
                    if inpt[i].endswith('"'):
                        inpt[i] = ljinux.api.adv_input(inpt[i][2:-1])
                    else:
                        temp_s = ljinux.api.adv_input(inpt[i][2:])
                        s = True
                        continue
                if not n:
                    if (not s) and inpt[i].startswith("-"):
                        if inpt[i].startswith("--"):
                            entry = inpt[i][2:]
                        else:
                            entry = inpt[i][1:]
                        n = True
                    elif (not s) and inpt[i].startswith('"'):
                        if not inpt[i].endswith('"'):
                            temp_s = inpt[i][1:]
                            s = True
                        else:
                            words.append(inpt[i][1:-1])
                    elif s:
                        if inpt[i].endswith('"'):
                            temp_s += " " + inpt[i][:-1]
                            words.append(temp_s)
                            s = False
                        else:
                            temp_s += " " + inpt[i]
                    else:
                        words.append(inpt[i])
                else:  # in keyword
                    if (not s) and inpt[i].startswith('"'):
                        if not inpt[i].endswith('"'):
                            temp_s = inpt[i][1:]
                            s = True
                        else:
                            options.update({entry: inpt[i][1:-1]})
                            hidwords.append(inpt[i][1:-1])
                            n = False
                    elif s:
                        if inpt[i].endswith('"'):
                            temp_s += " " + inpt[i][:-1]
                            options.update({entry: temp_s})
                            hidwords.append(temp_s)
                            n = False
                            s = False
                        else:
                            temp_s += " " + inpt[i]
                    elif inpt[i].startswith("-"):
                        options.update({entry: None})  # no option for the previous one
                        if inpt[i].startswith("--"):
                            entry = inpt[i][2:]
                        else:
                            entry = inpt[i][1:]
                        # leaving n = True
                    else:
                        options.update({entry: inpt[i]})
                        hidwords.append(inpt[i])
                        n = False
            if n:  # we have incomplete keyword
                # not gonna bother if s is True
                options.update({entry: None})

            del n, entry, s, temp_s

            argd = {
                "w": words,
                "hw": hidwords,
                "o": options,
            }

            if r is 1:  # add the filename
                argd.update({"n": inpt[0]})
            del options, words, hidwords, inpt, r
            return argd

        class fopen(object):
            """
            Ljinux standard api file operation function.
            To be used in the place of "with open()".
            Example:
              with ljinux.api.fopen("file path here", "wb", getcwd()):
            """

            def __init__(self, fname, mod="r", ctx=None):
                self.fn = fname
                self.mod = mod

            def __enter__(self):
                try:
                    global sdcard_fs
                    rm = False  # remount
                    if "w" in self.mod or "a" in self.mod:
                        rm = True
                    if rm and not sdcard_fs:
                        remount("/", False)
                    self.file = open(ljinux.api.betterpath(self.fn), self.mod)
                    if rm and not sdcard_fs:
                        remount("/", True)
                    del rm
                except RuntimeError:
                    return None
                return self.file

            def __exit__(self, typee, value, traceback):
                try:
                    self.file.flush()
                    self.file.close()

                    del self.file
                except AttributeError:
                    pass
                del self.fn, self.mod

        def isdir(dirr, rdir=None):
            """
            Checks if given item is file (returns 0) or directory (returns 1).
            Returns 2 if it doesn't exist.
            """
            res = 2

            bckdir = getcwd()
            if rdir is None:
                if "/" in dirr and dirr not in ["/", "&/"]:
                    rdir = dirr[: dirr.rfind("/")]
                    if len(rdir) == 0:
                        rdir = "/"
                    dirr = dirr[dirr.rfind("/") + 1 :]
                    cddd = ljinux.api.betterpath(rdir)
                else:
                    cddd = bckdir
            else:
                cddd = ljinux.api.betterpath(rdir)
            dirr = ljinux.api.betterpath(dirr)
            chdir(cddd)  # We assume ref dir exists
            try:
                chdir(dirr)
                chdir(bckdir)
                res = 1  # It's a dir
            except OSError:  # we are still in cddd
                if dirr in listdir():
                    res = 0
            chdir(bckdir)
            del cddd, rdir, dirr, bckdir
            return res

        def betterpath(back=None):
            """
            Ljinux standard api path translation.
            Removes the need to account for /LjinuxRoot
            """
            res = ""
            userr = ljinux.based.system_vars["USER"].lower()
            if userr != "root":
                hd = "/LjinuxRoot/home/" + ljinux.based.system_vars["USER"].lower()
            else:
                hd = "/"
            del userr
            if back is None:
                a = getcwd()
                if a.startswith(hd):
                    res = "~" + a[len(hd) :]
                elif a == "/":
                    res = "&/"
                elif a == "/LjinuxRoot":
                    res = "/"
                elif a.startswith("/LjinuxRoot"):
                    res = a[11:]
                else:
                    res = "&" + a
                del a
            else:  # resolve path back to normal
                if back in ["&/", "&"]:  # board root
                    res = "/"
                elif back.startswith("&/"):
                    res = back[1:]
                elif back.startswith("/LjinuxRoot"):
                    res = back  # already good
                elif back[0] == "/":
                    # This is for absolute paths
                    res = "/LjinuxRoot"
                    if back != "/":
                        res += back
                elif back[0] == "~":
                    res = hd
                    if back != "~":
                        res += back[1:]
                else:
                    res = back
            del back, hd
            return res

        def adv_input(whatever, _type=str):
            """
            Universal variable request
            Returns the variable's value in the specified type
            Parameters:
                whatever : The name of the variable
                _type : The type in which it should be returned
            Returns:
                The result of the variable in the type
                specified if found
                Otherwise, it returns the input
            """
            res = None
            if whatever.isdigit():
                res = int(whatever)
            elif whatever in ljinux.based.user_vars:
                res = ljinux.based.user_vars[whatever]
            elif whatever in ljinux.based.system_vars:
                res = ljinux.based.system_vars[whatever]
            elif whatever in ljinux.io.sys_getters:
                res = ljinux.io.sys_getters[whatever]()
            else:
                res = whatever
            return _type(res)

    class history:
        historyy = []
        nav = [0, 0, ""]
        sz = 50

        def load(filen):
            ljinux.history.historyy = list()
            try:
                with open(filen, "r") as historyfile:
                    for line in historyfile:
                        ljinux.io.ledset(3)  # act
                        ljinux.history.historyy.append(line.strip())
                        ljinux.io.ledset(1)  # idle
                        del line

            except OSError:
                try:
                    if not sdcard_fs:
                        remount("/", False)
                    with open(filen, "w") as historyfile:
                        pass
                    if not sdcard_fs:
                        remount("/", True)
                except RuntimeError:
                    ljinux.based.error(4, filen)
                ljinux.io.ledset(1)  # idle

        def appen(itemm):  # add to history, but don't save to file
            if (
                len(ljinux.history.historyy) > 0 and itemm != ljinux.history.gett(1)
            ) or len(ljinux.history.historyy) is 0:
                if len(ljinux.history.historyy) < ljinux.history.sz:
                    ljinux.history.historyy.append(itemm)
                elif len(ljinux.history.historyy) is ljinux.history.sz:
                    ljinux.history.shift(itemm)
                else:
                    ljinux.history.historyy = ljinux.history.historyy[
                        -(ljinux.history.sz - 1) :
                    ] + [itemm]

        def shift(itemm):
            ljinux.history.historyy.reverse()
            ljinux.history.historyy.pop()
            ljinux.history.historyy.reverse()
            ljinux.history.historyy.append(itemm)
            del itemm

        def save(filen):
            try:
                if not sdcard_fs:
                    remount("/", False)
                with open(filen, "w") as historyfile:
                    for item in ljinux.history.historyy:
                        historyfile.write(item + "\n")
                if not sdcard_fs:
                    remount("/", True)
            except (OSError, RuntimeError):
                ljinux.based.error(7, filen)

        def clear(filen):
            try:
                # deletes all history, from ram and storage
                a = open(filen, "r")
                a.close()
                del a
                if not sdcard_fs:
                    remount("/", False)
                with open(filen, "w") as historyfile:
                    historyfile.flush()
                if not sdcard_fs:
                    remount("/", True)
                ljinux.history.historyy.clear()
            except (OSError, RuntimeError):
                ljinux.based.error(4, filen)

        def gett(whichh):  # get a specific history item, from loaded history
            obj = len(ljinux.history.historyy) - whichh
            if obj < 0:
                raise IndexError
            return str(ljinux.history.historyy[obj])

        def getall():  # get the whole history, numbered, line by line
            for index, item in enumerate(ljinux.history.historyy):
                print(f"{index + 1}: {item}")
                del index, item

    class io:
        # Activity led
        ledcases = {
            0: bytearray([0, 0, 0]),  # off
            1: bytearray([3, 0, 0]),  # Alternative idle, to indicate input
            2: bytearray([2, 0, 0]),  # Idle
            3: bytearray([7, 7, 0]),  # Activity
            4: bytearray([0, 0, 5]),  # Waiting
            5: bytearray([0, 50, 0]),  # Error
            6: bytearray([255, 255, 255]),  # Your eyes are gone
            7: bytearray([0, 0, 7]),  # Alternative waiting
        }

        getled = 0

        led = digitalio.DigitalInOut(boardLED)
        ledg = None
        ledb = None

        defstate = True

        led.direction = digitalio.Direction.OUTPUT
        if configg["ledtype"].startswith("rgb"):
            ledg = digitalio.DigitalInOut(board.LED_GREEN)
            ledg.direction = digitalio.Direction.OUTPUT
            ledb = digitalio.DigitalInOut(board.LED_BLUE)
            ledb.direction = digitalio.Direction.OUTPUT

        if configg["ledtype"] == "generic_invert":
            configg["ledtype"] = "generic"
            defstate = False
        elif configg["ledtype"] == "rgb_invert":
            configg["ledtype"] = "rgb"
            defstate = False

        if configg["ledtype"] == "generic":
            led.value = defstate
        elif configg["ledtype"] == "neopixel":
            neopixel_write(led, ledcases[2])
        elif configg["ledtype"] == "rgb":
            led.value = defstate
            ledg.value = defstate
            ledb.value = defstate

        def ledset(state):
            """
            Set the led to a state.
            state can be int with one of the predifined states,
            or a tuple like (10, 40, 255) for a custom color
            """

            if isinstance(state, int):
                ## use preconfigured led states
                if configg["ledtype"] == "generic":
                    if state in [0, 3, 4, 5]:  # close tha led
                        ljinux.io.led.value = not ljinux.io.defstate
                    else:
                        ljinux.io.led.value = ljinux.io.defstate
                elif configg["ledtype"] == "neopixel":
                    neopixel_write(ljinux.io.led, ljinux.io.ledcases[state])
                elif configg["ledtype"] == "rgb":
                    cl = ljinux.io.ledcases[state]
                    ljinux.io.led.value, ljinux.io.ledg.value, ljinux.io.ledb.value = (
                        (cl[1], cl[0], cl[2])
                        if ljinux.io.defstate
                        else (not cl[1], not cl[0], not cl[2])
                    )
                    del cl

                ljinux.io.getled = state
                del state
            elif isinstance(state, tuple):
                # a custom color
                if configg["ledtype"] == "generic":
                    inv = ljinux.io.defstate
                    if sum(state) is 0:
                        inv = not inv
                    ljinux.io.led.value = inv
                    del inv
                elif configg["ledtype"] == "neopixel":
                    swapped_state = (state[1], state[0], state[2])
                    neopixel_write(ljinux.io.led, bytearray(swapped_state))
                    del swapped_state
                elif configg["ledtype"] == "rgb":
                    ljinux.io.led.value, ljinux.io.ledg.value, ljinux.io.ledb.value = (
                        (state[0], state[1], state[2])
                        if ljinux.io.defstate
                        else (not state[0], not state[1], not state[2])
                    )

                ljinux.io.getled = state
                del state
            else:
                del state
                raise TypeError("Invalid led state value")

        def get_static_file(filename, m="rb"):
            "Static file generator"
            try:
                with open(filename, m) as f:
                    b = None
                    while b is None or len(b) == 2048:
                        b = f.read(2048)
                        yield b
            except OSError:
                yield f"Error: File '{filename}' Not Found"

        def start_sdcard():
            global sdcard_fs
            if (
                configg["sd_SCLK"] != -1
                and configg["sd_SCSn"] != -1
                and configg["sd_MISO"] != -1
                and configg["sd_MOSI"] != -1
            ):
                spi = busio.SPI(
                    pintab[configg["sd_SCLK"]],
                    MOSI=pintab[configg["sd_MOSI"]],
                    MISO=pintab[configg["sd_MISO"]],
                )
                cs = digitalio.DigitalInOut(pintab[configg["sd_SCSn"]])
                dmtex("TF card bus ready")
                try:
                    sdcard = adafruit_sdcard.SDCard(spi, cs)
                    del spi
                    del cs
                    vfs = VfsFat(sdcard)
                    dmtex("TF card mount attempted")
                    mount(vfs, "/LjinuxRoot")
                    del sdcard, vfs
                    sdcard_fs = True
                except NameError:
                    dmtex("adafruit_sdcard library not present, aborting.")
            else:
                sdcard_fs = False
                dmtex("No pins for TF card, skipping setup")
                return

        sys_getters = {
            "sdcard": lambda: str(sdcard_fs),
            "uptime": lambda: str("%.5f" % (uptimee + time.monotonic())),
            "temperature": lambda: str("%.2f" % cpu.temperature),
            "memory": lambda: str(gc.mem_free()),
            "implementation_version": lambda: ljinux.based.system_vars[
                "IMPLEMENTATION"
            ],
            "implementation": lambda: implementation.name,
            "frequency": lambda: str(cpu.frequency),
            "voltage": lambda: str(cpu.voltage),
        }

    class based:
        silent = False
        olddir = None
        pled = False  # persistent led state for nested exec
        alias_dict = {}

        user_vars = {
            "history-file": "/LjinuxRoot/home/board/.history",
            "history-size": "10",
            "return": "0",
        }

        from os import uname

        system_vars = {
            "OS": "Ljinux",
            "SHELL": "Based",
            "USER": "root",
            "SECURITY": "off",
            "INIT": "normal",
            "HOSTNAME": "ljinux",
            "TERM": "xterm-256color",
            "LANG": "en_GB.UTF-8",
            "BOARD": board.board_id,
            "IMPLEMENTATION": ".".join(map(str, list(implementation.version))),
            "IMPLEMENTATION_RAW": uname()[3][: uname()[3].find(" on ")],
            "IMPLEMENTATION_DATE": uname()[3][uname()[3].rfind(" ") + 1 :],
        }
        del uname

        def get_internal():
            intlist = dir(ljinux.based.command)
            intlist.remove("__module__")
            intlist.remove("__qualname__")
            intlist.remove("__dict__")
            intlist.remove("__name__")  # these cannot be iterated over
            for item in intlist:
                if item.startswith("_"):
                    intlist.remove(item)
                del item
            return intlist

        def get_bins():
            try:
                return [
                    dirr[:-4]
                    for dirr in listdir("/LjinuxRoot/bin")
                    if dirr.endswith(".lja") and not dirr.startswith(".")
                ]
            except OSError:  # Yea no root, we cope
                return list()

        def error(wh=3, f=None, prefix=f"{colors.magenta_t}Based{colors.endc}"):
            """
            The different errors used by the based shell.
            CODE:
                ljinux.based.error([number])
                where [number] is one of the error below
            """
            ljinux.io.ledset(5)  # error
            time.sleep(0.1)
            errs = {
                1: "Syntax Error",
                2: "Input Error",
                3: "Error",
                4: f'"{f}": No such file or directory',
                5: "Network unavailable",
                6: "Display not attached",
                7: "Filesystem unwritable, board in developer mode",
                8: "Missing files",
                9: "Missing arguments",
                10: "File exists",
                11: "Not enough system memory",
                12: "Based: Error, variable already used",
                13: f"Terminal too small, minimum size: {f}",
                14: "Is a file",
                15: "Is a directory",
            }
            term.write(f"{prefix}: {errs[wh]}")
            ljinux.io.ledset(1)
            del errs

        def autorun():
            ljinux.io.ledset(3)  # act
            global Exit
            global Exit_code
            global Version

            ljinux.based.system_vars["VERSION"] = Version

            term.write(
                "\nWelcome to Ljinux wannabe kernel {}!\n\n".format(
                    ljinux.based.system_vars["VERSION"]
                ),
                end="",
            )

            try:
                systemprints(2, "Mount /LjinuxRoot")
                ljinux.io.start_sdcard()
                systemprints(1, "Mount /LjinuxRoot")
            except OSError:
                systemprints(
                    3,
                    "Mount /LjinuxRoot",
                    "Error: TF card not available, assuming built in fs",
                )
                del modules["adafruit_sdcard"]
                dmtex("Unloaded TFcard libraries")

            # Validate root exists
            try:
                chdir("/LjinuxRoot")
                chdir("/")
            except:
                systemprints(
                    4,
                    "RootValidityCheck",
                    "Cannot continue, you are on your own.",
                )
                term.hold_stdout = False
                term.flush_writes()
                return 1  # Abandon with EMERG

            ljinux.io.ledset(1)  # idle
            systemprints(
                2,
                "Running Init Script",
            )
            systemprints(
                2,
                "Attempting to open /LjinuxRoot/boot/Init.lja..",
            )
            lines = None
            Exit_code = 0
            try:
                ljinux.io.ledset(3)  # act
                ljinux.based.command.exec("/LjinuxRoot/boot/Init.lja")
                systemprints(1, "Running init script")
            except OSError:
                systemprints(3, "Init script not found")
            ljinux.history.load(ljinux.based.user_vars["history-file"])
            try:
                ljinux.history.sz = int(ljinux.based.user_vars["history-size"])
            except:
                pass
            systemprints(1, "History loaded")
            if ljinux.based.system_vars["INIT"] == "normal":
                systemprints(1, "Init complete")
            elif ljinux.based.system_vars["INIT"] == "loop":
                Exit = True
                Exit_code = 245
                term.write(
                    f"{colors.magenta_t}Based{colors.endc}: Complete. Restarting"
                )
            elif ljinux.based.system_vars["INIT"] == "oneshot":
                term.write(
                    f"{colors.magenta_t}Based{colors.endc}: Init complete. Halting"
                )
                ljinux.based.run("halt")
            else:
                term.write(
                    f"{colors.magenta_t}Based{colors.endc}: INIT specified incorrectly!"
                )
                ljinux.based.run("halt")

            ljinux.io.ledset(1)  # idle
            while not Exit:
                try:
                    ljinux.based.shell()
                except KeyboardInterrupt:
                    stdout.write("^C\n")
            Exit = False  # to allow ljinux.based.shell to be rerun from code.py
            return Exit_code

        class command:
            def exec(inpt):
                inpt = inpt.split(" ")
                global Exit
                global Exit_code

                if inpt[0] == "exec":
                    inpt = inpt[1:]
                try:
                    with open(inpt[0], "r") as filee:
                        for linee in filee:
                            linee = linee.strip()
                            ljinux.based.run(linee)
                            del linee
                    if (
                        ljinux.based.olddir is not None
                    ) and ljinux.based.olddir != getcwd():
                        chdir(ljinux.based.olddir)
                except OSError:
                    ljinux.based.error(4, inpt[0])
                del inpt

            def help(inpt):
                del inpt
                term.write(
                    f"LNL {colors.magenta_t}based{colors.endc}\nThese shell commands are defined internally or are in PATH.\nType 'help' to see this list.\n{colors.green_t}"
                )

                lt = set(ljinux.based.get_bins() + ljinux.based.get_internal())
                l = list()
                lenn = 0
                for i in lt:
                    if not i.startswith("_"):
                        l.append(i)
                        if len(i) > lenn:
                            lenn = len(i)
                    del i
                del lt
                lenn += 2
                l.sort()

                for index, tool in enumerate(l):
                    term.write(tool, end=(" " * lenn).replace(" ", "", len(tool)))
                    if index % 4 == 3:
                        stdout.write("\n")  # stdout faster than print cuz no logic
                    del index, tool
                stdout.write(colors.endc + "\n")

                del l
                del lenn

            def var(inpt):  # variables setter / editor
                valid = True
                inpt = inpt.split(" ")
                if inpt[0] == "var":  # check if the var is passed and trim it
                    temp = inpt
                    del inpt
                    inpt = []
                    for i in range(len(temp) - 1):
                        inpt.append(temp[i + 1])
                try:
                    # basic checks, if any of this fails, quit
                    for chh in inpt[0]:
                        if not (chh.islower() or chh.isupper() or chh == "-"):
                            valid = False
                            break
                    if inpt[1] != "=" or not (
                        inpt[2].startswith('"')
                        or inpt[2].isdigit()
                        or inpt[2].startswith("/")
                        or inpt[2].startswith("GP")
                        or inpt[2] in gpio_alloc
                    ):
                        valid = False
                        del chh
                    if valid:  # if the basic checks are done we can procceed to work
                        new_var = ""
                        if inpt[2].startswith('"'):
                            countt = len(inpt)
                            if inpt[2].endswith('"'):
                                new_var = str(inpt[2])[1:-1]
                            elif (countt > 3) and (inpt[countt - 1].endswith('"')):
                                new_var += str(inpt[2])[1:] + " "
                                for i in range(3, countt - 1):
                                    new_var += inpt[i] + " "
                                    del i
                                new_var += str(inpt[countt - 1])[:-1]
                            else:
                                ljinux.based.error(1)
                                valid = False
                        elif inpt[2].startswith("GP"):  # gpio allocation
                            if len(inpt[2]) > 2 and len(inpt[2]) <= 4:
                                gpp = int(inpt[2][2:])
                            else:
                                ljinux.based.error(2)
                                return "1"
                            if gpp in pin_alloc:
                                dmtex("PIN ALLOCATED, ABORT", force=True)
                                return "1"
                            else:
                                if ljinux.api.adv_input(inpt[0], str) == inpt[0]:
                                    gpio_alloc.update(
                                        {
                                            inpt[0]: [
                                                digitalio.DigitalInOut(pintab[gpp]),
                                                gpp,
                                            ]
                                        }
                                    )
                                    gpio_alloc[inpt[0]][0].switch_to_input(
                                        pull=digitalio.Pull.DOWN
                                    )
                                    pin_alloc.add(gpp)
                                else:
                                    ljinux.based.error(12)
                            del gpp
                            valid = False  # skip the next stuff

                        elif inpt[0] in gpio_alloc:
                            if inpt[2].isdigit():
                                if (
                                    gpio_alloc[inpt[0]][0].direction
                                    != digitalio.Direction.OUTPUT
                                ):
                                    gpio_alloc[inpt[0]][
                                        0
                                    ].direction = digitalio.Direction.OUTPUT
                                gpio_alloc[inpt[0]][0].value = int(inpt[2])
                                valid = False  # skip the next stuff
                        elif inpt[2] in gpio_alloc:
                            pass  # yes we really have to pass
                        else:
                            new_var += str(inpt[2])
                    else:
                        ljinux.based.error(1)
                        valid = False
                    if valid:  # now do the actual set
                        if inpt[0] in ljinux.based.system_vars:
                            if not (ljinux.based.system_vars["SECURITY"] == "on"):
                                ljinux.based.system_vars[inpt[0]] = new_var
                            else:
                                term.write(
                                    colors.error
                                    + "Cannot edit system variables, security is enabled."
                                    + colors.endc
                                )
                        elif (
                            inpt[0] == ljinux.api.adv_input(inpt[0], str)
                            or inpt[0] in ljinux.based.user_vars
                        ):
                            if inpt[2] in gpio_alloc:  # if setting value is gpio
                                if (
                                    gpio_alloc[inpt[2]][0].direction
                                    != digitalio.Direction.INPUT
                                ):
                                    gpio_alloc[inpt[2]][
                                        0
                                    ].direction = digitalio.Direction.INPUT
                                    gpio_alloc[inpt[2]][0].switch_to_input(
                                        pull=digitalio.Pull.DOWN
                                    )
                                ljinux.based.user_vars[inpt[0]] = str(
                                    int(gpio_alloc[inpt[2]][0].value)
                                )
                            else:
                                ljinux.based.user_vars[inpt[0]] = new_var
                        else:
                            ljinux.based.error(12)
                except IndexError:
                    ljinux.based.error(1)

            def unset(inpt):  # del variables
                inpt = inpt.split(" ")
                try:
                    a = inpt[0]
                    if a == ljinux.api.adv_input(a, str) and a not in gpio_alloc:
                        ljinux.based.error(2)
                    else:
                        if a in gpio_alloc:
                            gpio_alloc[a][0].deinit()
                            pin_alloc.remove(gpio_alloc[a][1])
                            del gpio_alloc[a]
                        elif a in ljinux.based.system_vars:
                            if not (ljinux.based.system_vars["SECURITY"] == "on"):
                                del ljinux.based.system_vars[a]
                            else:
                                term.write(
                                    colors.error
                                    + "Cannot edit system variables, security is enabled."
                                    + colors.endc
                                )
                        elif a in ljinux.based.user_vars:
                            del ljinux.based.user_vars[a]
                        else:
                            raise IndexError
                    del a
                except IndexError:
                    ljinux.based.error(1)

            def su(inpt):  # su command but worse
                inpt = inpt.split(" ")
                global dfpasswd
                passwordarr = {}
                try:
                    try:
                        with open("/LjinuxRoot/etc/passwd", "r") as data:
                            for line in data:
                                dt = line.split()
                                passwordarr[dt[0]] = dt[1]
                                del dt, line
                    except OSError:
                        pass
                    ljinux.io.ledset(2)
                    if passwordarr["root"] == getpass():
                        ljinux.based.system_vars["SECURITY"] = "off"
                        term.write("Authentication successful. Security disabled.")
                    else:
                        ljinux.io.ledset(3)
                        time.sleep(2)
                        term.write(
                            colors.error + "Authentication unsuccessful." + colors.endc
                        )

                    try:
                        del passwordarr
                    except NameError:
                        pass

                except (KeyboardInterrupt, KeyError):  # I betya some cve's cover this
                    try:
                        del passwordarr
                    except NameError:
                        pass

                    if dfpasswd == getpass():
                        ljinux.based.system_vars["security"] = "off"
                        term.write("Authentication successful. Security disabled.")
                    else:
                        term.write(
                            colors.error + "Authentication unsuccessful." + colors.endc
                        )
                try:
                    del passwordarr
                except NameError:
                    pass

            def history(inpt):  # history frontend
                inpt = inpt.split(" ")
                if inpt[0] == "":
                    ljinux.history.getall()
                elif inpt[0] == "clear":
                    ljinux.history.clear(ljinux.based.user_vars["history-file"])
                elif inpt[0] == "load":
                    ljinux.history.load(ljinux.based.user_vars["history-file"])
                    if "history-size" in ljinux.based.user_vars:
                        ljinux.history.sz = int(ljinux.based.user_vars["history-size"])
                elif inpt[0] == "save":
                    ljinux.history.save(ljinux.based.user_vars["history-file"])
                else:
                    term.write(f"{colors.magenta_t}Based{colors.endc}: Invalid option")

            def pexec(inpt):  # Python exec
                gc.collect()
                try:
                    exec(inpt)  # Vulnerability.exe
                except Exception as err:
                    term.write(
                        "Traceback (most recent call last):\n\t"
                        + str(type(err))[8:-2]
                        + ": "
                        + str(err)
                    )
                    del err
                del inpt
                gc.collect()

            def fpexec(inpt):  # Python script exec
                fpargs = list()
                inpt = inpt.split(" ")
                offs = 0
                if inpt[0] == "fpexec":
                    offs += 1

                try:
                    while inpt[offs].startswith("-"):
                        fpargs += list(inpt[offs][1:])
                        offs += 1
                except IndexError:
                    ljinux.based.error(9)
                    ljinux.based.user_vars["return"] = "1"
                    return

                gc.collect()
                try:
                    a = open(ljinux.api.betterpath(inpt[offs])).read()
                    gc.collect()
                    if not ("t" in fpargs or "l" in fpargs):
                        exec(a)
                    elif "i" in fpargs:
                        exec(a, dict(), dict())
                    elif "l" in fpargs:
                        exec(a, locals())
                    del a
                except Exception as err:
                    term.write(
                        "Traceback (most recent call last):\n\t"
                        + str(type(err))[8:-2]
                        + ": "
                        + str(err)
                    )
                    del err
                del offs, fpargs

        def parse_pipes(inpt):
            # This is a pipe
            p_and = "&&" in inpt
            p_to = "|" in inpt

            comlist = list()
            silencelist = list()
            comindex = -1

            if p_and and p_to:  # TODO
                # silencelist.append(False)
                # silencelist.append(True)
                pass
            elif p_and:
                while "&&" in inpt:
                    silencelist.append(False)
                    comlist.append(inpt[: inpt.find("&&")])
                    inpt = inpt[inpt.find("&&") + 2 :]
                    comindex += 1
                    while comlist[comindex].endswith(" "):
                        comlist[comindex] = comlist[comindex][:-1]
                    while comlist[comindex].startswith(" "):
                        comlist[comindex] = comlist[comindex][1:]

                while inpt.endswith(" "):
                    inpt = inpt[:-1]
                while inpt.startswith(" "):
                    inpt = inpt[1:]
                silencelist.append(False)
                comlist.append(inpt)
            elif p_to:  # TODO
                # silencelist.append(False)
                # silencelist.append(True)
                pass
            else:
                silencelist.append(False)
                comlist.append(inpt)

            del p_and, p_to, comindex, inpt
            return comlist, silencelist

        def run(executable, argv=None):
            # runs any single command

            ledmine = False  # ownership of led
            oldled = None
            if not ljinux.based.pled:
                ljinux.based.pled = True
                ljinux.io.ledset(3)
                ledmine = True
            else:
                oldled = ljinux.io.getled
                ljinux.io.ledset(3)

            if isinstance(argv, list):
                argv = " ".join(argv)
            elif argv is None:
                splitt = executable.split(" ")
                if len(splitt) > 1:
                    executable = splitt[0]
                    argv = " ".join(splitt[1:])
                del splitt

            if executable in ljinux.based.alias_dict.keys():
                executable = ljinux.based.alias_dict[executable]
                splitt = executable.split(" ")
                if len(splitt) > 1:
                    executable = splitt[0]
                    if argv is None:
                        argv = " ".join(splitt[1:])
                    else:
                        argv += " " + " ".join(splitt[1:])
                del splitt

            bins = ljinux.based.get_bins()
            ints = ljinux.based.get_internal()
            inbins = executable in bins
            inints = executable in ints
            del bins, ints
            gc.collect()

            if (executable == "") or executable.isspace() or executable.startswith("#"):
                pass
            elif executable in ljinux.modules:  # kernel module
                ljinux.based.modules[executable](argv)
            elif inbins:  # external commands
                bckargj = (
                    ""
                    if "argj" not in ljinux.based.user_vars
                    else ljinux.based.user_vars["argj"]
                )
                ljinux.api.setvar(
                    "argj", executable + ("" if argv is None else (" " + argv))
                )
                ljinux.based.command.exec("/LjinuxRoot/bin/" + executable + ".lja ")
                ljinux.api.setvar("argj", bckargj)
                del bckargj
            elif inints:  # internal commands
                if argv is None:
                    exec(f'ljinux.based.command.{executable}("")')
                else:
                    exec(
                        "ljinux.based.command."
                        + executable
                        + "('"
                        + argv.replace("'", "\\'")
                        + "')"
                    )
            elif argv is not None and argv.startswith("="):  # variable operation
                ljinux.based.command.var(executable + " " + argv)
            else:  # error
                term.write(
                    f"{colors.magenta_t}Based{colors.endc}: '{executable}': command not found"
                )
                ljinux.based.user_vars["return"] = "1"

            if ledmine:
                ljinux.based.pled = False
                ljinux.io.ledset(1)
            else:
                ljinux.io.ledset(oldled)

            del inbins, inints, executable, argv, ledmine, oldled
            gc.collect()

        def shell(led=True, nalias=False):
            # The interactive main shell
            # no longer accepts commands here

            global Exit, Exit_code

            if not term.enabled:
                ljinux.io.ledset(4)  # waiting for serial
                term.start()
                ljinux.io.ledset(1)  # idle
                term.trigger_dict = {
                    "enter": 0,
                    "ctrlC": 1,
                    "ctrlD": 2,
                    "ctrlL": 13,
                    "tab": 3,
                    "up": 4,
                    "down": 7,
                    "pgup": 11,
                    "pgdw": 12,
                    "overflow": 14,
                    "rest": "stack",
                    "rest_a": "common",
                    "echo": "common",
                    "idle": 20,
                }

            command_input = None
            if not Exit:
                while ((command_input == None) or (command_input == "\n")) and not Exit:
                    term.trigger_dict["prefix"] = (
                        "["
                        + colors.cyan_t
                        + ljinux.based.system_vars["USER"]
                        + colors.endc
                        + "@"
                        + colors.cyan_t
                        + ljinux.based.system_vars["HOSTNAME"]
                        + colors.endc
                        + "| "
                        + colors.yellow_t
                        + ljinux.api.betterpath()
                        + colors.endc
                        + "]"
                        + colors.blue_t
                        + "> "
                        + colors.endc
                    )

                    command_input = None
                    while (command_input in [None, ""]) and not Exit:
                        try:
                            term.program()
                            if term.buf[0] is 0:  # enter
                                ljinux.history.nav[0] = 0
                                command_input = term.buf[1]
                                term.buf[1] = ""
                                term.focus = 0
                                stdout.write("\n")
                            elif term.buf[0] is 1:
                                ljinux.io.ledset(2)  # keyact
                                print("^C")
                                term.buf[1] = ""
                                term.focus = 0
                                term.clear_line()
                                ljinux.io.ledset(1)  # idle
                            elif term.buf[0] is 2:
                                ljinux.io.ledset(2)  # keyact
                                print("^D")
                                Exit = True
                                Exit_code = 0
                                ljinux.io.ledset(1)  # idle
                                break
                            elif term.buf[0] is 3:  # tab key
                                if len(term.buf[1]):
                                    ljinux.io.ledset(2)  # keyact
                                    tofind = term.buf[
                                        1
                                    ]  # made into var for speed reasons
                                    candidates = []
                                    slicedd = tofind.split()
                                    lent = len(slicedd)
                                    if lent > 1:  # suggesting files
                                        files = listdir()
                                        for i in files:
                                            if i.startswith(
                                                slicedd[lent - 1]
                                            ):  # only on the arg we are in
                                                candidates.append(i)
                                            del i
                                        del files
                                    else:  # suggesting bins
                                        bins = ljinux.based.get_bins()
                                        ints = ljinux.based.get_internal()
                                        for i in [ints, bins]:
                                            for j in i:
                                                if j.startswith(tofind):
                                                    candidates.append(j)
                                                del j
                                            del i
                                        del bins, ints
                                    if len(candidates) > 1:
                                        stdout.write("\n")
                                        minn = 100
                                        for i in candidates:
                                            if not i.startswith("_"):  # discard those
                                                minn = min(minn, len(i))
                                                print("\t" + i)
                                            del i
                                        letters_match = 0
                                        isMatch = True
                                        while isMatch:
                                            for i in range(0, minn):
                                                for j in range(1, len(candidates)):
                                                    try:
                                                        if (
                                                            not candidates[j][
                                                                letters_match
                                                            ]
                                                            == candidates[j - 1][
                                                                letters_match
                                                            ]
                                                        ):
                                                            isMatch = False
                                                            break
                                                        else:
                                                            letters_match += 1
                                                    except IndexError:
                                                        isMatch = False
                                                        break
                                                    del j
                                                del i
                                                if not isMatch:
                                                    break
                                        del minn, isMatch
                                        if letters_match > 0:
                                            term.clear_line()
                                            if lent > 1:
                                                term.buf[1] = " ".join(
                                                    slicedd[:-1]
                                                    + [candidates[0][:letters_match]]
                                                )
                                            else:
                                                term.buf[1] = candidates[0][
                                                    :letters_match
                                                ]
                                        term.focus = 0
                                        del letters_match
                                    elif len(candidates) == 1:
                                        term.clear_line()
                                        if lent > 1:
                                            term.buf[1] = " ".join(
                                                slicedd[:-1] + [candidates[0]]
                                            )
                                        else:
                                            term.buf[1] = candidates[0]
                                        term.focus = 0
                                    else:
                                        term.clear_line()
                                    del candidates, lent, tofind, slicedd
                                    ljinux.io.ledset(1)  # idle
                                else:
                                    term.clear_line()
                            elif term.buf[0] is 4:  # up
                                ljinux.io.ledset(2)  # keyact
                                try:
                                    neww = ljinux.history.gett(
                                        ljinux.history.nav[0] + 1
                                    )
                                    # if no historyitem, we wont run the items below
                                    if ljinux.history.nav[0] == 0:
                                        ljinux.history.nav[2] = term.buf[1]
                                        ljinux.history.nav[1] = term.focus
                                    term.buf[1] = neww
                                    del neww
                                    ljinux.history.nav[0] += 1
                                    term.focus = 0
                                except IndexError:
                                    pass
                                term.clear_line()
                                ljinux.io.ledset(1)  # idle
                            elif term.buf[0] is 7:  # down
                                ljinux.io.ledset(2)  # keyact
                                if ljinux.history.nav[0] > 0:
                                    if ljinux.history.nav[0] > 1:
                                        term.buf[1] = ljinux.history.gett(
                                            ljinux.history.nav[0] - 1
                                        )
                                        ljinux.history.nav[0] -= 1
                                        term.focus = 0
                                    else:
                                        # have to give back the temporarily stored one
                                        term.buf[1] = ljinux.history.nav[2]
                                        term.focus = ljinux.history.nav[1]
                                        ljinux.history.nav[0] = 0
                                term.clear_line()
                            elif term.buf[0] in [11, 12]:  # pgup / pgdw
                                term.clear_line()
                            elif term.buf[0] is 13:  # Ctrl + L (clear screen)
                                term.clear()
                            elif term.buf[0] is 14:  # overflow
                                store = term.buf[1]
                                term.focus = 0
                                term.buf[1] = ""
                                term.trigger_dict["prefix"] = "> "
                                term.clear_line()
                                term.program()
                                if term.buf[0] is 0:  # enter
                                    ljinux.history.nav[0] = 0
                                    command_input = store + term.buf[1]
                                    term.buf[1] = ""
                                    stdout.write("\n")
                                elif term.buf[0] is 14:  # more lines
                                    store += term.buf[1]
                                    ljinux.history.nav[0] = 0
                                    term.buf[1] = ""
                                    term.focus = 0
                                    term.clear_line()
                                else:  # not gonna
                                    term.buf[0] = ""
                                    term.focus = 0
                                    ljinux.history.nav[0] = 0
                                del store
                            elif term.buf[0] is 20:  # console disconnected
                                ljinux.based.command.exec(
                                    "/LjinuxRoot/bin/_waitforconnection.lja"
                                )
                                term.clear_line()
                        except KeyboardInterrupt:
                            # duplicate code as by ^C^C you could escape somehow
                            print("^C")
                            term.buf[1] = ""
                            term.focus = 0
                            term.clear_line()
                if not Exit:
                    res = ""
                    if led:
                        ljinux.io.ledset(3)  # act
                    if not (
                        command_input == ""
                        or command_input.isspace()
                        or command_input.startswith("#")
                    ):
                        # Save to history
                        if command_input.startswith(" "):
                            while command_input.startswith(" "):
                                command_input = command_input[1:]
                        else:
                            ljinux.history.appen(command_input.strip())

                        # Output to file
                        p_write = ">" in command_input

                        # Remove > pipe from line, TODO
                        pass

                        # Fetch list of commands
                        comlist, silencelist = ljinux.based.parse_pipes(command_input)
                        if len(comlist) > 1:
                            comlist.reverse()
                            silencelist.reverse()
                        while len(comlist):
                            currentcmd = comlist.pop()
                            silencecmd = silencelist.pop()
                            if silencecmd:
                                ljinux.based.silent = True
                            ljinux.based.run(currentcmd)
                            if silencecmd:
                                ljinux.based.silent = False
                            del currentcmd, silencecmd
                        del comlist, silencelist  # abandon command_input

                        # Write stdout to file, TODO
                        pass

                        del p_write
                        gc.collect()
                        gc.collect()
                    if led:
                        ljinux.io.ledset(1)  # idle
                    gc.collect()
                    gc.collect()
                    return res
