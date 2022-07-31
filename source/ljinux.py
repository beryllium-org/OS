# -----------------
#      Ljinux
# Coded on a Raspberry Pi 400
# Ma'am I swear we are alright in the head
# -----------------

# Some important vars
Version = "0.4.0"
Circuitpython_supported = (7, 3)  # don't bother with last digit
dmesg = []
access_log = []

# Core board libs
try:
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
    print("FATAL: FAILED TO LOAD JCURSES")
    exit(0)


def dmtex(texx=None, end="\n", timing=True, force=False):
    # Persistent offset, Print "end=" preserver

    # current time since ljinux start rounded to 5 digits
    ct = "%.5f" % (uptimee + time.monotonic())

    # used to disable the time print
    strr = (
        "[{u}{upt}] {tx}".format(
            u="           ".replace(" ", "", len(ct)), upt=str(ct), tx=texx
        )
        if timing
        else texx
    )

    if (not term.dmtex_suppress) or force:
        print(strr, end=end)  # using the provided end

    global oend
    """
    if the oend of the last print is a newline we add a new entry
    otherwise we go to the last one and we add it along with the old oend
    """
    a = len(dmesg) - 1  # the last entry
    if "\n" == oend:
        dmesg.append(strr)
    elif (len(oend.replace("\n", "")) > 0) and (
        "\n" in oend
    ):  # there is hanging text in old oend
        dmesg[a] += oend.replace("\n", "")
        dmesg.append(strr)
    else:
        dmesg[a] += oend + strr
    oend = end  # oend for next

    del a, ct, strr


print("[    0.00000] Timings reset")
dmesg.append("[    0.00000] Timings reset")

# Now we can use this function to get a timing
dmtex("Basic Libraries loading")

# Basic absolutely needed libs
from sys import (
    implementation,
    platform,  # needed for neofetch btw
    modules,
    exit,
    stdout,
)

dmtex("System libraries loaded")

try:
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

    dmtex("Basic libraries loaded")
except ImportError:
    dmtex("FATAL: BASIC LIBRARIES LOAD FAILED")
    exit(0)

try:
    from neopixel_write import neopixel_write

    try:  # we can't fail this part though
        from neopixel_colors import neopixel_colors as nc
    except ImportError:
        dmtex("FATAL: FAILED TO LOAD NEOPIXEL_COLORS")
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
    for i in configg:
        if i.startswith("_"):
            del configg[i]
    del i

except (ValueError, OSError):
    configg = {}
    dmtex("Kernel config could not be found / parsed, applying defaults")

try:
    from lj_colours import lJ_Colours as colors

    print(colors.reset_s_format, end="")
    dmtex("Loaded lj_colours")
except ImportError:
    dmtex(f"{colors.error}FATAL:{colors.endc} FAILED TO LOAD LJ_COLOURS")
    dmtex(
        "If you intented to disable colors, just rename lj_colours_placebo -> lj_colours"
    )
    exit(0)

dmtex("Options applied:")

defaultoptions = {  # default configuration, in line with the manual (default value, type, allocates pin bool)
    "displaySCL": (-1, int, True),
    "displaySDA": (-1, int, True),
    "displayheight": (64, int, False),  # SSD1306 spec
    "displaywidth": (128, int, False),  # SSD1306 spec
    "led": (0, int, True),
    "ledtype": ("generic", str, False),
    "fixrtc": (True, bool, False),
    "SKIPTEMP": (False, bool, False),
    "SKIPCP": (False, bool, False),
    "DEBUG": (False, bool, False),
    "DISPLAYONLYMODE": (False, bool, False),
    "w5500_MOSI": (-1, int, True),
    "w5500_MISO": (-1, int, True),
    "w5500_SCSn": (-1, int, True),
    "w5500_SCLK": (-1, int, True),
    "sd_SCLK": (-1, int, True),
    "sd_SCSn": (-1, int, True),
    "sd_MISO": (-1, int, True),
    "sd_MOSI": (-1, int, True),
    "mem": (264, int, False),
}

# dynamic pintab
try:
    exec(f"from pintab_{board.board_id} import pintab")
