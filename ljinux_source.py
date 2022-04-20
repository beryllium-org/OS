# -----------------
#      Ljinux
# Coded on a Raspberry Pi 400
# Ma'am I swear this project is real
# -----------------

# Some important vars
Version = "0.4.0"
Circuitpython_supported_version = 7
dmesg = []
access_log = []

# Core board libs
try:
    import board
    import digitalio
except ImportError:
    print("O_O nope, i'm out")
    from sys import exit

    exit(0)

print("[    0.00000] Core libs loaded")
dmesg.append("[    0.00000] Core libs loaded")

# Pin allocation table
pin_alloc = set()

# Default password, aka the password if no /LjinuxRoot/etc/passwd is found
dfpasswd = "Ljinux"

# Exit code holder, has to be global for everyone to be able to see it.
Exit = False
Exit_code = 0

# Hardware autodetect vars, starts assuming everything is missing
sdcard_fs = False
display_availability = False
print("[    0.00000] Sys vars loaded")
dmesg.append("[    0.00000] Sys vars loaded")

import time

print("[    0.00000] Timing libraries done")
dmesg.append("[    0.00000] Timing libraries done")
uptimee = (
    -time.monotonic()
)  # using uptimee as an offset, this way uptime + time.monotonic = 0 at this very moment and it goes + from here on out
print("[    0.00000] Got time zero")
dmesg.append("[    0.00000] Got time zero")

import gc

gc.enable()
print("[    0.00000] Garbage collector loaded and enabled")
dmesg.append("[    0.00000] Garbage collector loaded and enabled")

# dmtex previous end holder
oend = "\n"  # needed to mask print

try:
    from jcurses import jcurses

    term = jcurses()  # the main curses entity, used primarily for based.shell()
    print("[    0.00000] Loaded jcurses")
    dmesg.append("[    0.00000] Loaded jcurses")
except ImportError:
    print("CRITICAL: FAILED TO LOAD JCURSES")
    exit(0)


def dmtex(texx=None, end="\n", timing=True):
    # Persistent offset, Print "end=" preserver
    global uptimee, oend

    ct = "%.5f" % (
        uptimee + time.monotonic()
    )  # current time since ljinux start rounded to 5 digits
    if timing:
        # timing is used to disable the time print in case you want to make a print(blah,end='')
        strr = "[{u}{upt}] {tx}".format(
            u="           ".replace(" ", "", len(ct)), upt=str(ct), tx=texx
        )
    else:
        strr = texx  # the message as is

    if not term.dmtex_suppress:
        print(strr, end=end)  # using the provided end

    if (
        "\n" == oend
    ):  # if the oend of the last print is a newline we add a new entry, otherwise we go to the last one and we add it along with the old oend
        dmesg.append(strr)
    elif (len(oend.replace("\n", "")) > 0) and (
        "\n" in oend
    ):  # special case, there is hanging text in old oend
        a = len(dmesg) - 1  # the last entry
        dmesg[a] += oend.replace("\n", "")  # add the spare text
        dmesg.append(strr)  # do the new entry now
    else:  # append to the last entry
        a = len(dmesg) - 1  # the last entry
        dmesg[a] += oend + strr  # with the ending ofc
    oend = end  # then we save the new oend for the next go


print("[    0.00000] Timings reset")
dmesg.append("[    0.00000] Timings reset")

# Now we can use this function to get a timing
dmtex("Basic Libraries loading")

# Basic libs
# These are absolutely needed

from sys import (
    implementation,
    platform,  # needed for picofetch
    modules,
    exit,
    stdout,
)  # if this import fails, idk

dmtex("System libraries loaded")

try:
    import busio

    from microcontroller import cpu, cpus

    from storage import remount, VfsFat, mount

    from os import chdir, rmdir, mkdir, sync, getcwd, listdir, remove

    from io import StringIO
    from usb_cdc import console
    from getpass import getpass
    import json
    from traceback import print_exception
    from math import trunc

    dmtex("Basic libraries loaded")
except ImportError:
    dmtex("FATAL: CRITICAL LIBRARY LOAD FAILED")
    exit(0)

try:
    from neopixel_write import neopixel_write

    try:  # we can't fail this part though
        from neopixel_colors import neopixel_colors as nc
    except ImportError:
        dmtex("CRITICAL: FAILED TO LOAD NEOPIXEL_COLORS")
        exit(1)
except ImportError:
    pass  # no big deal, this just isn't a neopixel board

# Kernel cmdline.txt
try:
    confign = "/config-" + board.board_id + ".json"
    with open(confign, "r") as f:  # load the config file
        dmtex("Loaded " + confign)
        configg = json.load(f)  # and parse it as a json
        f.close()
    del confign

except (ValueError, OSError):
    configg = {}
    dmtex("Kernel config could not be found / parsed, applying defaults")

try:
    from lj_colours import lJ_Colours as colors

    print(colors.reset_s_format, end="")
    dmtex("Loaded lj_colours")
except ImportError:
    dmtex("CRITICAL: FAILED TO LOAD LJ_COLOURS")
    exit(0)

dmtex("Options applied:")

defaultoptions = {  # default configuration, in line with the manual
    "displaySCL": (17, int),
    "displaySDA": (16, int),
    "displayheight": (64, int),  # SSD1306 spec
    "displaywidth": (128, int),  # SSD1306 spec
    "led": (0, int),
    "ledtype": ("generic", str),
    "fixrtc": (True, bool),
    "SKIPTEMP": (False, bool),
    "SKIPCP": (False, bool),
    "DEVBOARD": (False, bool),
    "DEBUG": (False, bool),
    "DISPLAYONLYMODE": (False, bool),
}

# General options
for optt in {
    "fixrtc",
    "SKIPTEMP",
    "SKIPCP",
    "DEBUG",
    "DEVBOARD",
    "DISPLAYONLYMODE",
    "displayheight",
    "displaywidth",
    "led",
    "ledtype",
}:
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
            'Missing / Invalid value for "' + optt + '" applied: ' + str(configg[optt]),
            timing=False,
        )

pintab = {  # Hardware pin allocations
    1: board.GP1,
    2: board.GP2,
    3: board.GP3,
    4: board.GP4,
    5: board.GP5,
    6: board.GP6,
    7: board.GP7,
    8: board.GP8,
    9: board.GP9,
    10: board.GP10,
    11: board.GP11,
    12: board.GP12,
    13: board.GP13,
    14: board.GP14,
    15: board.GP15,
    16: board.GP16,
    17: board.GP17,
    18: board.GP18,
    19: board.GP19,
    20: board.GP20,
    24: board.GP24,
    25: board.GP25,
    26: board.GP26,
    27: board.GP27,
    28: board.GP28,
}

for optt in {"displaySCL", "displaySDA", "led"}:
    try:
        pin = configg[optt]
        if pin in pin_alloc:
            dmtex("PIN ALLOCATED, EXITING")
            exit(0)
        else:
            pin_alloc.add(pin)
        dmtex(
            "\t" + colors.green_t + "√" + colors.endc + " " + optt + "=" + str(pin),
            timing=False,
        )
        del pin
    except KeyError:
        pass

dmtex("Total pin alloc: ", end="")
for i in pin_alloc:
    dmtex(str(i), timing=False, end=" ")
dmtex("", timing=False)

if configg["led"] == 0:
    boardLED = board.LED
else:
    boardLED = pintab[configg["led"]]

del defaultoptions
del pintab

# basic checks
if not configg["SKIPCP"]:  # beta testing
    if implementation.version[0] == Circuitpython_supported_version:
        dmtex("Running on supported implementation")
    else:
        dmtex(
            "-" * 42
            + "\n"
            + " " * 14
            + "WARNING: Unsupported CircuitPython version\n"
            + " " * 14
            + "Continuing after led alert..\n"
            + " " * 14
            + "-" * 42
        )
        time.sleep(6)
else:
    print("Skipped CircuitPython version checking, happy beta testing!")

if not configg["SKIPTEMP"]:
    """
    Taking measures in case of unordinary temperature readings.
    The override exists in case of hardware failure.
    """
    temp = cpu.temperature
    if temp > 60:
        while True:
            dmtex("Temperature is unsafe: " + str(temp) + " Celcius. Halting!")
            time.sleep(0.3)
    elif temp > 7:
        dmtex("Temperature OK: " + str(temp) + " Celcius")
    else:
        dmtex("Now that a 'cool' pico! B)")
    del temp
else:
    print("Temperature check skipped, rest in pieces cpu.")

