from os import system, mkdir, listdir, path, popen
from platform import uname
from getpass import getuser


def errexit():
    print("Compilation error, exiting")
    exit(1)


if uname().system == "Linux":
    slash = "/"
    copy = "cp"
else:
    slash = "\\"
    copy = "copy"
ami = getuser()
mpyn = f"../scripts/mpy-cross-{uname().machine}"
picop = ""
if system(f"test -d /media/{ami}/LJINUX") == 0:
    picop = f"/media/{ami}/LJINUX"
elif system(f"test -d /media/{ami}/CIRCUITPY") == 0:
    picop = f"/media/{ami}/CIRCUITPY"
elif system(f"test -d /media/CIRCUITPY") == 0:
    picop = f"/media/CIRCUITPY"
elif system("test -d /Volumes/LJINUX") == 0:
    picop = "/Volumes/LJINUX"
elif system("test -d /Volumes/CIRCUITPY") == 0:
    picop = "/Volumes/CIRCUITPY"
elif uname().system == "Windows":
    mpyn = f"..\scripts\mpy-cross-windows"
    drives = [chr(x) + ":" for x in range(65, 91) if path.exists(chr(x) + ":")]
    for _ in drives:
        vol = popen("vol " + _)
        if vol.readline()[:-1].split(" ")[-1].upper() == "CIRCUITPY":
            picop = f"%s" % _
        vol.close()
        if picop != "":
            break
if picop == "":
    print(
        "Error: Board not found.\nMake sure it is attached and mounted before you run make"
    )
    exit(1)

print(f"\nUsing mpycross: {mpyn}")
print(f"Using board path: {picop}\n")

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
