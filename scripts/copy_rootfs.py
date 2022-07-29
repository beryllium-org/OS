from os import system, mkdir, listdir, path, popen
from platform import uname
from getpass import getuser

ami = getuser()
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
        if vol.readline()[:-1].split(" ")[-1].upper() in ["CIRCUITPY", "LJINUX"]:
            picop = f"%s" % _
        vol.close()
        if picop != "":
            break
if picop == "":
    print(
        "Error: Board not found.\nMake sure it is attached and mounted before you run make"
    )
    exit(1)

if uname().system == "Linux":
    slash = "/"
    if system(f"test -d {picop}/LjinuxRoot") != 0:
        print("Created LjinuxRoot")
        mkdir(f"{picop}/LjinuxRoot")
    print(f"cp -rv ../LjinuxRoot/* {picop}/LjinuxRoot/")
    system(f"cp -rv ../LjinuxRoot/* {picop}/LjinuxRoot/")
    print(f"cp -v ../Manual.txt {picop}/LjinuxRoot/home/pi/")
    system(f"cp -v ../Manual.txt {picop}/LjinuxRoot/home/pi/")
else:
    slash = "\\"
    print(f"xcopy /y/s ..\\LjinuxRoot\\* {picop}\\LjinuxRoot\\")
    system(f"xcopy /y/s ..\\LjinuxRoot\\* {picop}\\LjinuxRoot\\")
    print(f"copy ..\\Manual.txt {picop}\\LjinuxRoot\\home\\pi\\")
    system(f"copy ..\\Manual.txt {picop}\\LjinuxRoot\\home\\pi\\")

ans = ""
while ans != "Y" and ans != "N":
    ans = input("Does the target microcontroller support wifi (Y/N): ").upper()
    if ans != "Y" and ans != "N":
        print("Invalid response, please answer Y, or N")

if ans == "Y":
    envline = {}
    paramlist = ['CIRCUITPY_WIFI_SSID','CIRCUITPY_WIFI_PASSWORD','CIRCUITPY_WEB_API_PASSWORD']

    defaults = True
    try:
        envfile = open(picop+slash+'.env')
    except:
        defaults = False

    if defaults:
        for line in envfile:
            try:
                envline[line.split('=')[0].strip()] = line.split('=')[1].strip()
            except:
                pass
        envfile.close()

    ans = ""
    while ans.upper() != "Y" and ans.upper() != "A":

        for param in paramlist:
            temp = input(param+": ["+envline.get(param,"")+"] ")
            if temp != "":
                envline[param] = temp

        print("\n"+slash+".env file about to be created:\n")
        for param in paramlist:
            print(param+"="+envline.get(param,""))

        print()
        ans = ""
        while ans.upper() != "Y" and ans.upper() != "N" and ans.upper() != "A":
            ans = input("Does this look correct (Y/N/(A)bort)?: ")
            if ans.upper() != "Y" and ans.upper() != "N" and ans.upper() != "A":
                print("Invalid response, please answer Y, N or A")

    if ans.upper() != "A":
        envfile = open(picop+slash+'.env','w')
        for param in paramlist:
            envfile.write(param+"="+envline.get(param,"")+"\n")
        envfile.close()
