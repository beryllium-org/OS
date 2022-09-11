from os import system, mkdir, listdir, path, popen
from platform import uname
from getpass import getuser
from detect_board import detect_board


def errexit():
    print("Compilation error, exiting")
    exit(1)


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

print("\n[1/4] Compiling Adafruit ntp\n-> adafruit_ntp")
a = system(
    f"{mpyn} ../other/Adafruit_CircuitPython_NTP/adafruit_ntp.py -s adafruit_ntp -v -O4 -o {picop}/lib/adafruit_ntp.mpy".replace(
        "/", slash
    )
)
if a != 0:
    errexit()
del a

print("\n[2/4] Compiling adafruit requests\n-> adafruit_requests")
a = system(
    f"{mpyn} ../other/Adafruit_CircuitPython_Requests/adafruit_requests.py -s adafruit_requests -v -O4 -o {picop}/lib/adafruit_requests.mpy".replace(
        "/", slash
    )
)
if a != 0:
    errexit()
del a

print("\n[3/4] Compiling adafruit HTTPServer\n-> adafruit_httpserver")
a = system(
    f"{mpyn} ../other/Adafruit_CircuitPython_HTTPServer/adafruit_httpserver.py -s adafruit_httpserver -v -O4 -o {picop}/lib/adafruit_httpserver.mpy".replace(
        "/", slash
    )
)
if a != 0:
    errexit()
del a

print("\n[4/4] Compiling w5500 spi drivers\n-> driver_w5500spi")
a = system(
    f"{mpyn} ../other/drivers/w5500spi.py -s driver_w5500spi -v -O4 -o {picop}/lib/drivers/driver_w5500spi.mpy".replace(
        "/", slash
    )
)
if a != 0:
    errexit()
del a

system("sync")
print()
del ami, picop, mpyn