if not configg["DEVBOARD"]:
    """
    Enable to skip board checks and patches.
    """
    print("Running board detection")
    boardactions = {
        "raspberry_pi_pico": lambda: dmtex("Running on a Raspberry Pi Pico."),
        "waveshare_rp2040_zero": lambda: dmtex("Running on a Waveshare RP2040-Zero."),
    }

    try:
        boardactions[board.board_id]()
    except KeyError:
        dmtex(
            colors.error
            + "Unknown board. "
            + colors.endc
            + "Please open an issue in "
            + colors.cyan_t
            + "https://github.com/bill88t/ljinux"
            + colors.endc
            + "\nContinuing in 20 seconds without any patches, assuming it's Raspberry Pi Pico compatible."
        )
        time.sleep(20)
    del boardactions
else:
    dmtex("Board detection skipped. Enjoy experimenting!")

gc.collect()
gc.collect()
dmtex(("Memory free: " + str(gc.mem_free()) + " bytes"))
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
    dmtex(colors.error + "CRITICAL: " + colors.endc + "AUDIO LIBRARIES LOADING FAILED")

# sd card
try:
    import adafruit_sdcard

    dmtex("Sdcard libraries loaded")
except ImportError:
    dmtex(colors.error + "CRITICAL: " + colors.endc + "SDCARD LIBRARIES LOADING FAILED")

# display
try:
    import adafruit_ssd1306

    dmtex("Display libraries loaded")
except ImportError:
    dmtex(
        colors.error + "CRITICAL: " + colors.endc + "DISPLAY LIBRARIES LOADING FAILED"
    )

# networking
try:
    import adafruit_requests as requests
    from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K
    import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket
    from adafruit_wsgi.wsgi_app import WSGIApp
    import adafruit_wiznet5k.adafruit_wiznet5k_wsgiserver as server

    dmtex("Networking libraries loaded")
except ImportError:
    dmtex(
        colors.error
        + "CRITICAL: "
        + colors.endc
        + "NETWORKING LIBRARIES LOADING FAILED"
    )

if not configg["fixrtc"]:
    # for rtc
    # based off of https://github.com/afaonline/DS1302_CircuitPython
    try:
        import rtc
        import ds1302

        dmtex("RTC library loaded")
        # rtc stuff @ init cuz otherwise system fails to access it
        # the pins to connect it to:
        rtcclk = digitalio.DigitalInOut(board.GP6)
        rtcdata = digitalio.DigitalInOut(board.GP7)
        rtcce = digitalio.DigitalInOut(board.GP8)

        # to make it suitable for system
        class RTC:
            @property
            def datetime(self):
                return rtcc.read_datetime()

        try:
            rtcc = ds1302.DS1302(rtcclk, rtcdata, rtcce)
            rtc.set_time_source(RTC())
            del rtcclk
            del rtcdata
            del rtcce
        except OSError:  # not sure how to catch if it's not available, TODO
            pass

        dmtex("RTC clock init done")
    except ImportError:
        dmtex(
            colors.error + "CRITICAL: " + colors.endc + "RTC LIBRARIES LOADING FAILED"
        )

dmtex("Imports complete")


def systemprints(mod, tx1, tx2=None):
    dmtex("[ ", timing=False, end="")

    mods = {
        1: lambda: dmtex(colors.green_t + "OK", timing=False, end=""),
        2: lambda: dmtex(colors.magenta_t + "..", timing=False, end=""),
        3: lambda: dmtex(colors.red_t + "FAILED", timing=False, end=""),
    }
    mods[mod]()
    dmtex(colors.endc + " ] " + tx1, timing=False)
    if tx2 is not None:
        dmtex("           -> " if mod is 3 else "       -> ", timing=False, end="")
        dmtex(tx2, timing=False)


dmtex("Additional loading done")


