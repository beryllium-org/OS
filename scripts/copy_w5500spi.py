from os import system, mkdir, listdir
from platform import uname
from detect_board import detect_board
from sys import argv


def errexit():
    print("Compilation error, exiting")
    exit(1)


optimis = "-O4"
try:
    if argv[1] == "debug":
        print("Alert: Compiling with debug enabled.")
        optimis = ""
except IndexError:
    pass

if uname().system == "Linux":
    slash = "/"
    copy = "cp"
else:
    slash = "\\"
    copy = "copy"

[picop, board] = detect_board()

if picop == "":
    print(
        "Error: Board not found.\nMake sure it is attached and mounted before you run make"
    )
    exit(1)

mpyn = f"../scripts/mpy-cross-{uname().machine}"

print(f"\nUsing mpycross: {mpyn}")
print(f"Using board path: {picop}")
print(f"Building for board: {board}\n")

if system(f"test -d {picop}/lib".replace("/", slash)) != 0:
    print("Created lib directory.")
    mkdir(f"{picop}/lib".replace("/", slash))

if system(f"test -d {picop}/lib/drivers".replace("/", slash)) != 0:
    print("Created lib/drivers directory.")
    mkdir(f"{picop}/lib/drivers".replace("/", slash))

print("[1/5] Compiling Adafruit ntp")
a = system(
    f"{mpyn} ../other/Adafruit_CircuitPython_NTP/adafruit_ntp.py -s adafruit_ntp -v -O4 -o {picop}/lib/adafruit_ntp.mpy".replace(
        "/", slash
    )
)
if a != 0:
    errexit()

print("[2/5] Compiling Adafruit requests")
a = system(
    f"{mpyn} ../other/Adafruit_CircuitPython_Requests/adafruit_requests.py -s adafruit_requests -v -O4 -o {picop}/lib/adafruit_requests.mpy".replace(
        "/", slash
    )
)
if a != 0:
    errexit()

print("[3/5] Compiling Adafruit HTTPServer")
a = system(
    f"{mpyn} ../other/Adafruit_CircuitPython_HTTPServer/adafruit_httpserver.py -s adafruit_httpserver -v -O4 -o {picop}/lib/adafruit_httpserver.mpy".replace(
        "/", slash
    )
)
if a != 0:
    errexit()

print("[4/5] Compiling Adafruit CircuitPython Wiznet5k")
if system(f"test -d {picop}/lib/adafruit_wiznet5k".replace("/", slash)) != 0:
    print("Created adafruit_wiznet5k directory.")
    mkdir(f"{picop}/lib/adafruit_wiznet5k".replace("/", slash))
for filee in listdir(
    "../other/Adafruit_CircuitPython_Wiznet5k/adafruit_wiznet5k/".replace("/", slash)
):
    if filee != "adafruit_wiznet5k_wsgiserver.py":
        a = system(
            f"{mpyn} ../other/Adafruit_CircuitPython_Wiznet5k/adafruit_wiznet5k/{filee} -s {filee[:-3]} -v {optimis} -o {picop}/lib/adafruit_wiznet5k/{filee[:-3]}.mpy".replace(
                "/", slash
            )
        )
        if a != 0:
            errexit()

print("[5/5] Compiling w5500 spi drivers")
a = system(
    f"{mpyn} ../other/drivers/w5500spi.py -s driver_w5500spi -v {optimis} -o {picop}/lib/drivers/driver_w5500spi.mpy".replace(
        "/", slash
    )
)
if a != 0:
    errexit()

system("sync")
print()