except:
    dmtex(f"{colors.error}ERROR:{colors.endc} Board config cannot be loaded")
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
            'Missing / Invalid value for "' + optt + '" applied: ' + str(configg[optt]),
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
for i in pin_alloc:
    dmtex(str(i), timing=False, end=" ")
dmtex("", timing=False)

if configg["led"] == -1:
    boardLED = board.LED
else:
    boardLED = pintab[configg["led"]]
boardLEDinvert = False

del defaultoptions

# basic checks
if not configg["SKIPCP"]:  # beta testing
    if implementation.version[:2] == Circuitpython_supported or (
        implementation.version[0] == Circuitpython_supported[0]
        and implementation.version[1] < Circuitpython_supported[1]
    ):
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
        dmtex("Now that a 'cool' board! B)")
    del temp
else:
    print("Temperature check skipped, rest in pieces cpu.")

dmtex("Running board detection")
boardactions = {
    "raspberry_pi_pico": lambda: dmtex("Running on a Raspberry Pi Pico."),
    "waveshare_rp2040_zero": lambda: dmtex("Running on a Waveshare RP2040-Zero."),
    "adafruit_kb2040": lambda: dmtex("Running on an Adafruit KB2040."),
    "waveshare_esp32s2_pico": lambda: dmtex("Running on a Waveshare ESP32-S2-Pico."),
    "adafruit_feather_esp32s2": lambda: exec(
        'dmtex("Running on an Adafruit Feather ESP32-S2."); boardLEDinvert = True'
    ),
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
    dmtex(colors.error + "Notice: " + colors.endc + "Audio libraries loading failed")

# sd card
try:
    import adafruit_sdcard

    dmtex("Sdcard libraries loaded")
except ImportError:
    dmtex(colors.error + "Notice: " + colors.endc + "SDcard libraries loading failed")

# display
try:
    import adafruit_ssd1306

    dmtex("Display libraries loaded")
except ImportError:
    dmtex(colors.error + "Notice: " + colors.endc + "Display libraries loading failed")

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
        colors.error + "Notice: " + colors.endc + "Networking libraries loading failed"
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
        dmtex(colors.error + "Notice: " + colors.endc + "RTC libraries loading failed")

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


class ljinux:
    class history:
        historyy = []
        nav = [0, 0, ""]

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
                ljinux.io.ledset(1)  # idle
                ljinux.based.error(4, filen)

        def appen(itemm):  # add to history, but don't save to file
            if (
                len(ljinux.history.historyy) > 0 and itemm != ljinux.history.gett(1)
            ) or len(ljinux.history.historyy) == 0:
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

        def clear(filen):
            try:
                # deletes all history, from ram and storage
                a = open(filen, "r")
                a.close()
                del a
                with open(filen, "w") as historyfile:
                    historyfile.flush()
                ljinux.history.historyy.clear()
            except OSError:
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

        getled = 0

        led = digitalio.DigitalInOut(boardLED)
        led.direction = digitalio.Direction.OUTPUT
        if configg["ledtype"] == "generic":
            led.value = True
        elif configg["ledtype"] == "generic_invert":
            led.value = False
        elif configg["ledtype"] == "neopixel":
            neopixel_write(led, nc.idle)

        network = None
        network_online = False
        network_name = "Offline"

        def ledset(state):
            """
            Set the led to a state.
            state can be int with one of the predifined states,
            or a tuple like (10, 40, 255) for a custom color
            """
            if isinstance(state, int):
                ## use preconfigured led states
                if configg["ledtype"] in ["generic", "generic_invert"]:
                    if state in {0, 3}:
                        ljinux.io.led.value = (
                            False if configg["ledtype"] == "generic" else True
                        )
                    else:
                        ljinux.io.led.value = (
                            True if configg["ledtype"] == "generic" else False
                        )
                elif configg["ledtype"] == "neopixel":
                    neopixel_write(ljinux.io.led, ljinux.io.ledcases[state])
            elif isinstance(state, tuple):
                # a custom color
                if configg["ledtype"] in ["generic", "generic_invert"]:
                    if not (state[0] == 0 and state[1] == 0 and state[2] == 0):
                        # apply 1 if any of tuple >0
                        ljinux.io.led.value = (
                            True if configg["ledtype"] == "generic" else False
                        )
                    else:
                        ljinux.io.led.value = (
                            False if configg["ledtype"] == "generic" else True
                        )
                elif configg["ledtype"] == "neopixel":
                    neopixel_write(ljinux.io.led, bytearray(state))
            else:
                raise TypeError
            ljinux.io.getled = state

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

        def init_net():
            global configg
            if (
                configg["w5500_SCSn"] != -1
                and configg["w5500_SCLK"] != -1
                and configg["w5500_MISO"] != -1
                and configg["w5500_MOSI"] != -1
            ):
                cs = digitalio.DigitalInOut(pintab[configg["w5500_SCSn"]])
                spi = busio.SPI(
                    pintab[configg["w5500_SCLK"]],
                    MOSI=pintab[configg["w5500_MOSI"]],
                    MISO=pintab[configg["w5500_MISO"]],
                )
                ca = True
                dmtex("Network bus ready")
            else:
                ca = False
                dmtex("No pins for networking, skipping setup")
            if ca:
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
                for i in [
                    "adafruit_wiznet5k.adafruit_wiznet5k_dhcp",
                    "adafruit_wiznet5k.adafruit_wiznet5k_socket",
                    "adafruit_wiznet5k.adafruit_wiznet5k_dns",
                    "adafruit_wiznet5k.adafruit_wiznet5k",
                    "adafruit_wiznet5k",
                    "adafruit_wsgi.wsgi_app",
                    "adafruit_requests",
                    "adafruit_wiznet5k.adafruit_wiznet5k_wsgiserver",
                    "adafruit_wsgi",
                    "adafruit_wsgi.request",
                ]:
                    try:
                        exec(f"global {i};del {i};del modules[{i}]")
                    except:
                        pass
                dmtex("Unloaded networking libraries")
            del ca

        def start_sdcard():
            global sdcard_fs
            if (
                configg["sd_SCLK"] != -1
                and configg["sd_SCSn"] != -1
                and configg["sd_MISO"] != -1
                and configg["sd_MOSI"] != -1
            ):
                spi = busio.SPI(board.GP2, MOSI=board.GP3, MISO=board.GP4)
                cs = digitalio.DigitalInOut(board.GP5)
            else:
                sdcard_fs = False
                dmtex("No pins for sdcard, skipping setup")
                return
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

        sys_getters = {
            "sdcard": lambda: str(sdcard_fs),
            "uptime": lambda: str("%.5f" % (uptimee + time.monotonic())),
            "temperature": lambda: str("%.2f" % cpu.temperature),
            "display-attached": lambda: str(display_availability),
            "memory": lambda: str(gc.mem_free()),
            "implementation_version": lambda: ljinux.based.system_vars[
                "IMPLEMENTATION"
            ],
            "implementation": lambda: implementation.name,
            "frequency": lambda: str(cpu.frequency),
            "voltage": lambda: str(cpu.voltage),
        }

    class networking:
        wsgiServer = None

        def get_content_type(filee):
            ext = filee.split(".")[-1]
            if ext in ("html", "htm"):
                return "text/html"
            elif ext == "js":
                return "application/javascript"
            elif ext == "css":
                return "text/css"
            elif ext in ("jpg", "jpeg"):
                return "image/jpeg"
            elif ext == "png":
                return "image/png"
            elif ext == "json":
                return "application/json"
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
                    try:
                        rtcc.write_datetime(nettime)
                    except NameError:
                        dmtex("Cannot set time, since no rtc is attached")
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
        olddir = None
        pled = False  # persistent led state for nested exec
        alias_dict = {}
        raw_command_input = ""

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
            }
            print(f"{colors.magenta_t}Based{colors.endc}: {errs[wh]}")
            ljinux.io.ledset(1)
            del errs

        def autorun():
            ljinux.io.ledset(3)  # act
            global Exit
            global Exit_code
            global Version

            ljinux.based.system_vars["VERSION"] = Version

            print(
                "\nWelcome to lJinux wannabe Kernel {}!\n\n".format(
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
                print(
                    f"{colors.magenta_t}Based{colors.endc}: Init complete. Restarting"
                )
            elif ljinux.based.system_vars["Init-type"] == "delayed-reboot-repeat":
                try:
                    time.sleep(float(ljinux.based.user_vars["repeat-delay"]))
                except IndexError:
                    print(
                        f"{colors.magenta_t}Based{colors.endc}: No delay specified! Waiting 60s."
                    )
                    time.sleep(60)
                    Exit = True
                    Exit_code = 245
                    print(
                        f"{colors.magenta_t}Based{colors.endc}: Init complete and delay finished. Restarting"
                    )
            elif ljinux.based.system_vars["Init-type"] == "oneshot-quit":
                Exit = True
                Exit_code = 244
                print(f"{colors.magenta_t}Based{colors.endc}: Init complete. Halting")
            elif ljinux.based.system_vars["Init-type"] == "repeat":
                try:
                    while not Exit:
                        for commandd in lines:
                            ljinux.based.shell(commandd)

                except KeyboardInterrupt:
                    print(f"{colors.magenta_t}Based{colors.endc}: Caught Ctrl + C")
            elif ljinux.based.system_vars["Init-type"] == "delayed-repeat":
                try:
                    time.sleep(float(ljinux.based.user_vars["repeat-delay"]))
                except IndexError:
                    print(
                        f"{colors.magenta_t}Based{colors.endc}: No delay specified! Waiting 60s."
                    )
                    time.sleep(60)
                try:
                    while not Exit:
                        for commandd in lines:
                            ljinux.based.shell(commandd)

                except KeyboardInterrupt:
                    print(f"{colors.magenta_t}Based{colors.endc}: Caught Ctrl + C")
            else:
                print(
                    f"{colors.magenta_t}Based{colors.endc}: Init-type specified incorrectly, assuming oneshot"
                )
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
                print(
                    f"{colors.magenta_t}Based{colors.endc}: '{errr[0]}': command not found"
                )
                ljinux.based.user_vars["return"] = "1"

            def execc(argj):
                global Exit
                global Exit_code

                if argj[0] == "exec":
                    argj = argj[1:]

                try:
                    with open(argj[0], "r") as filee:
                        ljinux.based.olddir = getcwd()
                        mine = False
                        if not ljinux.based.pled:
                            ljinux.based.pled = True
                            ljinux.io.ledset(3)
                            mine = True
                        else:
                            old = ljinux.io.getled
                            ljinux.io.ledset(3)
                            time.sleep(0.03)
                            ljinux.io.ledset(old)
                            del old
                        for j in filee:
                            j = j.strip()

                            ljinux.based.shell(
                                'argj = "{}"'.format(" ".join([str(i) for i in argj])),
                                led=False,
                            )

                            ljinux.based.shell(j, led=False)

                            del j
                        if ljinux.based.olddir != getcwd():
                            chdir(ljinux.based.olddir)
                        if mine:
                            ljinux.io.ledset(1)
                        del mine
                except OSError:
                    ljinux.based.error(4, argj[0])

            def helpp(dictt):
                print(
                    f"LNL {colors.magenta_t}based\nThese shell commands are defined internally or are in PATH.\nType 'help' to see this list.\n"
                )  # shameless, but without rgb spam

                l = ljinux.based.get_bins() + list(dictt.keys())

                lenn = 0
                for i in l:
                    if len(i) > lenn:
                        lenn = len(i)
                lenn += 2

                for index, tool in enumerate(l):
                    print(
                        colors.green_t + tool + colors.endc,
                        end=(" " * lenn).replace(" ", "", len(tool)),
                    )
                    if index % 4 == 3:
                        stdout.write("\n")  # stdout faster than print cuz no logic
                stdout.write("\n")

                del l
                del lenn

            def var(inpt):  # variables setter / editor
                valid = True
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
                                if ljinux.based.fn.adv_input(inpt[0], str) == inpt[0]:
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
                                print(
                                    colors.error
                                    + "Cannot edit system variables, security is enabled."
                                    + colors.endc
                                )
                        elif (
                            inpt[0] == ljinux.based.fn.adv_input(inpt[0], str)
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

            def dell(inpt):  # del variables, and dell computers
                try:
                    a = inpt[1]
                    if a == ljinux.based.fn.adv_input(a, str) and a not in gpio_alloc:
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
                                print(
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

            def suuu(inpt):  # su command but worse
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
                        print("Authentication successful. Security disabled.")
                    else:
                        ljinux.io.ledset(3)
                        time.sleep(2)
                        print(
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
                        print("Authentication successful. Security disabled.")
                    else:
                        print(
                            colors.error + "Authentication unsuccessful." + colors.endc
                        )
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
                        print("{colors.magenta_t}Based{colors.endc}: Invalid option")
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
                                            print(
                                                f"{colors.magenta_t}Based{colors.endc}: Arg not in argj"
                                            )
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
                                    print(
                                        f"{colors.magenta_t}Based{colors.endc}: Invalid action type: "
                                        + condition[i]
                                    )
                                    break
                            if val == 1:
                                ljinux.based.shell(
                                    " ".join(inpt[next_part:]), led=False
                                )
                            del next_part
                            del val
                        except KeyError:
                            print(
                                f"{colors.magenta_t}Based{colors.endc}: Invalid condition type"
                            )
                    else:
                        print(
                            f"{colors.magenta_t}Based{colors.endc}: Incomplete condition"
                        )
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

            def pexecc(inpt):  # filtered & true source
                global Version
                pcomm = ljinux.based.raw_command_input.lstrip(
                    ljinux.based.raw_command_input.split()[0]
                ).replace(" ", "", 1)
                nl = False
                try:
                    if "-n" in inpt[1]:
                        nl = True
                        pcomm = pcomm.lstrip(
                            ljinux.based.raw_command_input.split()[1]
                        ).replace(" ", "", 1)
                except IndexError:
                    ljinux.based.error(9)
                    ljinux.based.user_vars["return"] = "1"
                    return
                if not nl:
                    print(
                        "Adafruit CircuitPython {} on ljinux {}; {}\n>>> {}".format(
                            ljinux.based.system_vars["IMPLEMENTATION"],
                            Version,
                            ljinux.based.system_vars["BOARD"],
                            pcomm,
                        )
                    )
                try:
                    exec(pcomm)  # Vulnerability.exe
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
                fpargs = list()
                offs = 1

                try:
                    while inpt[offs].startswith("-"):
                        fpargs += list(inpt[offs][1:])
                        offs += 1
                except IndexError:
                    ljinux.based.error(9)
                    ljinux.based.user_vars["return"] = "1"
                    return

                if not ("n" in fpargs):
                    print(
                        "Adafruit CircuitPython {} on ljinux {}; {}\nRunning file: {}".format(
                            ljinux.based.system_vars["IMPLEMENTATION"],
                            Version,
                            ljinux.based.system_vars["BOARD"],
                            inpt[offs],
                        )
                    )
                try:
                    a = open(ljinux.based.fn.betterpath(inpt[offs])).read()
                    if not ("t" in fpargs or "l" in fpargs):
                        exec(a)
                    elif "i" in fpargs:
                        exec(a, dict(), dict())
                    elif "l" in fpargs:
                        exec(a, locals())
                    del a
                except Exception as err:
                    print(
                        "Traceback (most recent call last):\n\t"
                        + str(type(err))[8:-2]
                        + ": "
                        + str(err)
                    )
                    del err
                del offs, fpargs

        class fn:
            """
            Common functions used by the commands.
            CODE:
                ljinux.based.fn.[function_name](parameters)
            """

            def isdir(dirr, rdir=None):
                """
                Checks if given item is file (returns 0) or directory (returns 1).
                Returns 2 if it doesn't exist.
                """
                dirr = ljinux.based.fn.betterpath(dirr)

                cddd = getcwd()
                try:
                    chdir(dirr)
                    chdir(cddd)
                    del cddd
                    return 1
                except OSError:
                    del cddd  # yes we need both
                    try:
                        return (
                            0
                            if dirr[dirr.rfind("/") + 1 :]
                            in listdir(
                                dirr[: dirr.rfind("/")] if rdir is None else rdir
                            )
                            else 2
                        )
                    except OSError:
                        return 2  # we have had enough

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

        def shell(
            inp=None, led=True, args=None, nalias=False
        ):  # the shell function, warning do not touch, it has feelings - no I think I will 20/3/22
            global Exit
            if inp is not None and args is not None:
                for i in args:
                    inp += f" {i}"
            del args
            function_dict = {
                # holds all built-in commands. The plan is to move as many as possible externally
                # yea, hello 9/6/22 here, we keepin bash-like stuff in, but we have to take the normal
                # ones out, we almost there
                "error": ljinux.based.command.not_found,
                "exec": ljinux.based.command.execc,
                "help": ljinux.based.command.helpp,
                "var": ljinux.based.command.var,
                "unset": ljinux.based.command.dell,
                "su": ljinux.based.command.suuu,
                "history": ljinux.based.command.historgf,
                "if": ljinux.based.command.iff,
                "ping": ljinux.based.command.ping,
                "webserver": ljinux.based.command.webs,
                "pexec": ljinux.based.command.pexecc,
                "COMMENT": ljinux.based.command.do_nothin,
                "#": ljinux.based.command.do_nothin,
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
                    "ctrlL": 13,
                    "tab": 3,
                    "up": 4,
                    "down": 7,
                    "pgup": 11,
                    "pgdw": 12,
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
                        + "> "
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
                                    slicedd = tofind.split()
                                    lent = len(slicedd)
                                    if lent > 1:  # suggesting files
                                        files = listdir()
                                        for i in files:
                                            if i.startswith(
                                                slicedd[lent - 1]
                                            ):  # only on the arg we are in
                                                candidates.append(i)
                                        del files
                                    else:  # suggesting bins
                                        bins = ljinux.based.get_bins()
                                        for i in [function_dict, bins]:
                                            for j in i:
                                                if j.startswith(tofind):
                                                    candidates.append(j)
                                        del bins
                                    if len(candidates) > 1:
                                        stdout.write("\n")
                                        minn = 100
                                        for i in candidates:
                                            if not i.startswith("_"):  # discard those
                                                minn = min(minn, len(i))
                                                print("\t" + i)
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
                                                        else:
                                                            letters_match += 1
                                                    except IndexError:
                                                        isMatch = False
                                        del minn, isMatch
                                        if letters_match > 0:
                                            term.clear_line()
                                            if lent > 1:
                                                term.buf[1] = "".join(
                                                    slicedd[:-1]
                                                    + list(
                                                        " "
                                                        + candidates[0][:letters_match]
                                                    )
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
                                            term.buf[1] = "".join(
                                                slicedd[:-1] + list(" " + candidates[0])
                                            )
                                        else:
                                            term.buf[1] = candidates[0]
                                        term.focus = 0
                                    else:
                                        term.clear_line()
                                    del candidates, lent, tofind, slicedd
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
                                elif term.buf[0] in [11, 12]:  # pgup / pgdw
                                    term.clear_line()
                                elif term.buf[0] is 13:  # Ctrl + L (clear screen)
                                    term.buf[1] = ""
                                    term.focus = 0
                                    term.clear()

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
                        if (not "|" in command_input) and (not "&&" in command_input):
                            ljinux.based.raw_command_input = command_input
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
                                elif (not nalias) and (
                                    command_split[0] in ljinux.based.alias_dict
                                ):
                                    ljinux.based.shell(
                                        ljinux.based.alias_dict[command_split[0]],
                                        led=False,
                                        args=command_split[1:],
                                        nalias=True,
                                    )
                                elif (command_split[0] in function_dict) and (
                                    command_split[0]
                                    not in [
                                        "error",
                                        "help",
                                    ]
                                ):  # those are special bois, they will not be special when I make the api great
                                    gc.collect()
                                    gc.collect()
                                    res = function_dict[command_split[0]](command_split)
                                elif command_split[0] == "help":
                                    res = function_dict["help"](function_dict)
                                elif command_split[1] == "=":
                                    res = function_dict["var"](command_split)
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
                                    gc.collect()
                                    gc.collect()
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
        public = []

        # ---

        def setup():
            ljinux.based.command.fpexecc([None, "-n", "/bin/display_f/setup.py"])

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
        def draw_circle(xpos0, ypos0, rad, col, f):
            ljinux.farland.public = [xpos0, ypos0, rad, col]
            if not f:
                ljinux.based.command.fpexecc(
                    [None, "-n", "/bin/display_f/draw_circle.py"]
                )
            else:
                ljinux.based.command.fpexecc(
                    [None, "-n", "/bin/display_f/f_draw_circle.py"]
                )

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