class ljinux:  # The parentheses are needed. Same as with jcurses. Don't remove them.
    class history:
        historyy = []
        nav = [0, 0, ""]

        def load(filen):
            ljinux.history.historyy = list()
            try:
                with open(filen, "r") as historyfile:
                    lines = historyfile.readlines()
                    for line in lines:
                        ljinux.io.ledset(3)  # act
                        ljinux.history.historyy.append(line.strip())
                        ljinux.io.ledset(1)  # idle

            except OSError:
                ljinux.io.ledset(1)  # idle
                ljinux.based.error(4, filen)

        def appen(itemm):  # add to history, but don't save to file
            ljinux.history.historyy.append(itemm)

        def save(filen):
            try:
                # File unused but I need to check it's existence
                a = open(filen, "r")
                a.close()
                try:
                    with open(filen, "w") as historyfile:
                        for item in ljinux.history.historyy:
                            historyfile.write(item + "\n")

                        historyfile.flush()
                except OSError:
                    ljinux.based.error(7, filen)
            except OSError:
                ljinux.based.error(4, filen)

        def clear(filen):  # deletes all history, from ram and storage
            try:
                a = open(filen, "r")
                a.close()
                with open(filen, "w") as historyfile:
                    historyfile.flush()
                ljinux.history.historyy.clear()
            except OSError:
                ljinux.based.error(4, filen)

        def gett(whichh):  # get a specific history item, from loaded history
            return str(ljinux.history.historyy[len(ljinux.history.historyy) - whichh])

        def getall():  # get the whole history, numbered, line by line
            for i in range(len(ljinux.history.historyy)):
                print(str(i + 1) + ": " + str(ljinux.history.historyy[i]))

    class backrounding:
        webserver = False

        def main_tick(loud=False):  # this run in between of shell character captures
            if ljinux.backrounding.webserver:
                try:
                    ljinux.networking.wsgiServer.update_poll()
                except AttributeError:
                    global access_log
                    print("Error:\n" + str(access_log))
            if loud:
                print(str(gc.mem_free()))

    class io:
        # activity led

        ledcases = {
            0: nc.off,
            1: nc.idle,
            2: nc.idletype,
            3: nc.activity,
            4: nc.waiting,
            5: nc.error,
            6: nc.killtheuser,
        }

        led = digitalio.DigitalInOut(boardLED)
        led.direction = digitalio.Direction.OUTPUT
        if configg["ledtype"] == "generic":
            led.value = True
        elif configg["ledtype"] == "neopixel":
            neopixel_write(led, nc.idle)

        # sd card
        # L R and Enter keys for basic io
        buttonl = digitalio.DigitalInOut(board.GP19)
        buttonl.switch_to_input(pull=digitalio.Pull.DOWN)
        buttonr = digitalio.DigitalInOut(board.GP18)
        buttonr.switch_to_input(pull=digitalio.Pull.DOWN)
        buttone = digitalio.DigitalInOut(board.GP20)
        buttone.switch_to_input(pull=digitalio.Pull.DOWN)
        network = None
        network_online = False
        network_name = "Offline"

        def ledset(state):  # Set the led to a state
            if configg["ledtype"] == "generic":
                if state in [0, 3]:
                    ljinux.io.led.value = False
                else:
                    ljinux.io.led.value = True
            elif configg["ledtype"] == "neopixel":
                neopixel_write(ljinux.io.led, ljinux.io.ledcases[state])

        def get_static_file(filename, m="rb"):
            "Static file generator"
            try:
                with open(filename, m) as f:
                    b = None
                    while b is None or len(b) == 2048:
                        b = f.read(2048)
                        yield b
            except OSError:
                yield "CRITICAL: File Not Found"

        def init_net():
            cs = digitalio.DigitalInOut(board.GP13)
            spi = busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP12)
            dmtex("Network bus ready")
            ca = True
            try:
                ljinux.io.network = WIZNET5K(spi, cs, is_dhcp=False)
                dmtex("Eth interface created")
            except (AssertionError, NameError):
                dmtex("Eth interface creation failed")
                ca = False
            del spi
            del cs
            if ca and ljinux.io.network.link_status:
                dhcp_status = ljinux.io.network.set_dhcp(
                    hostname="Ljinux", response_timeout=10
                )
                dmtex("Ran dhcp")
                if dhcp_status == 0:
                    dmtex('Hostname set to "Ljinux"')
                    requests.set_socket(socket, ljinux.io.network)
                    dmtex("Eth set as socket")
                    dmtex("Chip: " + ljinux.io.network.chip)
                    macc = ""
                    for i in ljinux.io.network.mac_address:
                        macc += str(hex(i))[2:] + ":"
                    dmtex("MAC eth0: " + macc[:-1])
                    del macc
                    dmtex(
                        "IP address: "
                        + ljinux.io.network.pretty_ip(ljinux.io.network.ip_address)
                    )
                    dmtex("Neworking init successful")
                    ljinux.io.network_name = "eth0"
                    ljinux.io.network_online = True
                    server.set_interface(ljinux.io.network)
                    server.socket.gc.enable()
                else:
                    dmtex("DHCP failed")
            else:
                dmtex("Ethernet cable not connected / interface unavailable")
                try:
                    del modules["adafruit_wiznet5k.adafruit_wiznet5k_dhcp"]
                    del modules["adafruit_wiznet5k.adafruit_wiznet5k_socket"]
                    del modules["adafruit_wiznet5k.adafruit_wiznet5k_dns"]
                    del modules["adafruit_wiznet5k.adafruit_wiznet5k"]
                    del modules["adafruit_wiznet5k"]
                    del modules["adafruit_wsgi.wsgi_app"]
                    del modules["adafruit_requests"]
                    del modules["adafruit_wiznet5k.adafruit_wiznet5k_wsgiserver"]
                    del modules["adafruit_wsgi"]
                    del modules["adafruit_wsgi.request"]
                except KeyError:
                    pass
                dmtex("Unloaded networking libraries")
            del ca

        def start_sdcard():
            global sdcard_fs
            spi = busio.SPI(board.GP2, MOSI=board.GP3, MISO=board.GP4)
            cs = digitalio.DigitalInOut(board.GP5)
            dmtex("SD bus ready")
            try:
                sdcard = adafruit_sdcard.SDCard(spi, cs)
                vfs = VfsFat(sdcard)
                dmtex("SD mount attempted")
                mount(vfs, "/LjinuxRoot")
                sdcard_fs = True
            except NameError:
                dmtex("SD libraries not present, aborting.")
            del spi
            del cs
            try:
                del sdcard
                del vfs
            except NameError:
                pass

        def left_key():
            return ljinux.io.buttonl.value

        def right_key():
            return ljinux.io.buttonr.value

        def enter_key():
            return ljinux.io.buttone.value

        def get_sdcard_fs():
            return str(sdcard_fs)

        def get_uptime():
            return str("%.5f" % (uptimee + time.monotonic()))

        def get_temp():
            return str("%.2f" % cpu.temperature)

        def get_display_status():
            return str(display_availability)

        def get_mem_free():
            return str(gc.mem_free())

        def get_freq():
            return str(cpu.frequency)

        def get_implementation_version():
            return ljinux.based.system_vars["IMPLEMENTATION"]

        def get_implementation():
            return implementation.name

        def get_volt():
            return str(cpu.voltage)

        sys_getters = {
            "sdcard": get_sdcard_fs,
            "uptime": get_uptime,
            "temperature": get_temp,
            "display-attached": get_display_status,
            "memory": get_mem_free,
            "implementation_version": get_implementation_version,
            "implementation": get_implementation,
            "frequency": get_freq,
            "voltage": get_volt,
        }

    class networking:
        wsgiServer = None

        def get_content_type(filee):
            ext = filee.split(".")[-1]
            if ext in ("html", "htm"):
                return "text/html"
            if ext == "js":
                return "application/javascript"
            if ext == "css":
                return "text/css"
            if ext in ("jpg", "jpeg"):
                return "image/jpeg"
            if ext == "png":
                return "image/png"
            return "text/plain"

        def serve_file(file_path):
            return (
                "200 OK",
                [("Content-Type", ljinux.networking.get_content_type(file_path))],
                ljinux.io.get_static_file(file_path),
            )

        def timeset():
            if ljinux.networking.test():
                try:
                    dmtex(
                        "IP lookup worldtimeapi.org: %s"
                        % ljinux.io.network.pretty_ip(
                            ljinux.io.network.get_host_by_name("worldtimeapi.org")
                        )
                    )
                    r = requests.get(
                        "http://worldtimeapi.org/api/timezone/Europe/Athens"
                    )
                    dat = r.json()
                    dmtex("Public IP: " + dat["client_ip"])
                    dst = 1 if dat["dst"] == "True" else 0
                    nettime = time.struct_time(
                        (
                            int(dat["datetime"][:4]),
                            int(dat["datetime"][5:7]),
                            int(dat["datetime"][8:10]),
                            int(dat["datetime"][11:13]),
                            int(dat["datetime"][14:16]),
                            int(dat["datetime"][17:19]),
                            int(dat["day_of_week"]),
                            int(dat["day_of_year"]),
                            dst,
                        )
                    )
                    rtcc.write_datetime(nettime)
                    del nettime
                    dmtex("Network time set for " + dat["abbreviation"])
                    del dat
                    r.close()
                except (ValueError, AssertionError):
                    dmtex("Failed to fetch time data")
            else:
                dmtex("Network unavailable")

        def test():
            if ljinux.io.network_online and not ljinux.io.network.link_status:
                ljinux.io.network_online = False
                ljinux.io.network_name = "Offline"
                dmtex("Network connection lost")
                return False
            return True

        def resolve():
            ljinux.networking.test()
            if ljinux.io.network_online:
                pass  # wip
            else:
                ljinux.based.error(5)

        def packet(data):
            ljinux.networking.test()
            if ljinux.io.network_online:
                pass  # same
            else:
                ljinux.based.error(5)

    class based:
        silent = False

        user_vars = {
            "history-file": "/LjinuxRoot/home/pi/.history",
            "return": "0",
        }

        system_vars = {
            "USER": "root",
            "SECURITY": "off",
            "Init-type": "oneshot",
            "HOSTNAME": "pico",
            "TERM": "xterm-256color",
            "LANG": "en_GB.UTF-8",
            "BOARD": board.board_id.replace("_", " "),
            "IMPLEMENTATION": ".".join(map(str, list(implementation.version))),
        }

        def get_bins():
            try:
                return [
                    dirr[:-4]
                    for dirr in listdir("/LjinuxRoot/bin")
                    if dirr.endswith(".lja") and not dirr.startswith(".")
                ]
            except OSError:  # Yea no root, we cope
                return list()

        class shellfuncs:
            historypos = 0

            def history_movement(action):
                pass

        def error(wh=3, f=None):
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
                4: "'{}': No such file or directory".format(f),
                5: "Network unavailable",
                6: "Display not attached",
                7: "Filesystem unwritable, board in developer mode",
                8: "Missing files",
                9: "Missing arguments",
                10: "File exists",
            }
            print("based: " + errs[wh])
            ljinux.io.ledset(1)  # idle
            del errs

        def autorun():
            ljinux.io.ledset(3)  # act
            global Exit
            global Exit_code
            global Version

            ljinux.based.system_vars["VERSION"] = Version

            print(
                "Welcome to lJinux wannabe Kernel {}!\n\n".format(
                    ljinux.based.system_vars["VERSION"]
                ),
                end="",
            )

            time.sleep(0.6)  # it's iconic staying here for a bit
            try:
                systemprints(2, "Mount /LjinuxRoot")
                ljinux.io.start_sdcard()
                systemprints(1, "Mount /LjinuxRoot")
            except OSError:
                systemprints(
                    3,
                    "Mount /LjinuxRoot",
                    "Error: sd card not available, assuming built in fs",
                )
                del modules["adafruit_sdcard"]
                dmtex("Unloaded sdio libraries")
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
            Exit_code = 0  # resetting, in case we are the 2nd .shell
            try:
                ljinux.io.ledset(3)  # act
                ljinux.based.command.execc(["/LjinuxRoot/boot/Init.lja"])
                systemprints(1, "Running Init Script")
            except OSError:
                systemprints(3, "Running Init Script")
            ljinux.history.load(ljinux.based.user_vars["history-file"])
            systemprints(1, "History Reload")
            if ljinux.based.system_vars["Init-type"] == "oneshot":
                systemprints(1, "Init complete")
            elif ljinux.based.system_vars["Init-type"] == "reboot-repeat":
                Exit = True
                Exit_code = 245
                print("based: Init complete. Restarting")
            elif ljinux.based.system_vars["Init-type"] == "delayed-reboot-repeat":
                try:
                    time.sleep(float(ljinux.based.user_vars["repeat-delay"]))
                except IndexError:
                    print("based: No delay specified! Waiting 60s.")
                    time.sleep(60)
                    Exit = True
                    Exit_code = 245
                    print("based: Init complete and delay finished. Restarting")
            elif ljinux.based.system_vars["Init-type"] == "oneshot-quit":
                Exit = True
                Exit_code = 244
                print("based: Init complete. Halting")
            elif ljinux.based.system_vars["Init-type"] == "repeat":
                try:
                    while not Exit:
                        for commandd in lines:
                            ljinux.based.shell(commandd)

                        if ljinux.io.buttonl.value and ljinux.io.buttonr.value:
                            time.sleep(0.5)
                            Exit = True
                            Exit_code = 244

                except KeyboardInterrupt:
                    print("based: Caught Ctrl + C")
            elif ljinux.based.system_vars["Init-type"] == "delayed-repeat":
                try:
                    time.sleep(float(ljinux.based.user_vars["repeat-delay"]))
                except IndexError:
                    print("based: No delay specified! Waiting 60s.")
                    time.sleep(60)
                try:
                    while not Exit:
                        for commandd in lines:
                            ljinux.based.shell(commandd)

                        if ljinux.io.buttonl.value and ljinux.io.buttonr.value:
                            time.sleep(0.5)
                            Exit = True
                            Exit_code = 244

                except KeyboardInterrupt:
                    print("based: Caught Ctrl + C")
            else:
                print("based: Init-type specified incorrectly, assuming oneshot")
            ljinux.io.ledset(1)  # idle
            while not Exit:
                try:
                    ljinux.based.shell()
                except KeyboardInterrupt:
                    stdout.write("^C\n")
            Exit = False  # to allow ljinux.based.shell to be rerun
            return Exit_code

        class command:
            def not_found(errr):  # command not found
                print("based: " + errr[0] + ": command not found")
                ljinux.based.user_vars["return"] = "1"

            def execc(argj):
                """
                Execution script
                """
                global Exit
                global Exit_code

                if argj[0] == "exec":
                    argj = argj[1:]

                try:
                    with open(argj[0], "r") as filee:

                        for j in filee:
                            j = j.strip()

                            ljinux.based.shell(
                                'argj = "{}"'.format(" ".join([str(i) for i in argj])),
                                led=False,
                            )
                            ljinux.based.shell(j, led=False)

                            del j
                except OSError:
                    ljinux.based.error(4, argj[0])

            def helpp(dictt):  # help
                print(
                    "LNL based\nThese shell commands are defined internally or are in PATH. Type `help' to see this list."
                )  # shameless
                j = 0
                for (
                    i
                ) in (
                    dictt.keys()
                ):  # the passed dict keys is the list of based internal keys
                    if j < 2:
                        print(
                            i, end="                 ".replace(" ", "", len(i))
                        )  # basically the 3 wide collumn
                        j += 1
                    else:
                        print(i)  # this gives us \n
                        j = 0
                try:
                    l = ljinux.based.get_bins()
                    for i in l:
                        if j < 2:
                            print(
                                i, end="                 ".replace(" ", "", len(i))
                            )  # basically the 3 wide collumn
                            j += 1
                        else:
                            print(i)  # this gives us a very needed \n
                            j = 0
                    del l
                    print("\n", end="")
                except OSError:  # Yea no root, we cope
                    pass

            def var(inpt, user_vars, system_vars):  # system & user variables setter
                valid = True
                if inpt[0] == "var":
                    temp = inpt
                    del inpt
                    inpt = []
                    for i in range(len(temp) - 1):
                        inpt.append(temp[i + 1])
                try:
                    for chh in inpt[0]:
                        if not (chh.islower() or chh.isupper() or chh == "-"):
                            valid = False
                    if inpt[1] == "=":
                        if not (
                            inpt[2].startswith('"')
                            or inpt[2].isdigit()
                            or inpt[2].startswith("/")
                        ):
                            valid = False
                    else:
                        valid = False
                    if valid:
                        new_var = ""
                        if inpt[2].startswith('"'):
                            countt = len(inpt)
                            if inpt[2].endswith('"'):
                                new_var = str(inpt[2])[1:-1]
                            elif (countt > 3) and (inpt[countt - 1].endswith('"')):
                                new_var += str(inpt[2])[1:] + " "
                                for i in range(3, countt - 1):
                                    new_var += inpt[i] + " "
                                new_var += str(inpt[countt - 1])[:-1]
                            else:
                                ljinux.based.error(1)
                                valid = False
                        else:
                            new_var += str(inpt[2])
                    else:
                        ljinux.based.error(1)
                        valid = False
                    if valid:
                        if inpt[0] in system_vars:
                            if not (system_vars["SECURITY"] == "on"):
                                system_vars[inpt[0]] = new_var
                            else:
                                print(
                                    "Cannot edit system variables, security is enabled."
                                )
                        else:
                            user_vars[inpt[0]] = new_var
                except IndexError:
                    ljinux.based.error(1)

            def display(inpt, objectss):  # the graphics drawing stuff
                typee = inpt[
                    1
                ]  # "text / pixel / rectangle / line / circle / triangle / fill"
                if typee == "text":  # x, y, color, text in ""
                    try:
                        xi = 0
                        xi = ljinux.based.fn.adv_input(inpt[2], int)
                        yi = ljinux.based.fn.adv_input(inpt[3], int)
                        txt = ""  # inpt[5]
                        col = ljinux.based.fn.adv_input(inpt[4], int)
                        if inpt[5].startswith('"'):  # let's do some string proccessing!
                            countt = len(inpt)  # get the numb of args
                            if countt > 6:
                                txt += (
                                    str(inpt[5])[1:] + " "
                                )  # get the first word, remove last char (")
                                if inpt[countt - 1].endswith('"'):
                                    for i in range(
                                        6, countt - 1
                                    ):  # make all the words one thicc string
                                        txt += str(inpt[i]) + " "
                                    txt += str(inpt[countt - 1])[
                                        :-1
                                    ]  # last word without last char (")
                                else:
                                    print("based: Input error")
                            else:
                                txt += str(inpt[5])[1:-1]
                        else:
                            print("based: Input error")
                        ljinux.farland.text(txt, xi, yi, col)
                    except ValueError:
                        print("based: Input error")
                elif typee == "dot":  # x,y,col
                    try:
                        xi = ljinux.based.fn.adv_input(inpt[2], int)
                        yi = ljinux.based.fn.adv_input(inpt[3], int)
                        col = ljinux.based.fn.adv_input(inpt[4], int)
                        ljinux.farland.pixel(xi, yi, col)
                    except ValueError:
                        print("based: Input error")
                elif (
                    typee == "rectangle"
                ):  # x start, y start, x stop, y stop, color, mode (fill / border)
                    try:
                        xi = ljinux.based.fn.adv_input(inpt[2], int)
                        yi = ljinux.based.fn.adv_input(inpt[3], int)
                        xe = ljinux.based.fn.adv_input(inpt[4], int)
                        ye = ljinux.based.fn.adv_input(inpt[5], int)
                        col = ljinux.based.fn.adv_input(inpt[6], int)
                        modd = ljinux.based.fn.adv_input(inpt[7], str)
                        ljinux.farland.rect(xi, yi, xe, ye, col, modd)
                    except ValueError:
                        print("based: Input error")
                elif typee == "line":  # x start, y start, x stop, y stop, color
                    try:
                        xi = ljinux.based.fn.adv_input(inpt[2], int)
                        yi = ljinux.based.fn.adv_input(inpt[3], int)
                        xe = ljinux.based.fn.adv_input(inpt[4], int)
                        ye = ljinux.based.fn.adv_input(inpt[5], int)
                        col = ljinux.based.fn.adv_input(inpt[6], int)
                        ljinux.farland.line(xi, yi, xe, ye, col)
                    except ValueError:
                        print("based: Input error")
                elif (
                    typee == "circle"
                ):  # x center, y center, rad, color, mode (fill/ border / template) TODO fix fill and do template
                    try:
                        xi = ljinux.based.fn.adv_input(inpt[2], int)
                        yi = ljinux.based.fn.adv_input(inpt[3], int)
                        radd = ljinux.based.fn.adv_input(inpt[4], int)
                        col = ljinux.based.fn.adv_input(inpt[5], int)
                        modd = ljinux.based.fn.adv_input(inpt[6], int)
                        if modd != "fill":
                            ljinux.farland.draw_circle(xi, yi, radd, col)
                        else:
                            ljinux.farland.f_draw_circle(xi, yi, radd, col)
                    except ValueError:
                        print("based: Input error")
                elif (
                    typee == "triangle"
                ):  # x point 1, y point 1, x point 2, y point 2, x point 3, y point 3, color, mode (fill/ border)
                    try:
                        xi = ljinux.based.fn.adv_input(inpt[2], int)
                        yi = ljinux.based.fn.adv_input(inpt[3], int)
                        xe = ljinux.based.fn.adv_input(inpt[4], int)
                        ye = ljinux.based.fn.adv_input(inpt[5], int)
                        xz = ljinux.based.fn.adv_input(inpt[6], int)
                        yz = ljinux.based.fn.adv_input(inpt[7], int)
                        col = ljinux.based.fn.adv_input(inpt[8], int)
                        modd = ljinux.based.fn.adv_input(inpt[9], str)
                        ljinux.farland.line(xi, yi, xe, ye, col)
                        ljinux.farland.line(xi, yi, xz, yz, col)
                        ljinux.farland.line(xz, yz, xe, ye, col)
                        if modd == "fill":
                            templ = ljinux.farland.virt_line(xi, yi, xe, ye)
                            for i in templ:
                                ljinux.farland.ext_line(xz, yz, i[0], i[1], col)
                    except ValueError:
                        print("based: Input error")
                elif typee == "fill":  # color
                    try:
                        col = ljinux.based.fn.adv_input(inpt[2], int)
                        ljinux.farland.fill(col)
                    except ValueError:
                        print("based: Input error")
                elif typee == "rhombus":  # todo
                    pass
                elif typee == "move":  # todo
                    pass
                elif typee == "delete":  # todo more
                    optt = ljinux.based.fn.adv_input(inpt[2], int)
                    if optt == "all":
                        ljinux.farland.clear()
                    else:
                        ljinux.based.error(1)
                elif typee == "refresh":
                    ljinux.farland.frame()
                else:
                    ljinux.based.error(1)

            def suuu(inpt, system_vars):  # su command but worse
                global dfpasswd
                passwordarr = {}
                try:
                    try:
                        with open("/LjinuxRoot/etc/passwd", "r") as data:
                            lines = data.readlines()
                            for line in lines:
                                dt = line.split()
                                passwordarr[dt[0]] = dt[1]
                                del dt
                            data.close()
                            del lines
                    except OSError:
                        pass
                    if passwordarr["root"] == getpass():
                        system_vars["SECURITY"] = "off"
                        print("Authentication successful. Security disabled.")
                    else:
                        print("Authentication unsuccessful.")

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
                        system_vars["security"] = "off"
                        print("Authentication successful. Security disabled.")
                    else:
                        print("Authentication unsuccessful.")
                try:
                    del passwordarr
                except NameError:
                    pass

            def historgf(inpt):  # history get full list
                try:
                    if inpt[1] == "clear":
                        ljinux.history.clear(ljinux.based.user_vars["history-file"])
                    elif inpt[1] == "load":
                        ljinux.history.load(ljinux.based.user_vars["history-file"])
                    elif inpt[1] == "save":
                        ljinux.history.save(ljinux.based.user_vars["history-file"])
                    else:
                        print("based: Invalid option")
                except IndexError:
                    ljinux.history.getall()

            def iff(inpt):  # the if, the pinnacle of ai WIP
                condition = []
                complete = False
                next_part = None
                if inpt[1] == "[":
                    for i in range(2, len(inpt)):
                        if inpt[i] == "]":
                            complete = True
                            next_part = i + 1
                            break
                        else:
                            condition.append(inpt[i])
                    if complete:
                        try:
                            val = False
                            need_new_cond = False
                            i = 0
                            while i < len(condition) - 1:
                                if condition[i] == "argj":  # this is an argument check
                                    i += 1  # we can move on as we know of the current situation
                                    if (
                                        condition[i] == "has"
                                    ):  # check if condition is present
                                        i += 1  # we have to keep moving
                                        if (
                                            condition[i]
                                            in ljinux.based.user_vars["argj"]
                                        ):  # it's in!
                                            val = True
                                        else:
                                            val = False
                                        need_new_cond = True
                                    elif (
                                        condition[i].startswith('"')
                                        and condition[i].endswith('"')
                                    ) and (
                                        (condition[i + 1] == "is")
                                        or (condition[i + 1] == "==")
                                        or (condition[i + 1] == "=")
                                    ):  # check next arg for name and the one ahead of it for value
                                        namee = condition[i][1:-1]  # remove ""
                                        i += 2
                                        try:
                                            if (
                                                namee in ljinux.based.user_vars["argj"]
                                            ):  # it's in!
                                                pos = ljinux.based.user_vars[
                                                    "argj"
                                                ].find(namee)
                                                sz = len(namee)
                                                nextt = ljinux.based.user_vars["argj"][
                                                    pos + sz + 1 :
                                                ]
                                                cut = nextt.find(" ") + 1
                                                del sz
                                                del pos
                                                if cut is not 0:
                                                    nextt = nextt[: nextt.find(" ") + 1]
                                                del cut
                                                if nextt == condition[i][1:-1]:
                                                    val = True
                                                    need_new_cond = True
                                                else:
                                                    val = False
                                                    need_new_cond = True
                                                i += 1
                                            else:
                                                raise KeyError
                                            del namee
                                        except KeyError:
                                            print("based: Arg not in argj")
                                elif condition[i] == "and":  # and what
                                    i += 1  # just read the argj, i'm not gonna copy the comments
                                    if val == 0:  # no need to keep goin, just break;
                                        break
                                    else:
                                        need_new_cond = False
                                elif condition[i] == "or":  # or what
                                    i += 1
                                    if val == 1:  # no need to keep goin, just break;
                                        break
                                    else:
                                        need_new_cond = False
                                elif condition[i].isdigit():  # meth
                                    i += 1  # todo
                                else:
                                    print("based: Invalid action type: " + condition[i])
                                    break
                            if val == 1:
                                ljinux.based.shell(
                                    " ".join(inpt[next_part:]), led=False
                                )
                            del next_part
                            del val
                        except KeyError:
                            print("based: Invalid condition type")
                    else:
                        print("based: Incomplete condition")
                else:
                    ljinux.based.error(1)
                del need_new_cond
                del complete
                del condition

            def ping(inpt):  # brok
                print("Ping google.com: %d ms" % ljinux.io.network.ping("google.com"))

            def webs(inpt):  # not nginx, more like njinx
                ljinux.networking.test()
                if ljinux.io.network_online:
                    try:
                        pathh = inpt[1]
                    except IndexError:
                        pathh = "/LjinuxRoot/var/www/default/"

                    print("Ljinux Web Server")
                    try:
                        arg = inpt[1]
                    except IndexError:
                        arg = ""
                    if arg != "-k":
                        print("Starting in the backround, send webserver -k to kill.")
                        web_app = WSGIApp()

                        @web_app.route("/")
                        def root(request):
                            global access_log
                            access_log.append("Root accessed")
                            return (
                                "200 OK",
                                [],
                                ljinux.io.get_static_file(pathh + "default.html"),
                            )

                        @web_app.route("/access_log")
                        def root(request):
                            global access_log
                            access_log.append("Accessed log")
                            return ("200 OK", [], [str(access_log)])

                        @web_app.route("/<pagee>")
                        def led_on(request, pagee):
                            global access_log
                            access_log.append("Accessed " + pagee)
                            return ljinux.networking.serve_file(str(pathh + pagee))

                        try:
                            ljinux.networking.wsgiServer = server.WSGIServer(
                                80, application=web_app
                            )
                            ljinux.networking.wsgiServer.start()
                            ljinux.backrounding.webserver = True
                        except RuntimeError:
                            print("Out of sockets, please reboot")
                            return
                    elif ljinux.backrounding.webserver:
                        ljinux.backrounding.webserver = (
                            not ljinux.backrounding.webserver
                        )
                        del ljinux.networking.wsgiServer
                        ljinux.networking.wsgiServer = None
                        print(
                            "Webserver unloaded, keep in mind sockets cannot be reused in the current implementation, and you might have to reboot to restart the webserver."
                        )
                    else:
                        print("Error: Webserver not running")
                else:
                    print("Network unavailable")

            def do_nothin(inpt):
                pass  # really this is needed

            def pexecc(inpt, rc):  # filtered & true source
                global Version
                pcomm = rc.lstrip(rc.split()[0]).replace(" ", "", 1)
                nl = False
                try:
                    if "-n" in inpt[1]:
                        nl = True
                        pcomm = pcomm.lstrip(rc.split()[1]).replace(" ", "", 1)
                except IndexError:
                    ljinux.based.error(9)
                    ljinux.based.user_vars["return"] = "1"
                    return
                if not nl:
                    print(
                        "Adafruit CircuitPython "
                        + str(implementation.version[0])
                        + "."
                        + str(implementation.version[1])
                        + "."
                        + str(implementation.version[2])
                        + " on Ljinux "
                        + Version
                        + "; Raspberry Pi Pico with rp2040\n>>> "
                        + pcomm
                    )
                try:
                    exec(pcomm)
                    del pcomm
                except Exception as err:
                    print(
                        "Traceback (most recent call last):\n\t"
                        + str(type(err))[8:-2]
                        + ": "
                        + str(err)
                    )
                    del err
                del nl

            def fpexecc(inpt):  # file pexec
                global Version
                nl = False
                offs = 1
                try:
                    if "-n" in inpt[1]:
                        nl = True
                        offs = 2
                except IndexError:
                    ljinux.based.error(9)
                    ljinux.based.user_vars["return"] = "1"
                    return
                if not nl:
                    print(
                        "Adafruit CircuitPython "
                        + str(implementation.version[0])
                        + "."
                        + str(implementation.version[1])
                        + "."
                        + str(implementation.version[2])
                        + " on Ljinux "
                        + Version
                        + "; Raspberry Pi Pico with rp2040\nRunning file: "
                        + inpt[offs]
                    )
                try:
                    a = open(inpt[offs]).read()
                    exec(a)
                    del a
                except Exception as err:
                    print(
                        "Traceback (most recent call last):\n\t"
                        + str(type(err))[8:-2]
                        + ": "
                        + str(err)
                    )
                    del err
                del nl
                del offs

        class fn:
            """
            Common functions used by the commands.
            CODE:
                ljinux.based.fn.[function_name](parameters)
            """

            def betterpath(back=None):
                """
                Removes /LjinuxRoot from path and puts it back
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
                        res = "board/"
                    elif a == "/LjinuxRoot":
                        res = "/"
                    elif a.startswith("/LjinuxRoot"):
                        res = a[11:]
                    else:
                        res = "board" + a
                    del a
                else:  # resolve path back to normal
                    if back.startswith("board"):
                        """
                        if the path starts with board/ it means it understands the reality of the fs
                        and we can just ommit the board part
                        """
                        res = back[5:]
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

            def get_valid_options(inpt, vopts):
                """
                Returns an options array if the given parameter start with the character '-'.
                Returns an empty array if there is none, duplicate or invalid character followind '-'.
                Parameters:
                    inpt : string with args, ex: "-n"
                    vopts : string with valid options, ex: "abc"
                """
                opts = []
                i = 1
                try:
                    while i < len(inpt):  # why not "for"?
                        if inpt[i] in vopts:
                            opts.append(inpt[i])
                            vopts = vopts.replace(inpt[i], "")
                            i += 1
                        else:
                            return []
                    del vopts
                except IndexError:
                    pass
                del i
                del inpt
                return opts

            def adv_input(whatever, _type):
                """
                Universal variable request
                Returns the variable's value in the specified type
                Parameters:
                    whatever : The name of the variable
                    _type : The type in which it should be returned
                """
                res = None
                act_dict = {
                    "left_key": ljinux.io.left_key,
                    "right_key": ljinux.io.right_key,
                    "enter_key": ljinux.io.enter_key,
                }
                if whatever.isdigit():
                    res = int(whatever)
                elif whatever in ljinux.based.user_vars:
                    res = ljinux.based.user_vars[whatever]
                elif whatever in ljinux.based.system_vars:
                    res = ljinux.based.system_vars[whatever]
                elif whatever in ljinux.io.sys_getters:
                    res = ljinux.io.sys_getters[whatever]()
                elif whatever in act_dict:
                    res = act_dict[whatever]()
                else:
                    raise ValueError("Could not be found in Ljinux lists")
                return _type(res)

        def shell(
            inp=None,
            led=True,
        ):  # the shell function, warning do not touch, it has feelings - no I think I will 20/3/22
            global Exit
            function_dict = {  # holds all built-in commands. The plan is to move as many as possible externally
                "error": ljinux.based.command.not_found,
                "exec": ljinux.based.command.execc,
                "help": ljinux.based.command.helpp,
                "var": ljinux.based.command.var,
                "display": ljinux.based.command.display,
                "su": ljinux.based.command.suuu,
                "history": ljinux.based.command.historgf,
                "if": ljinux.based.command.iff,
                "ping": ljinux.based.command.ping,
                "webserver": ljinux.based.command.webs,
                "pexec": ljinux.based.command.pexecc,
                "COMMENT": ljinux.based.command.do_nothin,
                "fpexec": ljinux.based.command.fpexecc,
            }
            command_input = False
            if not term.enabled:
                ljinux.io.ledset(4)  # waiting for serial
                term.start()
                ljinux.io.ledset(1)  # idle
                term.trigger_dict = {
                    "inp_type": "prompt",
                    "enter": 0,
                    "ctrlC": 1,
                    "ctrlD": 2,
                    "tab": 3,
                    "up": 4,
                    "down": 7,
                    "rest": "stack",
                    "rest_a": "common",
                    "echo": "common",
                }
            if not Exit:
                while (
                    (command_input == False) or (command_input == "\n")
                ) and not Exit:
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
                        + ljinux.based.fn.betterpath()
                        + colors.endc
                        + "]"
                        + colors.blue_t
                        + ">"
                        + colors.endc
                    )
                    if inp is None:
                        command_input = False
                        while (command_input in [False, ""]) and not Exit:
                            try:
                                term.program()
                                if term.buf[0] is 0:
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
                                    global Exit
                                    global Exit_code
                                    Exit = True
                                    Exit_code = 0
                                    ljinux.io.ledset(1)  # idle
                                    break
                                elif term.buf[0] is 3:  # tab key
                                    ljinux.io.ledset(2)  # keyact
                                    tofind = term.buf[
                                        1
                                    ]  # made into var for speed reasons
                                    candidates = []
                                    bins = ljinux.based.get_bins()
                                    for i in [function_dict, bins]:
                                        for j in i:
                                            if j.startswith(tofind):
                                                candidates.append(j)
                                    if len(candidates) > 1:
                                        stdout.write("\n")
                                        for i in candidates:
                                            print("\t" + i)
                                    elif len(candidates) == 1:
                                        term.clear_line()
                                        term.buf[1] = candidates[0]
                                        term.focus = 0
                                    else:
                                        term.clear_line()
                                    del bins
                                    del tofind
                                    del candidates
                                    ljinux.io.ledset(1)  # idle
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
                                    ljinux.io.ledset(1)  # idle
                                ljinux.backrounding.main_tick()
                                try:
                                    if command_input[:1] != " " and command_input != "":
                                        ljinux.history.appen(command_input.strip())
                                except (
                                    AttributeError,
                                    TypeError,
                                ):  # idk why this is here, forgor
                                    pass
                            except KeyboardInterrupt:  # duplicate code as by ^C^C you could escape somehow
                                print("^C")
                                term.buf[1] = ""
                                term.focus = 0
                                term.clear_line()
                    else:
                        command_input = inp
                if not Exit:
                    res = ""
                    if led:
                        ljinux.io.ledset(3)  # act
                    if not (command_input == ""):
                        gc.collect()
                        gc.collect()
                        if (not "|" in command_input) and (not "&&" in command_input):
                            command_split = (
                                command_input.split()
                            )  # making it an arr of words
                            try:
                                if str(command_split[0])[:2] == "./":
                                    command_split[0] = str(command_split[0])[2:]
                                    if command_split[0] != "":
                                        res = function_dict["exec"](command_split)
                                    else:
                                        print("Error: No file specified")
                                elif (command_split[0] in function_dict) and (
                                    command_split[0]
                                    not in [
                                        "error",
                                        "var",
                                        "help",
                                        "display",
                                        "su",
                                        "pexec",
                                    ]
                                ):  # those are special bois, they will not be special when I make the api great
                                    res = function_dict[command_split[0]](command_split)
                                elif command_split[0] == "pexec":
                                    res = function_dict["pexec"](
                                        command_split, command_input
                                    )
                                elif command_split[0] == "help":
                                    res = function_dict["help"](function_dict)
                                elif command_split[0] == "display":
                                    global display_availability
                                    if display_availability:
                                        res = function_dict["display"](
                                            command_split, ljinux.farland.entities
                                        )
                                    else:
                                        ljinux.based.error(6)
                                elif command_split[0] == "su":
                                    res = function_dict["su"](
                                        command_split, ljinux.based.system_vars
                                    )
                                elif (command_split[1] == "=") or (
                                    command_split[0] == "var"
                                ):
                                    res = function_dict["var"](
                                        command_split,
                                        ljinux.based.user_vars,
                                        ljinux.based.system_vars,
                                    )
                                else:
                                    raise IndexError
                            except IndexError:
                                bins = ljinux.based.get_bins()
                                certain = False
                                for i in bins:
                                    if (
                                        command_split[0] == i
                                    ) and not certain:  # check if currently examined file is same as command
                                        command_split[0] = (
                                            "/LjinuxRoot/bin/" + i + ".lja"
                                        )  # we have to fill in the full path
                                        certain = True
                                del bins  # we no longer need the list
                                if certain:
                                    res = function_dict["exec"](command_split)
                                else:
                                    res = function_dict["error"](command_split)
                                del certain
                        elif ("|" in command_input) and not (
                            "&&" in command_input
                        ):  # this is a pipe  :)
                            ljinux.based.silent = True
                            the_pipe_pos = command_input.find("|", 0)
                            ljinux.based.shell(
                                command_input[: the_pipe_pos - 1], led=False
                            )
                            ljinux.based.silent = False
                            ljinux.based.shell(
                                command_input[the_pipe_pos + 2 :]
                                + " "
                                + ljinux.based.user_vars["return"],
                                led=False,
                            )
                            del the_pipe_pos
                        elif ("&&" in command_input) and not (
                            "|" in command_input
                        ):  # this is a dirty pipe  :)
                            the_pipe_pos = command_input.find("&&", 0)
                            ljinux.based.shell(
                                command_input[: the_pipe_pos - 1], led=False
                            )
                            ljinux.based.shell(
                                command_input[the_pipe_pos + 2 :], led=False
                            )
                            del the_pipe_pos
                        elif ("&&" in command_input) and (
                            "|" in command_input
                        ):  # this pipe was used to end me :(
                            the_pipe_pos_1 = command_input.find("|", 0)
                            the_pipe_pos_2 = command_input.find("&&", 0)
                            if the_pipe_pos_1 < the_pipe_pos_2:  # the first pipe is a |
                                ljinux.based.silent = True
                                ljinux.based.shell(command_input[: the_pipe_pos_1 - 1])
                                ljinux.based.silent = False
                                ljinux.based.shell(
                                    command_input[the_pipe_pos_1 + 2 :]
                                    + " "
                                    + ljinux.based.user_vars["return"]
                                )
                            else:  # the first pipe is a &&
                                ljinux.based.shell(
                                    command_input[: the_pipe_pos_2 - 1], led=False
                                )
                                ljinux.based.shell(
                                    command_input[the_pipe_pos_2 + 2 :], led=False
                                )
                            del the_pipe_pos_1
                            del the_pipe_pos_2
                        else:
                            pass
                    if led:
                        ljinux.io.ledset(1)  # idle
                    gc.collect()
                    gc.collect()
                    return res

    class farland:  # wayland, but like a farfetched dream
        # the screen holder
        oled = None
        # the time variables
        timm_old = 0
        tp = [0, 0, 0, -1]
        poss = [0, 6, 16, 22, 11]
        poin = False
        offs = 50
        # fps stuff
        time_old = time.monotonic()
        time_new = None
        frames = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        frame_poi = 0
        frames_suff = False
        # the display objects
        entities = []  # it will hold the drawn objects and allow their dynamic deletion
        # ---

        def setup():
            global display_availability
            ljinux.io.ledset(3)  # act
            try:
                i2c = busio.I2C(
                    pintab[configg["displaySCL"]], pintab[configg["displaySDA"]]
                )  # SCL, SDA
                ljinux.farland.oled = adafruit_ssd1306.SSD1306_I2C(
                    128, 64, i2c
                )  # I use the i2c cuz it ez
                del i2c
                ljinux.farland.oled.fill(0)  # cuz why not
                ljinux.farland.oled.show()
                display_availability = True
            except (RuntimeError, KeyError, NameError):
                print(
                    "Failed to create display object, display functions will be unavailable"
                )
                try:
                    del modules["adafruit_ssd1306"]
                    del modules["adafruit_framebuf"]
                except KeyError:
                    pass
                dmtex("Unloaded display libraries")
            ljinux.io.ledset(1)  # idle

        def frame():
            global display_availability
            if display_availability:
                ljinux.farland.oled.show()

        def clear():
            global display_availability
            if display_availability:
                ljinux.farland.oled.fill(0)
                ljinux.farland.oled.show()

        def pixel(x, y, col):
            ljinux.farland.oled.pixel(x, y, col)

        def fill(col):
            ljinux.farland.oled.fill(col)

        def text(strr, x, y, col):
            ljinux.farland.oled.text(strr, x, y, col, font_name="/font5x8.bin")

        # getters
        def height():
            return int(ljinux.farland.oled.height)

        def width():
            return int(ljinux.farland.oled.width)

        # privitive graphics
        def draw_circle(xpos0, ypos0, rad, col):
            x = rad - 1
            top_l = None
            top_r = None
            bot_l = None
            bot_r = None
            y = 0
            dx = 1
            dy = 1
            err = dx - (rad << 1)
            while x >= y:
                ljinux.farland.oled.pixel(xpos0 + x, ypos0 + y, col)
                ljinux.farland.oled.pixel(xpos0 + y, ypos0 + x, col)
                ljinux.farland.oled.pixel(xpos0 - y, ypos0 + x, col)
                ljinux.farland.oled.pixel(xpos0 - x, ypos0 + y, col)
                ljinux.farland.oled.pixel(xpos0 - x, ypos0 - y, col)
                ljinux.farland.oled.pixel(xpos0 - y, ypos0 - x, col)
                ljinux.farland.oled.pixel(xpos0 + y, ypos0 - x, col)
                ljinux.farland.oled.pixel(xpos0 + x, ypos0 - y, col)
                if err <= 0:
                    y += 1
                    err += dy
                    dy += 2
                if err > 0:
                    x -= 1
                    dx += 2
                    err += dx - (rad << 1)

        def f_draw_circle(xpos0, ypos0, rad, col):
            rad -= 1
            y = -rad
            while y <= rad:
                x = -rad
                while x <= rad:
                    if (x * 2 + y * 2) < (rad * rad + rad * 0.8):
                        ljinux.farland.oled.pixel(xpos0 + x, ypos0 + y, col)
                        # setpixel(origin.x+x, origin.y+y)
                    x += 1
                y += 1

        def draw_top():  # to be made into an app
            for i in range(128):
                for j in range(11):
                    ljinux.farland.oled.pixel(i, j, True)

        def line(x0, y0, x1, y1, col):
            dx = abs(x1 - x0)
            dy = abs(y1 - y0)
            x, y = x0, y0
            sx = -1 if x0 > x1 else 1
            sy = -1 if y0 > y1 else 1
            if dx > dy:
                err = dx / 2.0
                while x != x1:
                    ljinux.farland.oled.pixel(int(x), int(y), col)
                    err -= dy
                    if err < 0:
                        y += sy
                        err += dx
                    x += sx
            else:
                err = dy / 2.0
                while y != y1:
                    ljinux.farland.oled.pixel(int(x), int(y), col)
                    err -= dx
                    if err < 0:
                        x += sx
                        err += dy
                    y += sy
                ljinux.farland.oled.pixel(int(x), int(y), col)

        def ext_line(x0, y0, x1, y1, col):
            dx = abs(x1 - x0)
            dy = abs(y1 - y0)
            x, y = x0, y0
            sx = -1 if x0 > x1 else 1
            sy = -1 if y0 > y1 else 1
            if dx > dy:
                err = dx / 2.0
                while x != x1:
                    ljinux.farland.oled.pixel(int(x), int(y), col)
                    ljinux.farland.oled.pixel(int(x) + 1, int(y), col)
                    ljinux.farland.oled.pixel(int(x) - 1, int(y), col)
                    ljinux.farland.oled.pixel(int(x), int(y) + 1, col)
                    ljinux.farland.oled.pixel(int(x), int(y) - 1, col)
                    err -= dy
                    if err < 0:
                        y += sy
                        err += dx
                    x += sx
            else:
                err = dy / 2.0
                while y != y1:
                    ljinux.farland.oled.pixel(int(x), int(y), col)
                    if not isInteger(x):
                        ljinux.farland.oled.pixel(int(x) + 1, int(y), col)
                        ljinux.farland.oled.pixel(int(x) - 1, int(y), col)
                    if not isInteger(y):
                        ljinux.farland.oled.pixel(int(x), int(y) + 1, col)
                        ljinux.farland.oled.pixel(int(x), int(y) - 1, col)
                    err -= dx
                    if err < 0:
                        x += sx
                        err += dy
                    y += sy
                ljinux.farland.oled.pixel(int(x), int(y), col)
                if not isInteger(x):
                    ljinux.farland.oled.pixel(int(x) + 1, int(y), col)
                    ljinux.farland.oled.pixel(int(x) - 1, int(y), col)
                if not isInteger(y):
                    ljinux.farland.oled.pixel(int(x), int(y) + 1, col)
                    ljinux.farland.oled.pixel(int(x), int(y) - 1, col)

        def virt_line(x0, y0, x1, y1):
            virt_l_tab = []
            dx = abs(x1 - x0)
            dy = abs(y1 - y0)
            x, y = x0, y0
            sx = -1 if x0 > x1 else 1
            sy = -1 if y0 > y1 else 1
            if dx > dy:
                err = dx / 2.0
                while x != x1:
                    virt_l_tab.append([int(x), int(y)])
                    err -= dy
                    if err < 0:
                        y += sy
                        err += dx
                    x += sx
            else:
                err = dy / 2.0
                while y != y1:
                    virt_l_tab.append([int(x), int(y)])
                    err -= dx
                    if err < 0:
                        x += sx
                        err += dy
                    y += sy
                virt_l_tab.append([int(x), int(y)])
            return virt_l_tab

        def rect(x0, y0, x1, y1, col, modee):
            if modee == "border":
                if x0 < x1:
                    for i in range(x0, x1):
                        ljinux.farland.oled.pixel(i, y0, col)
                        ljinux.farland.oled.pixel(i, y1, col)
                else:
                    for i in range(x1, x0):
                        ljinux.farland.oled.pixel(i, y0, col)
                        ljinux.farland.oled.pixel(i, y1, col)
                if y0 < y1:
                    for i in range(y0, y1):
                        ljinux.farland.oled.pixel(x0, i, col)
                        ljinux.farland.oled.pixel(x1, i, col)
                else:
                    for i in range(x1, x0):
                        ljinux.farland.oled.pixel(x0, i, col)
                        ljinux.farland.oled.pixel(x1, i, col)
            elif modee == "fill":
                if (x0 < x1) and (y0 < y1):
                    for i in range(x0, x1):
                        for j in range(y0, y1):
                            ljinux.farland.oled.pixel(i, j, col)
                elif (x0 < x1) and (y1 > y0):
                    for i in range(x0, x1):
                        for j in range(y0, y1, -1):
                            ljinux.farland.oled.pixel(i, j, col)
                elif (x0 > x1) and (y1 < y0):
                    for i in range(x0, x1, -1):
                        for j in range(y0, y1):
                            ljinux.farland.oled.pixel(i, j, col)
                elif (x0 > x1) and (y1 > y0):
                    for i in range(x0, x1, -1):
                        for j in range(y0, y1, -1):
                            ljinux.farland.oled.pixel(i, j, col)
                else:
                    ljinux.based.error(1)

        # clock functions, to be made part of hs

        # init the clock
        def draw_init_clock():
            ljinux.farland.oled.text(
                "0", ljinux.farland.poss[0] + ljinux.farland.offs, 2, False
            )
            ljinux.farland.oled.text(
                "0", ljinux.farland.poss[1] + ljinux.farland.offs, 2, False
            )
            ljinux.farland.oled.text(
                "0", ljinux.farland.poss[2] + ljinux.farland.offs, 2, False
            )
            ljinux.farland.oled.text(
                "0", ljinux.farland.poss[3] + ljinux.farland.offs, 2, False
            )

        # each time increments if monotonic has gone up
        def draw_clock():
            ljinux.farland.timm_in = int(time.monotonic())
            if ljinux.farland.timm_in != ljinux.farland.timm_old:
                ljinux.farland.timm_old = ljinux.farland.timm_in
                if ljinux.farland.tp[3] != 9:
                    ljinux.farland.oled.text(
                        str(ljinux.farland.tp[3]),
                        ljinux.farland.poss[3] + ljinux.farland.offs,
                        2,
                        True,
                    )
                    ljinux.farland.tp[3] += 1
                    ljinux.farland.oled.text(
                        str(ljinux.farland.tp[3]),
                        ljinux.farland.poss[3] + ljinux.farland.offs,
                        2,
                        False,
                    )
                elif ljinux.farland.tp[2] != 5:
                    ljinux.farland.oled.text(
                        str(ljinux.farland.tp[3]),
                        ljinux.farland.poss[3] + ljinux.farland.offs,
                        2,
                        True,
                    )
                    ljinux.farland.tp[3] = 0
                    ljinux.farland.oled.text(
                        str(ljinux.farland.tp[3]),
                        ljinux.farland.poss[3] + ljinux.farland.offs,
                        2,
                        False,
                    )
                    ljinux.farland.oled.text(
                        str(ljinux.farland.tp[2]),
                        ljinux.farland.poss[2] + ljinux.farland.offs,
                        2,
                        True,
                    )
                    ljinux.farland.tp[2] += 1
                    ljinux.farland.oled.text(
                        str(ljinux.farland.tp[2]),
                        ljinux.farland.poss[2] + ljinux.farland.offs,
                        2,
                        False,
                    )
                elif ljinux.farland.tp[1] != 9:
                    ljinux.farland.oled.text(
                        str(ljinux.farland.tp[3]),
                        ljinux.farland.poss[3] + ljinux.farland.offs,
                        2,
                        True,
                    )
                    ljinux.farland.tp[3] = 0
                    ljinux.farland.oled.text(
                        str(ljinux.farland.tp[3]),
                        ljinux.farland.poss[3] + ljinux.farland.offs,
                        2,
                        False,
                    )
                    ljinux.farland.oled.text(
                        str(ljinux.farland.tp[2]),
                        ljinux.farland.poss[2] + ljinux.farland.offs,
                        2,
                        True,
                    )
                    ljinux.farland.tp[2] = 0
                    ljinux.farland.oled.text(
                        str(ljinux.farland.tp[2]),
                        ljinux.farland.poss[2] + ljinux.farland.offs,
                        2,
                        False,
                    )
                    ljinux.farland.oled.text(
                        str(ljinux.farland.tp[1]),
                        ljinux.farland.poss[1] + ljinux.farland.offs,
                        2,
                        True,
                    )
                    ljinux.farland.tp[1] += 1
                    ljinux.farland.oled.text(
                        str(ljinux.farland.tp[1]),
                        ljinux.farland.poss[1] + ljinux.farland.offs,
                        2,
                        False,
                    )
                elif ljinux.farland.tp[0] != 5:
                    ljinux.farland.oled.text(
                        str(ljinux.farland.tp[3]),
                        ljinux.farland.poss[3] + ljinux.farland.offs,
                        2,
                        True,
                    )
                    ljinux.farland.tp[3] = 0
                    ljinux.farland.oled.text(
                        str(ljinux.farland.tp[3]),
                        ljinux.farland.poss[3] + ljinux.farland.offs,
                        2,
                        False,
                    )
                    ljinux.farland.oled.text(
                        str(ljinux.farland.tp[2]),
                        ljinux.farland.poss[2] + ljinux.farland.offs,
                        2,
                        True,
                    )
                    ljinux.farland.tp[2] = 0
                    ljinux.farland.oled.text(
                        str(ljinux.farland.tp[2]),
                        ljinux.farland.poss[2] + ljinux.farland.offs,
                        2,
                        False,
                    )
                    ljinux.farland.oled.text(
                        str(ljinux.farland.tp[1]),
                        ljinux.farland.poss[1] + ljinux.farland.offs,
                        2,
                        True,
                    )
                    ljinux.farland.tp[1] = 0
                    ljinux.farland.oled.text(
                        str(ljinux.farland.tp[1]),
                        ljinux.farland.poss[1] + ljinux.farland.offs,
                        2,
                        False,
                    )
                    ljinux.farland.oled.text(
                        str(ljinux.farland.tp[0]),
                        ljinux.farland.poss[0] + ljinux.farland.offs,
                        2,
                        True,
                    )
                    ljinux.farland.tp[0] += 1
                    ljinux.farland.oled.text(
                        str(ljinux.farland.tp[0]),
                        ljinux.farland.poss[0] + ljinux.farland.offs,
                        2,
                        False,
                    )
                ljinux.farland.poin = not (ljinux.farland.poin)
                ljinux.farland.oled.text(
                    ":",
                    ljinux.farland.poss[4] + ljinux.farland.offs,
                    2,
                    ljinux.farland.poin,
                )

        def fps():
            if ljinux.farland.frame_poi <= 9:
                ljinux.farland.time_new = time.monotonic()
                ljinux.farland.frames[ljinux.farland.frame_poi] = (
                    ljinux.farland.time_new - ljinux.farland.time_old
                )
                ljinux.farland.time_old = time.monotonic()
                if ljinux.farland.frames_suff:
                    ljinux.farland.frames_av()
                ljinux.farland.frame_poi += 1
            else:
                ljinux.farland.frames_suff = True
                ljinux.farland.frames_av()
                ljinux.farland.frame_poi = 0

        def frames_av():
            average = sum([1 / (ljinux.farland.frames[i] / 10) for i in range(10)])
            print(average)

    class get_input:
        def left_key():
            return ljinux.io.buttonl.value

        def right_key():
            return ljinux.io.buttonr.value

        def enter_key():
            return ljinux.io.buttone.value

        def serial():
            return input()
