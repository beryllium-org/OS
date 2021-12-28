# -----------------
# Ljinux by bill88t
# Coded on a Raspberry Pi 400
# Ma'am I swear this project is real
# -----------------

# immutable vars
Version = "0.0.3"
# debug prints
ljdebug = False

# default password, aka the password if no /ljinux/etc/passwd is found TODO ADD THIS FUNCTIONALITY
dfpasswd = "Ljinux"
#exit code holder, has to be global
Exit = False
Exit_code = 0

#hardware autodetect vars, starts assuming everything is missing
sdcard_fs = False
display_availability = False
print("[    0.00000] Sys vars loaded")

import time
print("[    0.00000] Timing libraries done")
uptimee = -time.monotonic()
print("[    0.00000] Got time zero")

def dmtex(texx=None):
    try:
        ct = uptimee+time.monotonic() # current time since ljinux start
        if (ct < 10): # this all just moves it to the left to accomodate for thicc uptimes
            print("[    ",end="")
        elif (ct < 100):
            print("[   ",end="")
        elif (ct < 1000):
            print("[  ",end="")
        else: # THICCC
            print("[ ",end="")
        print("%.5f" % ct + "] " + texx)
    except TypeError:
        pass

print("[    0.00000] Timings reset")

# now we can use this function to get a timing
dmtex("Basic Libraries loading")

#basic libs
import sys
import supervisor
import board
import pwmio
import digitalio
import analogio
import busio
import microcontroller
import storage
import gc
import os
import sys
import math
dmtex("Basic libraries loaded")

# audio
import audiomp3
import audiopwmio
import audiocore
dmtex("Audio libraries loaded")

# sd card
import adafruit_sdcard
dmtex("Sdcard libraries loaded")

# display
import adafruit_ssd1306
dmtex("Display libraries loaded")

# password input
from getpass import getpass
dmtex("Getpass library loaded")

# for rtc
# based off of https://github.com/afaonline/DS1302_CircuitPython
import rtc
import ds1302
dmtex("RTC library loaded")

dmtex("Imports complete")
# trust me, all of em are necessary

# rtc stuff @ init cuz otherwise system fails to access it
#the pins to connect it to
rtcclk = digitalio.DigitalInOut(board.GP6)
rtcdata = digitalio.DigitalInOut(board.GP7)
rtcce = digitalio.DigitalInOut(board.GP8)

# to make it suitable for system
class RTC(object):
    @property
    def datetime(self):
        return rtcc.read_datetime()

try:
    rtcc = ds1302.DS1302(rtcclk,rtcdata,rtcce) # muh rtc object
    r = RTC() # now in a good format
    rtc.set_time_source(r)

except OSError: # not sure how to catch if it's not available, TODO
    pass

dmtex("RTC clock init done")

def isInteger(N):
    # Convert float value
    # of N to integer
    X = int(N)
    temp2 = N - X
    # If N is not equivalent
    # to any integer
    if (temp2 > 0):
        return False
    return True

class ljinux():
    class history:
        historyy = []
        historyitems = 0

        def load(filen):
            ljinux.history.historyy = []
            ljinux.history.historyitems = 0
            try:
                with open(filen, 'r') as historyfile:
                    ljinux.io.led.value = False
                    lines = historyfile.readlines()
                    ljinux.io.led.value = True
                    for line in lines:
                        ljinux.io.led.value = False
                        ljinux.history.historyy.append(line.strip())
                        ljinux.history.historyitems += 1
                        ljinux.io.led.value = True
            except OSError:
                    ljinux.io.led.value = True
                    print("based: "+ filen +": No such file or directory\n")

        def appen(itemm): # add to history, but don't save to file
            ljinux.history.historyy.append(itemm)
            ljinux.history.historyitems += 1

        def save(filen):
            ljinux.io.led.value = False
            try:
                a = open(filen, 'r')
                a.close()
                with open(filen, 'w') as historyfile:
                    ljinux.io.led.value = True
                    for i in range(ljinux.history.historyitems):
                        ljinux.io.led.value = False
                        historyfile.write(ljinux.history.historyy[i] + "\n")
                        ljinux.io.led.value = True
                    ljinux.io.led.value = False
                    historyfile.flush()
            except OSError:
                    print("based: "+ filen +": No such file or directory\n")
            ljinux.io.led.value = True

        def clear(filen): # deletes all history, from ram and storage
            try:
                ljinux.io.led.value = False
                a = open(filen, 'r')
                a.close()
                with open(filen, 'w') as historyfile:
                    historyfile.flush()
                ljinux.history.historyitems = 0
                ljinux.history.historyy = []
            except OSError:
                    print("based: "+ filen +": No such file or directory\n")
            ljinux.io.led.value = True

        def gett(whichh): # get a specific history item, from loaded history
            return str(ljinux.history.historyy[whichh])

        def getall(): # get the whole history, numbered, line by line
            for i in range(ljinux.history.historyitems):
                print(str(i+1) + ": " + str(ljinux.history.historyy[i]))

    class SerialReader: # based off of https://github.com/todbot/circuitpython-tricks#rename-circuitpy-drive-to-something-new, thanks a lot dude this shiet is awesome!
        global ljdebug
        def __init__(self):
            self.s = ''
            self.scount = 0 # how many are in the array, just for speed
            self.capture_step = 0 # var to hold status of capturing multi-byte chars
            self.pos = 0 # where is the cursor, and to be more precise, how many steps left it is.
            self.temp_s = '' # holds current command, while you are browsing the history
            self.historypos = 0
        def read(self,end_char='\n', echo= not ljdebug): # you can call it with a custom end_char or no echo
            global ljdebug
            badchar = False # don't pass char to str
            n = supervisor.runtime.serial_bytes_available
            if n > 0:
                i = sys.stdin.read(n) # it's now a char, read from stdin
                for s in i:
                    hexed = str(hex(ord(s))) # I tried to fix this 3 times. Watch this number go up.
                    if ljdebug:
                        print(hexed) #use this to get it's hex form
                    if (hexed == "0x4"): # catch Ctrl + D
                        print("^D")
                        global Exit
                        Exit = True
                        return None
                    elif (hexed == "0x7f"): # catch Backspace
                        if (self.scount - self.pos > 0):
                            if (self.pos == 0):
                                self.s = self.s[:-1]
                                self.scount -= 1
                                sys.stdout.write('\010')
                                sys.stdout.write(' ')
                                sys.stdout.write('\010')
                            else:
                                # oh come on whyyyyyyy
                                sys.stdout.write('\010')
                                insertion_pos = self.scount - self.pos - 1
                                self.s = self.s[:insertion_pos] + self.s[insertion_pos+1:] # backend insertion
                                self.scount -= 1
                                steps_in = 0
                                for i in self.s[insertion_pos:]: # frontend insertion
                                    sys.stdout.write(i)
                                    steps_in +=1
                                sys.stdout.write(' ')
                                sys.stdout.write('\x1b[{}D'.format(steps_in+1)) # go back to pos
                        badchar = True
                    elif ((hexed == "0x1b") or (self.capture_step > 0)): # catch arrow keys
                        if (self.capture_step < 2): # we need to get the char that specifies it's an arrow key, the useless char and then the one we need
                            self.capture_step += 1
                        else:
                            # up: \x1b[{n}A
                            # down: \x1b[{n}B
                            # right: \x1b[{n}C
                            # left: \x1b[{n}D
                            # where n = number of steps
                            if (hexed == "0x41"): # Up arrow key
                                try:
                                    pass
                                except IndexError:
                                    pass
                            elif (hexed == "0x44"): # Left arrow key
                                if (self.pos < self.scount):
                                    self.pos += 1
                                    sys.stdout.write('\x1b[1D')
                            elif (hexed == "0x43"): # Right arrow key
                                if (self.pos > 0):
                                    self.pos -= 1
                                    sys.stdout.write('\x1b[1C')
                            elif (hexed == "0x42"): # Down arrow key
                                pass
                            self.capture_step = 0
                        badchar = True
                    elif ((hexed == "0xf") and ljdebug): # Catch Ctrl + O on debug
                        print("\n------------")
                        print("self.pos = " + str(self.pos))
                        print("self.s = " + str(self.s))
                        print("self.scount = " + str(self.scount))
                        print("self.capture_step = " + str(self.capture_step))
                        print("self.temp_s = " + str(self.temp_s))
                    else:
                        if echo: sys.stdout.write(s)  # echo back to hooman
                        if not (badchar):
                            if ((self.pos == 0) or (s == end_char)):
                                self.s = self.s + s      # keep building the string up
                                self.scount += 1
                            else:
                                insertion_pos = self.scount - self.pos
                                self.s = self.s[:insertion_pos] + s + self.s[insertion_pos:] # backend insertion
                                self.scount += 1
                                steps_in = 0
                                for i in self.s[insertion_pos+1:]: # frontend insertion
                                    sys.stdout.write(i)
                                    steps_in +=1
                                sys.stdout.write('\x1b[{}D'.format(steps_in)) # go back to pos
                        if s.endswith(end_char): # got our end_char!
                            rstr = self.s        # save for return
                            self.s = ''          # reset everything
                            self.scount = 0
                            self.pos = 0
                            self.capture_step = 0
                            self.historypos = 0
                            return rstr
            return None                  # no end_char yet

    class io(object):
        # activity led
        led = digitalio.DigitalInOut(board.LED)
        led.direction = digitalio.Direction.OUTPUT
        led.value = True
        # sd card
        # L R and Enter keys for basic io
        buttonl = digitalio.DigitalInOut(board.GP12)
        buttonl.switch_to_input(pull=digitalio.Pull.DOWN)
        buttonr = digitalio.DigitalInOut(board.GP13)
        buttonr.switch_to_input(pull=digitalio.Pull.DOWN)
        buttone = digitalio.DigitalInOut(board.GP11)
        buttone.switch_to_input(pull=digitalio.Pull.DOWN)
        # pc puzzer
        #buzzer = pwmio.PWMOut(board.GP15, variable_frequency=True, frequency = 200, duty_cycle = 0)

        def start_sdcard():
            global sdcard_fs
            spi = busio.SPI(board.GP2, MOSI=board.GP3, MISO=board.GP4)
            cs = digitalio.DigitalInOut(board.GP5)
            sdcard = adafruit_sdcard.SDCard(spi, cs)
            vfs = storage.VfsFat(sdcard)
            storage.mount(vfs, "/ljinux")
            sdcard_fs = True

        def left_key():
            if (ljinux.io.buttonl.value == True):
                return True
            else:
                return False

        def right_key():
            if (ljinux.io.buttonr.value == True):
                return True
            else:
                return False

        def enter_key():
            if (ljinux.io.buttone.value == True):
                return True
            else:
                return False

        def serial():
            return input()

    class based(object):
        user_vars = {'history-file': "/ljinux/home/pi/.history"}
        system_vars = {'user': "root", 'security': "off", 'Init-type': "oneshot"}
        inputt = None
        def autorun():
            ljinux.io.led.value = False
            global Exit
            global Exit_code
            global Version
            print("\nWelcome to ljinux wanna-be kernel " + Version + "\n\n", end='')
            try:
                print("[ Starting ] Mount /ljinux")
                ljinux.io.start_sdcard()
                print("[ OK ] Mount /ljinux")
            except OSError:
                print("[ Failed ] Mount /ljinux\nError: sd card not available, assuming built in fs")
            ljinux.io.led.value = True
            print("[ Starting ] Running Init Script\nAttempting to open /ljinux/boot/Init.lja..")
            lines = None
            try:
                ljinux.io.led.value = False
                f = open("/ljinux/boot/Init.lja", 'r')
                lines = f.readlines()
                f.close()
                count = 0
                ljinux.io.led.value = True
                for line in lines:
                    ljinux.io.led.value = False
                    lines[count] = line.strip()
                    count += 1
                    ljinux.io.led.value = True
                for commandd in lines:
                    ljinux.based.shell(commandd)
                print("[ OK ] Running Init Script")
            except OSError:
                print("[ Failed ] Running Init Script\n")
            ljinux.history.load(ljinux.based.user_vars["history-file"])
            print("[ OK ] History Reload\n")
            if (ljinux.based.system_vars["Init-type"] == "oneshot"):
                print("based: Init complete. Press any key to drop to shell..\n")
            elif (ljinux.based.system_vars["Init-type"] == "reboot-repeat"):
                global Exit
                global Exit_code
                Exit = True
                Exit_code = 245
                print("based: Init complete. Restarting")
            elif (ljinux.based.system_vars["Init-type"] == "delayed-reboot-repeat"):
                try:
                    time.sleep(float(ljinux.based.user_vars["repeat-delay"]))
                except IndexError:
                    print("based: No delay specified! Waiting 60s.")
                    time.sleep(60)
                    global Exit
                    global Exit_code
                    Exit = True
                    Exit_code = 245
                    print("based: Init complete and delay finished. Restarting")
            elif (ljinux.based.system_vars["Init-type"] == "oneshot-quit"):
                global Exit
                global Exit_code
                Exit = True
                Exit_code = 244
                print("based: Init complete. Halting")
            elif (ljinux.based.system_vars["Init-type"] == "repeat"):
                try:
                    while not Exit:
                        for commandd in lines:
                            ljinux.based.shell(commandd)
                        if ((ljinux.io.buttonl.value == True) and (ljinux.io.buttonr.value == True)):
                            time.sleep(.5)
                            if ((ljinux.io.buttonl.value == True) and (ljinux.io.buttonr.value == True)):
                                global Exit
                                global Exit_code
                                Exit = True
                                Exit_code = 244
                except KeyboardInterrupt:
                    print("based: Caught Ctrl + C, press any key to drop to shell..")
            elif (ljinux.based.system_vars["Init-type"] == "delayed-repeat"):
                try:
                    time.sleep(float(ljinux.based.user_vars["repeat-delay"]))
                except IndexError:
                    print("based: No delay specified! Waiting 60s.")
                    time.sleep(60)
                try:
                    while not Exit:
                        for commandd in lines:
                            ljinux.based.shell(commandd)
                        if ((ljinux.io.buttonl.value == True) and (ljinux.io.buttonr.value == True)):
                            time.sleep(.5)
                            if ((ljinux.io.buttonl.value == True) and (ljinux.io.buttonr.value == True)):
                                global Exit
                                global Exit_code
                                Exit = True
                                Exit_code = 244
                except KeyboardInterrupt:
                    print("based: Caught Ctrl + C, press any key to drop to shell..")
            else:
                print("based: Init-type specified incorrectly, assuming oneshot")
            ljinux.io.led.value = True
            if not Exit:
                sys.stdin.read(1)
            while not Exit:
                try:
                    ljinux.based.shell()
                    gc.collect()
                except KeyboardInterrupt:
                    ljinux.io.led.value = False
                    print("^C\n",end='')
                    ljinux.io.led.value = True

        class command():
            def ls(dirr):
                argss_in = {}
                in_l = 0
                aa = False
                ll = False
                rett = ""
                directory_listing = os.listdir()
                try:
                    if ("-" == str(dirr[1])[:1]):
                        argss_in = list(str(dirr[1])[1:])
                except IndexError:
                    pass
                if ("l" in argss_in):
                    ll = True
                if ("a" in argss_in):
                    if ll:
                        print(".")
                        rett += (".")
                        print("..")
                        rett += ("..")
                    else:
                        print(".", end='   ')
                        rett += (".   ")
                        print("..", end='   ')
                        rett += ("..   ")
                    aa = True
                    in_l +=2
                for i in directory_listing:
                    if ((i)[:1] == "."):
                        if (aa):
                            if not (ll):
                                    print(i, end='   ')
                                    rett += (i + '   ')
                                    in_l += 1
                            else:
                                print(i)
                                rett += (i)
                                in_l += 1
                    else:
                        if not (ll):
                            print(i, end='   ')
                            rett += (i + '   ')
                            in_l += 1
                        else:
                            print(i)
                            rett += (i)
                            in_l +=1
                if not (ll):
                    print("\n", end='')
                    rett += ("\n")
                return rett

            def not_found(errr): # command not found
                print("based: " + errr[0] + ": command not found")

            def execc(whatt): # exec a file
                global Exit
                global Exit_code
                if (whatt[0] == "exec"):
                    for i in range(len(whatt)-1):
                        whatt[i] = whatt[i+1]

                try:
                    ljinux.io.led.value = False
                    f = open(whatt[0], 'r')
                    lines = f.readlines()
                    count = 0
                    ljinux.io.led.value = True
                    for line in lines:
                        ljinux.io.led.value = False
                        lines[count] = line.strip()
                        count += 1
                        ljinux.io.led.value = True
                    for commandd in lines:
                        ljinux.based.shell(commandd)
                    f.close()
                except OSError:
                    ljinux.io.led.value = True
                    print("based: "+ whatt[0] +": No such file or directory\n")

            def pwd(dirr): # print working directory
                print(os.getcwd())

            def helpp(dictt): # help
                for i in dictt.keys():
                    print(i)

            def echoo(what): # echo command
                try:
                    if (what[1].startswith("\"")):
                        if (what[1].endswith("\"")):
                            print(str(what[1])[1:-1])
                        else:
                            countt = len(what)
                            if (countt > 2):
                                if (what[countt-1].endswith("\"")):
                                    print(str(what[1])[1:],end=' ')
                                    for i in range(2, countt-1):
                                        print(what[i],end=' ')
                                    print(str(what[countt-1])[:-1])
                                else:
                                    pass
                    else:
                        act_dict = {'left_key': ljinux.io.left_key, 'right_key': ljinux.io.right_key, 'enter_key': ljinux.io.enter_key, 'serial_input': ljinux.io.serial}
                        if (what[1] in ljinux.based.user_vars):
                            print(ljinux.based.user_vars[what[1]])
                        elif (what[1] in act_dict):
                            print(act_dict[what[1]]())
                        else:
                            pass
                except IndexError:
                    pass

            def read(datatypee): # read value of device
                dataa = None
                readopts = {'left_key': ljinux.get_input.left_key, 'right_key': ljinux.get_input.right_key, 'enter_key': ljinux.get_input.enter_key, 'serial_input': ljinux.get_input.serial}
                try:
                    if (datatypee[1] in readopts):
                        dataa = readopts[datatypee[1]]()
                except IndexError:
                    print("Available read options: left_key, right_key, enter_key, serial_input")
                return dataa

            def exitt(returncode): # exit
                global Exit
                global Exit_code
                print("Bye")
                Exit = True
                try:
                    Exit_code = returncode[1]
                except IndexError:
                    pass

            def unamee(optt): # uname
                ljinux.io.led.value = False
                global Version
                try:
                    if (optt[1] == "-a"):
                        tt = time.localtime()
                        print("Ljinux Raspberry Pi Pico " + Version + " " + str(tt.tm_mday) + "/" + str(tt.tm_mon) + "/" + str(tt.tm_year) + " " + str(tt.tm_hour) + ":" + str(tt.tm_min) + ":" + str(tt.tm_sec) + " circuitpython Ljinux")
                except IndexError:
                    print("Ljinux")
                ljinux.io.led.value = True

            def cdd(optt): # cd
                ljinux.io.led.value = False
                try:
                    os.chdir(optt[1])
                except OSError:
                    print("Error: Directory does not exist")
                except IndexError:
                    pass
                ljinux.io.led.value = True

            def mkdiir(dirr): # mkdir
                global sdcard_fs
                ljinux.io.led.value = False
                try:
                    if not sdcard_fs:
                        storage.remount("/",False)
                    os.mkdir(dirr[1])
                    if not sdcard_fs:
                        storage.remount("/",True)
                except OSError as errr:
                    if (str(errr) == "[Errno 17] File exists"):
                        print("mkdir: cannot create directory ‘" + dirr[1] + "’: File exists")
                    else:
                        print("rmdir: cannot create directory ‘" + dirr[1] + "’: Cannot write, the pi pico is in read only mode!\nMake sure to disable to usb drive to be able to access these functions!")
                except IndexError:
                    pass
                ljinux.io.led.value = True

            def rmdiir(dirr): # rmdir
                global sdcard_fs
                ljinux.io.led.value = False
                try:
                    if not sdcard_fs:
                        storage.remount("/",False)
                    os.rmdir(dirr[1])
                    if not sdcard_fs:
                        storage.remount("/",True)
                except OSError as errr:
                    if (str(errr) == "[Errno 2] No such file/directory"):
                        print("rmdir: failed to remove ‘" + dirr[1] + "’: No such file or directory")
                    else:
                        print("rmdir: failed to remove ‘" + dirr[1] + "’: Cannot write, the pi pico is in read only mode!\nMake sure to disable to usb drive to be able to access these functions!")
                except IndexError:
                    pass
                ljinux.io.led.value = True

            def var(inpt, user_vars, system_vars): # system & user variables setter
                ljinux.io.led.value = False
                valid = True
                if (inpt[0] == "var"):
                    temp = inpt
                    del inpt
                    inpt = []
                    for i in range(len(temp)-1):
                        inpt.append(temp[i+1])
                try:
                    for chh in inpt[0]:
                        if not (chh.islower() or chh.isupper() or chh == "-"):
                            valid = False
                    if (inpt[1] == '='):
                        if not (inpt[2].startswith('"')):
                            if not (inpt[2].isdigit()):
                                valid = False
                    else:
                        valid = False
                    if valid:
                        new_var = ""
                        if (inpt[2].startswith("\"")):
                            countt = len(inpt)
                            if (inpt[2].endswith("\"")):
                                new_var = str(inpt[2])[1:-1]
                            elif ((countt > 3) and (inpt[countt-1].endswith("\""))):
                                new_var += (str(inpt[2])[1:] + ' ')
                                for i in range(3, countt-1):
                                    new_var += (inpt[i] + ' ')
                                new_var += (str(inpt[countt-1])[:-1])
                            else:
                                print("based: invalid syntax: 1")
                                valid = False
                        else:
                            new_var += str(inpt[2])
                    else:
                        print("based: invalid syntax: 2")
                        valid = False
                    if valid:
                        if (inpt[0] in system_vars):
                            if not (system_vars["security"] == "on"):
                                system_vars[inpt[0]] = new_var
                            else:
                                print("Cannot edit system variables, security is enabled.")
                        else:
                            user_vars[inpt[0]] = new_var
                except IndexError:
                    print("based: invalid syntax: 3")
                ljinux.io.led.value = True

            def display(inpt, objectss): # the graphics drawing stuff
                try:
                    typee = inpt[1] # "text / pixel / rectangle / line / circle / triangle / fill"
                    if (typee == "text"): # x, y, color, text in ""
                        xi = int(inpt[2])
                        yi = int(inpt[3])
                        txt = "" #inpt[5]
                        col = int(inpt[4])
                        if (inpt[5].startswith("\"")): # let's do some string proccessing!
                            countt = len(inpt) # get the numb of args
                            if (countt > 6):
                                txt += str(inpt[5])[1:] + " " # get the first word, remove last char (")
                                if (inpt[countt - 1].endswith("\"")):
                                    for i in range(6,countt-1): # make all the words one thicc string
                                        txt += str(inpt[i]) + " "
                                    txt += str(inpt[countt-1])[:-1] # last word without last char (")
                                else:
                                    # oh cmon wtfrick
                                    print("based: Input error")
                            else:
                                txt += str(inpt[5])[1:-1]
                        else:
                            print("based: Input error")
                        ljinux.farland.text(txt,xi,yi,col)
                    elif (typee == "dot"): # x,y,col
                        try:
                            xi = int(inpt[2])
                            yi = int(inpt[3])
                            col = int(inpt[4])
                            ljinux.farland.pixel(xi,yi,col)
                        except ValueError: # if he sends chars instead of numb
                            print("based: Input error")
                    elif (typee == "rectangle"): # x start, y start, x stop, y stop, color, mode (fill / border)
                        try:
                            xi = int(inpt[2])
                            yi = int(inpt[3])
                            xe = int(inpt[4])
                            ye = int(inpt[5])
                            col = int(inpt[6])
                            modd = inpt[7]
                            ljinux.farland.rect(xi,yi,xe,ye,col,modd)
                        except ValueError:
                            print("based: Input error")
                    elif (typee == "line"): # x start, y start, x stop, y stop, color
                        try:
                            xi = int(inpt[2])
                            yi = int(inpt[3])
                            xe = int(inpt[4])
                            ye = int(inpt[5])
                            col = int(inpt[6])
                            ljinux.farland.line(xi,yi,xe,ye,col)
                        except ValueError:
                            print("based: Input error")
                    elif (typee == "circle"): # x center, y center, rad, color, mode (fill/ border / template) TODO fix fill and do template
                        try:
                            xi = int(inpt[2])
                            yi = int(inpt[3])
                            radd = int(inpt[4])
                            col = int(inpt[5])
                            modd = inpt[6]
                            if (modd != "fill"):
                                ljinux.farland.draw_circle(xi,yi,radd,col)
                            else:
                                ljinux.farland.f_draw_circle(xi,yi,radd,col)
                            #ljinux.farland.entities{""}
                        except ValueError:
                            print("based: Input error")
                    elif (typee == "triangle"): # x point 1, y point 1, x point 2, y point 2, x point 3, y point 3, color, mode (fill/ border)
                        try:
                            xi = int(inpt[2])
                            yi = int(inpt[3])
                            xe = int(inpt[4])
                            ye = int(inpt[5])
                            xz = int(inpt[6])
                            yz = int(inpt[7])
                            col = int(inpt[8])
                            modd = inpt[9]
                            ljinux.farland.line(xi,yi,xe,ye,col)
                            ljinux.farland.line(xi,yi,xz,yz,col)
                            ljinux.farland.line(xz,yz,xe,ye,col)
                            if (modd == "fill"):
                                templ = ljinux.farland.virt_line(xi,yi,xe,ye)
                                for i in templ:
                                    ljinux.farland.ext_line(xz,yz,i[0],i[1],col)

                        except ValueError:
                            print("based: Input error")
                    elif (typee == "fill"): # color
                        try:
                            col = int(inpt[2])
                            ljinux.farland.fill(col)
                        except ValueError:
                            print("based: Input error")
                    elif (typee == "rhombus"): # todo
                        pass
                    elif (typee == "move"): # todo
                        pass
                    elif (typee == "delete"): #todo more
                        optt = inpt[2]
                        if (optt == "all"):
                            ljinux.farland.clear()
                        else:
                            print("based: Syntax error")
                    elif (typee == "refresh"):
                        ljinux.farland.frame()
                    else:
                        print("based: Syntax error")
                except IndexError:
                    print("based: Syntax error")

            def timme(inpt): # time command
                try:
                    if (inpt[1] == "set"):
                        try:
                            the_time = time.struct_time((int(inpt[4]),int(inpt[3]),int(inpt[2]),int(inpt[5]),int(inpt[6]),int(inpt[7]),1,-1,-1)) # yr, mon, d, hr, m, s, ss, shit,shit,shit
                            rtcc.write_datetime(the_time)
                        except IndexError:
                            print("based: Syntax error")
                except IndexError:
                    tt = time.localtime()
                    print("Current time: " + str(tt.tm_mday) + "/" + str(tt.tm_mon) + "/" + str(tt.tm_year) + " " + str(tt.tm_hour) + ":" + str(tt.tm_min) + ":" + str(tt.tm_sec))

            def suuu(inpt,system_vars): # su command but worse
                global dfpasswd
                if (dfpasswd == getpass()):
                    system_vars["security"] = "off"
                    print("Authentication successful. Security disabled.")
                else:
                    print("Authentication unsuccessful.")

            def playmp3(inpt): # play mp3
                try:
                    with open(inpt[1], "rb") as data:
                        mp3 = audiomp3.MP3Decoder(data)
                        a = audiopwmio.PWMAudioOut(board.GP15)
                        print("Playing")
                        try:
                            a.play(mp3)
                            while a.playing:
                                time.sleep(.2)
                                gc.collect()
                                if (ljinux.io.buttone.value == True):
                                    if a.playing:
                                        a.pause()
                                        print("Paused")
                                        time.sleep(.5)
                                        while a.paused:
                                            if ((ljinux.io.buttonl.value == True) and (ljinux.io.buttonr.value == True) and not (ljinux.io.buttone.value == True)):
                                                a.stop()
                                            elif (ljinux.io.buttone.value == True):
                                                a.resume()
                                                print("Resumed")
                                                time.sleep(.5)
                                            else:
                                                time.sleep(.1)
                        except KeyboardInterrupt:
                            a.stop()
                        a.deinit()
                        mp3.deinit()
                        print("Stopped")
                except OSError:
                    print("Based: File not found")

            def playwav(inpt): # play wav file
                try:
                    with open(inpt[1], "rb") as data:
                        wav = audiocore.WaveFile(data)
                        a = audiopwmio.PWMAudioOut(board.GP15)
                        print("Playing")
                        try:
                            a.play(wav)
                            while a.playing:
                                time.sleep(.2)
                                gc.collect()
                                if (ljinux.io.buttone.value == True):
                                    if a.playing:
                                        a.pause()
                                        print("Paused")
                                        time.sleep(.5)
                                        while a.paused:
                                            if ((ljinux.io.buttonl.value == True) and (ljinux.io.buttonr.value == True) and not (ljinux.io.buttone.value == True)):
                                                a.stop()
                                            elif (ljinux.io.buttone.value == True):
                                                a.resume()
                                                print("Resumed")
                                                time.sleep(.5)
                                            else:
                                                time.sleep(.1)
                        except KeyboardInterrupt:
                            a.stop()
                        a.deinit()
                        wav.deinit()
                        print("Stopped")
                except OSError:
                    print("Based: File not found")

            def neofetch(inpt): # picofetch / neofetch
                global Version
                global uptimee
                print("    `.::///+:/-.        --///+//-:``    ",end="")
                print(ljinux.based.system_vars["user"],end="")
                print("@pico")
                print("   `+oooooooooooo:   `+oooooooooooo:    ---------                        ")
                print("    /oooo++//ooooo:  ooooo+//+ooooo.    OS: Ljinux",end=" ")
                print(Version)
                print("    `+ooooooo:-:oo-  +o+::/ooooooo:     Host: Raspberry Pi Pico v1.0     ")
                print("     `:oooooooo+``    `.oooooooo+-      Kernel:",end=" ")
                print(Version)
                print("       `:++ooo/.        :+ooo+/.`       Uptime:",end=" ")
                neofetch_time = int(uptimee + time.monotonic())
                uptimestr = ""
                hours = neofetch_time // 3600 # Take out the hours
                neofetch_time -= hours * 3600 #
                minutes = neofetch_time // 60 # Take out the minutes
                neofetch_time -= minutes * 60 #
                if (hours > 0):
                    uptimestr += str(hours) + " hours, "
                if (minutes > 0):
                    uptimestr += str(minutes) + " minutes, "
                if (neofetch_time > 0):
                    uptimestr += str(neofetch_time) + " seconds"
                else:
                    uptimestr = uptimestr[:-2]
                print(uptimestr)
                print("          ...`  `.----.` ``..           Packages: 0 ()")
                print("       .::::-``:::::::::.`-:::-`        Shell: based 0.0.1")
                print("      -:::-`   .:::::::-`  `-:::-       WM: Farland")
                print("     `::.  `.--.`  `` `.---.``.::`      Terminal: TTYACM0")
                print("         .::::::::`  -::::::::` `       CPU: RP2040 (2) @ 133MHz")
                print("   .::` .:::::::::- `::::::::::``::.    Memory: " + str(int(264 - int(gc.mem_free())/1000)) + "KiB / 264KiB          ")
                print("  -:::` ::::::::::.  ::::::::::.`:::-")
                print("  ::::  -::::::::.   `-::::::::  ::::")
                print("  -::-   .-:::-.``....``.-::-.   -::-")
                print("   .. ``       .::::::::.     `..`..")
                print("     -:::-`   -::::::::::`  .:::::`")
                print("     :::::::` -::::::::::` :::::::.")
                print("     .:::::::  -::::::::. ::::::::")
                print("      `-:::::`   ..--.`   ::::::.")
                print("        `...`  `...--..`  `...`")
                print("              .::::::::::")
                print("               `.-::::-`")

            def rebooto(inpt): # reboot the whole microcontroller
                global Exit
                global Exit_code
                Exit = True
                Exit_code = 245

            def sensors(inpt): # lm-sensors
                print("%.2f" % microcontroller.cpu.temperature,end="")
                print("°C")

            def historgf(inpt): # history get full list
                try:
                    if (inpt[1] == "clear"):
                        ljinux.history.clear(ljinux.based.user_vars["history-file"])
                    elif (inpt[1] == "load"):
                        ljinux.history.load(ljinux.based.user_vars["history-file"])
                    elif (inpt[1] == "save"):
                        ljinux.history.save(ljinux.based.user_vars["history-file"])
                    else:
                        print("based: Invalid option")
                except IndexError:
                    ljinux.history.getall()

        def shell(inp=None):
            global Exit
            function_dict = {'ls':ljinux.based.command.ls, 'error':ljinux.based.command.not_found, 'exec':ljinux.based.command.execc, 'pwd':ljinux.based.command.pwd, 'help':ljinux.based.command.helpp, 'echo':ljinux.based.command.echoo, 'read':ljinux.based.command.read, 'exit':ljinux.based.command.exitt, 'uname':ljinux.based.command.unamee, 'cd':ljinux.based.command.cdd, 'mkdir':ljinux.based.command.mkdiir, 'rmdir':ljinux.based.command.rmdiir, 'var':ljinux.based.command.var, 'display':ljinux.based.command.display, 'time':ljinux.based.command.timme, 'su':ljinux.based.command.suuu, 'mp3':ljinux.based.command.playmp3, 'wav':ljinux.based.command.playwav, 'picofetch':ljinux.based.command.neofetch, 'reboot':ljinux.based.command.rebooto, 'sensors':ljinux.based.command.sensors, 'history':ljinux.based.command.historgf}
            command_input = False
            input_obj = ljinux.SerialReader()
            if not Exit:
                while ((command_input == False) or (command_input == "\n")):
                    if (inp == None):
                        print("[" + ljinux.based.system_vars["user"] + "@pico | " + os.getcwd() + "]> ", end='')
                        command_input = False
                        while (((not command_input) or (command_input == "")) and not Exit):
                            command_input = input_obj.read()  # read until newline, echo back chars
                            #mystr = usb_reader.read(end_char='\t', echo=False) # trigger on tab, no echo
                            gc.collect()
                            #time.sleep(.03)
                            try:
                                if (command_input[:1] != " "):
                                    ljinux.history.appen(command_input.strip())
                            except (AttributeError, TypeError):
                                pass
                    else:
                        command_input = inp
                if not Exit:
                    command_split = command_input.split()
                    ljinux.io.led.value = False
                    if not (command_input == ""):
                        try:
                            if (str(command_split[0])[:2] == "./"):
                                command_split[0] = str(command_split[0])[2:]
                                if (command_split[0] != ''):
                                    function_dict["exec"](command_split)
                                else:
                                    print("Error: No file specified")
                            elif ((command_split[0] in function_dict) and (command_split[0] not in ["error", "var", "help", "display", "su"])):
                                function_dict[command_split[0]](command_split)
                            elif (command_split[0] == "help"):
                                function_dict["help"](function_dict)
                            elif (command_split[0] == "display"):
                                global display_availability
                                if display_availability:
                                    function_dict["display"](command_split,ljinux.farland.entities)
                                else:
                                    print("based: Display not attached")
                            elif (command_split[0] == "su"):
                                function_dict["su"](command_split,ljinux.based.system_vars)
                            elif ((command_split[1] == "=") or (command_split[0] == "var")):
                                function_dict["var"](command_split, ljinux.based.user_vars, ljinux.based.system_vars)
                            else:
                                function_dict["error"](command_split)
                        except IndexError:
                            function_dict["error"](command_split)
                    ljinux.io.led.value = True

    class farland(object):
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
        entities = {}
        # ---
        
        def setup():
            global display_availability
            ljinux.io.led.value = False
            try:
                i2c = busio.I2C(board.GP17, board.GP16)  # SCL, SDA
                ljinux.farland.oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c) # I use the i2c cuz it ez
                ljinux.farland.oled.fill(0) # cuz why not
                ljinux.farland.oled.show()
                display_availability = True
            except RuntimeError:
                print("Failed to create display object, display functions will be unavailable")
            ljinux.io.led.value = True
        
        def frame():
            global display_availability
            if display_availability:
                ljinux.farland.oled.show()
        
        def clear():
            global display_availability
            if display_availability:
                ljinux.io.led.value = False
                ljinux.farland.oled.fill(0)
                ljinux.farland.oled.show()
                ljinux.io.led.value = True
        
        def pixel(x,y,col):
            ljinux.farland.oled.pixel(x, y, col)

        def fill(col):
            ljinux.farland.oled.fill(col)
        
        def text(strr,x,y,col):
            ljinux.farland.oled.text(strr,x,y,col)
        
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
            while (y<=rad):
                x=-rad
                while (x<=rad):
                    if ((x*x+y*y) < (rad*rad + rad*0.8)):
                        ljinux.farland.oled.pixel(xpos0+x, ypos0+y, col)
                        #setpixel(origin.x+x, origin.y+y)
                    x += 1
                y += 1
        
        def draw_top(): # to be made into an app
            for i in range(128):
                for j in range (11):
                    ljinux.farland.oled.pixel(i,j, True)
        
        def line(x0,y0,x1,y1,col):
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

        def ext_line(x0,y0,x1,y1,col):
            dx = abs(x1 - x0)
            dy = abs(y1 - y0)
            x, y = x0, y0
            sx = -1 if x0 > x1 else 1
            sy = -1 if y0 > y1 else 1
            if dx > dy:
                err = dx / 2.0
                while x != x1:
                    ljinux.farland.oled.pixel(int(x), int(y), col)
                    ljinux.farland.oled.pixel(int(x)+1, int(y), col)
                    ljinux.farland.oled.pixel(int(x)-1, int(y), col)
                    ljinux.farland.oled.pixel(int(x), int(y)+1, col)
                    ljinux.farland.oled.pixel(int(x), int(y)-1, col)
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
                        ljinux.farland.oled.pixel(int(x)+1, int(y), col)
                        ljinux.farland.oled.pixel(int(x)-1, int(y), col)
                    if not isInteger(y):
                        ljinux.farland.oled.pixel(int(x), int(y)+1, col)
                        ljinux.farland.oled.pixel(int(x), int(y)-1, col)
                    err -= dx
                    if err < 0:
                        x += sx
                        err += dy
                    y += sy
                ljinux.farland.oled.pixel(int(x), int(y), col)
                if not isInteger(x):
                    ljinux.farland.oled.pixel(int(x)+1, int(y), col)
                    ljinux.farland.oled.pixel(int(x)-1, int(y), col)
                if not isInteger(y):
                    ljinux.farland.oled.pixel(int(x), int(y)+1, col)
                    ljinux.farland.oled.pixel(int(x), int(y)-1, col)

        def virt_line(x0,y0,x1,y1):
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

        def rect(x0,y0,x1,y1,col,modee):
            if (modee == "border"):
                if (x0 < x1):
                    for i in range(x0,x1):
                        ljinux.farland.oled.pixel(i, y0, col)
                        ljinux.farland.oled.pixel(i, y1, col)
                else:
                    for i in range(x1,x0):
                        ljinux.farland.oled.pixel(i, y0, col)
                        ljinux.farland.oled.pixel(i, y1, col)
                if (y0 < y1):
                    for i in range(y0,y1):
                        ljinux.farland.oled.pixel(x0, i, col)
                        ljinux.farland.oled.pixel(x1, i, col)
                else:
                    for i in range(x1,x0):
                        ljinux.farland.oled.pixel(x0, i, col)
                        ljinux.farland.oled.pixel(x1, i, col)
            elif (modee == "fill"):
                if ((x0<x1) and (y0<y1)):
                    for i in range(x0,x1):
                        for j in range(y0,y1):
                            ljinux.farland.oled.pixel(i, j, col)
                elif ((x0<x1) and (y1>y0)):
                    for i in range(x0,x1):
                        for j in range(y0,y1,-1):
                            ljinux.farland.oled.pixel(i, j, col)
                elif ((x0>x1) and (y1<y0)):
                    for i in range(x0,x1,-1):
                        for j in range(y0,y1):
                            ljinux.farland.oled.pixel(i, j, col)
                elif ((x0>x1) and (y1>y0)):
                    for i in range(x0,x1,-1):
                        for j in range(y0,y1,-1):
                            ljinux.farland.oled.pixel(i, j, col)
                else:
                    print("based: syntax error")


        
        #clock functions, to be made part of hs
        
        # init the clock
        def draw_init_clock():
            ljinux.farland.oled.text("0", ljinux.farland.poss[0] + ljinux.farland.offs, 2, False)
            ljinux.farland.oled.text("0", ljinux.farland.poss[1] + ljinux.farland.offs, 2, False)
            ljinux.farland.oled.text("0", ljinux.farland.poss[2] + ljinux.farland.offs, 2, False)
            ljinux.farland.oled.text("0", ljinux.farland.poss[3] + ljinux.farland.offs, 2, False)
        
        # each time increments if monotonic has gone up
        def draw_clock():
            ljinux.farland.timm_in = int(time.monotonic())
            if (ljinux.farland.timm_in != ljinux.farland.timm_old):
                ljinux.farland.timm_old = ljinux.farland.timm_in
                if (ljinux.farland.tp[3] != 9):
                    ljinux.farland.oled.text(str(ljinux.farland.tp[3]), ljinux.farland.poss[3] + ljinux.farland.offs, 2, True)
                    ljinux.farland.tp[3] += 1
                    ljinux.farland.oled.text(str(ljinux.farland.tp[3]), ljinux.farland.poss[3] + ljinux.farland.offs, 2, False)
                elif (ljinux.farland.tp[2] != 5):
                    ljinux.farland.oled.text(str(ljinux.farland.tp[3]), ljinux.farland.poss[3] + ljinux.farland.offs, 2, True)
                    ljinux.farland.tp[3] = 0
                    ljinux.farland.oled.text(str(ljinux.farland.tp[3]), ljinux.farland.poss[3] + ljinux.farland.offs, 2, False)
                    ljinux.farland.oled.text(str(ljinux.farland.tp[2]), ljinux.farland.poss[2] + ljinux.farland.offs, 2, True)
                    ljinux.farland.tp[2] += 1
                    ljinux.farland.oled.text(str(ljinux.farland.tp[2]), ljinux.farland.poss[2] + ljinux.farland.offs, 2, False)
                elif (ljinux.farland.tp[1] != 9):
                    ljinux.farland.oled.text(str(ljinux.farland.tp[3]), ljinux.farland.poss[3] + ljinux.farland.offs, 2, True)
                    ljinux.farland.tp[3] = 0
                    ljinux.farland.oled.text(str(ljinux.farland.tp[3]), ljinux.farland.poss[3] + ljinux.farland.offs, 2, False)
                    ljinux.farland.oled.text(str(ljinux.farland.tp[2]), ljinux.farland.poss[2] + ljinux.farland.offs, 2, True)
                    ljinux.farland.tp[2] = 0
                    ljinux.farland.oled.text(str(ljinux.farland.tp[2]), ljinux.farland.poss[2] + ljinux.farland.offs, 2, False)
                    ljinux.farland.oled.text(str(ljinux.farland.tp[1]), ljinux.farland.poss[1] + ljinux.farland.offs, 2, True)
                    ljinux.farland.tp[1] += 1
                    ljinux.farland.oled.text(str(ljinux.farland.tp[1]), ljinux.farland.poss[1] + ljinux.farland.offs, 2, False)
                elif (ljinux.farland.tp[0] != 5):
                    ljinux.farland.oled.text(str(ljinux.farland.tp[3]), ljinux.farland.poss[3] + ljinux.farland.offs, 2, True)
                    ljinux.farland.tp[3] = 0
                    ljinux.farland.oled.text(str(ljinux.farland.tp[3]), ljinux.farland.poss[3] + ljinux.farland.offs, 2, False)
                    ljinux.farland.oled.text(str(ljinux.farland.tp[2]), ljinux.farland.poss[2] + ljinux.farland.offs, 2, True)
                    ljinux.farland.tp[2] = 0
                    ljinux.farland.oled.text(str(ljinux.farland.tp[2]), ljinux.farland.poss[2] + ljinux.farland.offs, 2, False)
                    ljinux.farland.oled.text(str(ljinux.farland.tp[1]), ljinux.farland.poss[1] + ljinux.farland.offs, 2, True)
                    ljinux.farland.tp[1] = 0
                    ljinux.farland.oled.text(str(ljinux.farland.tp[1]), ljinux.farland.poss[1] + ljinux.farland.offs, 2, False)
                    ljinux.farland.oled.text(str(ljinux.farland.tp[0]), ljinux.farland.poss[0] + ljinux.farland.offs, 2, True)
                    ljinux.farland.tp[0] += 1
                    ljinux.farland.oled.text(str(ljinux.farland.tp[0]), ljinux.farland.poss[0] + ljinux.farland.offs, 2, False)
                ljinux.farland.poin = not (ljinux.farland.poin)
                ljinux.farland.oled.text(":", ljinux.farland.poss[4] + ljinux.farland.offs, 2, ljinux.farland.poin)
        
        def fps():
            if ((ljinux.farland.frame_poi <= 9)):
                ljinux.farland.time_new = time.monotonic()
                ljinux.farland.frames[ljinux.farland.frame_poi] = ljinux.farland.time_new - ljinux.farland.time_old
                ljinux.farland.time_old = time.monotonic()
                if ljinux.farland.frames_suff:
                    ljinux.farland.frames_av()
                ljinux.farland.frame_poi += 1
            else :
                ljinux.farland.frames_suff = True
                ljinux.farland.frames_av()
                ljinux.farland.frame_poi = 0
        
        def frames_av():
            average = 0
            for i in range(10):
                average += ljinux.farland.frames[i]
                average = 1/ (average / 10)
            print(average)

    class get_input(object):
        def left_key():
            if (ljinux.io.buttonl.value == True):
                return True
            else:
                return False

        def right_key():
            if (ljinux.io.buttonr.value == True):
                return True
            else:
                return False

        def enter_key():
            if (ljinux.io.buttone.value == True):
                return True
            else:
                return False

        def serial():
            return input()

def lock(it_is): # to be made part of hs app
    if (it_is):
        oss.farland.pixel(2, 9, False)
        oss.farland.pixel(3, 9, False)
        oss.farland.pixel(4, 9, False)
        oss.farland.pixel(5, 9, False)
        oss.farland.pixel(6, 9, False)
        oss.farland.pixel(7, 9, False)
        oss.farland.pixel(8, 9, False)
        oss.farland.pixel(2, 8, False)
        oss.farland.pixel(3, 8, False)
        oss.farland.pixel(4, 8, False)
        oss.farland.pixel(5, 8, False)
        oss.farland.pixel(6, 8, False)
        oss.farland.pixel(7, 8, False)
        oss.farland.pixel(8, 8, False)
        oss.farland.pixel(2, 7, False)
        oss.farland.pixel(3, 7, False)
        oss.farland.pixel(4, 7, False)
        oss.farland.pixel(6, 7, False)
        oss.farland.pixel(7, 7, False)
        oss.farland.pixel(8, 7, False)
        oss.farland.pixel(2, 6, False)
        oss.farland.pixel(3, 6, False)
        oss.farland.pixel(4, 6, False)
        oss.farland.pixel(5, 6, False)
        oss.farland.pixel(6, 6, False)
        oss.farland.pixel(7, 6, False)
        oss.farland.pixel(8, 6, False)
        oss.farland.pixel(2, 5, False)
        oss.farland.pixel(3, 5, False)
        oss.farland.pixel(4, 5, False)
        oss.farland.pixel(5, 5, False)
        oss.farland.pixel(6, 5, False)
        oss.farland.pixel(7, 5, False)
        oss.farland.pixel(8, 5, False)
        #the hinge thing
        oss.farland.pixel(7, 4, False)
        oss.farland.pixel(7, 3, False)
        oss.farland.pixel(6, 2, False)
        oss.farland.pixel(5, 2, False)
        oss.farland.pixel(4, 2, False)
        oss.farland.pixel(3, 3, False)
        oss.farland.pixel(3, 4, False)
        oss.farland.pixel(3, 5, False)
    else:
        oss.farland.pixel(2, 9, False)
        oss.farland.pixel(3, 9, False)
        oss.farland.pixel(4, 9, False)
        oss.farland.pixel(5, 9, False)
        oss.farland.pixel(6, 9, False)
        oss.farland.pixel(7, 9, False)
        oss.farland.pixel(8, 9, False)
        oss.farland.pixel(2, 8, False)
        oss.farland.pixel(3, 8, False)
        oss.farland.pixel(4, 8, False)
        oss.farland.pixel(5, 8, False)
        oss.farland.pixel(6, 8, False)
        oss.farland.pixel(7, 8, False)
        oss.farland.pixel(8, 8, False)
        oss.farland.pixel(2, 7, False)
        oss.farland.pixel(3, 7, False)
        oss.farland.pixel(4, 7, False)
        oss.farland.pixel(6, 7, False)
        oss.farland.pixel(7, 7, False)
        oss.farland.pixel(8, 7, False)
        oss.farland.pixel(2, 6, False)
        oss.farland.pixel(3, 6, False)
        oss.farland.pixel(4, 6, False)
        oss.farland.pixel(5, 6, False)
        oss.farland.pixel(6, 6, False)
        oss.farland.pixel(7, 6, False)
        oss.farland.pixel(8, 6, False)
        oss.farland.pixel(2, 5, False)
        oss.farland.pixel(3, 5, False)
        oss.farland.pixel(4, 5, False)
        oss.farland.pixel(5, 5, False)
        oss.farland.pixel(6, 5, False)
        oss.farland.pixel(7, 5, False)
        oss.farland.pixel(8, 5, False)
        #the hinge thing
        oss.farland.pixel(7, 3, False)
        oss.farland.pixel(6, 2, False)
        oss.farland.pixel(5, 2, False)
        oss.farland.pixel(4, 2, False)
        oss.farland.pixel(3, 3, False)
        oss.farland.pixel(3, 4, False)
        oss.farland.pixel(3, 5, False)
dmtex("Func loads complete")
oss = ljinux()
dmtex("OS object created")
oss.farland.setup()
dmtex("Display object created")
#oss.farland.draw_top()
#oss.farland.draw_init_clock()

#with open("/boot_out.txt", "r") as file:
#    if 'Unlocked' in file.read():
#        lock(False)
#    else:
#        lock(True)
#    file.close()

oss.farland.frame()
time.sleep(.4)
dmtex("System init done")

# initial center of the circle
#center_x = 64
#center_y = 40
# how fast does it move in each direction
#x_inc = 1
#y_inc = 1
# what is the starting radius of the circle
#radius = 8
frame_time_old = time.monotonic()
frame_time_new = None

try:
    while not Exit:
        dmtex("Running autorun")
        oss.based.autorun()
        ## undraw the previous circle
        #oss.farland.draw_circle(center_x, center_y, radius, col=0)
        #
        ## if bouncing off right
        #if center_x + radius >= oss.farland.width():
        #    # start moving to the left
        #    x_inc = -1
        ## if bouncing off left
        #elif center_x - radius < 0:
        #    # start moving to the right
        #    x_inc = 1
        #
        ## if bouncing off top
        #if center_y + radius >= oss.farland.height():
        #    # start moving down
        #    y_inc = -1
        ## if bouncing off bottom
        #elif center_y - radius < 0 + 12:
        #    # start moving up
        #    y_inc = 1
        #
        ## go more in the current direction
        #center_x += x_inc
        #center_y += y_inc
        #
        ## draw the new circle
        #oss.farland.draw_circle(center_x, center_y, radius)
        # show all the changes we just made
        #oss.farland.draw_clock()
        #oss.farland.frame()
        #oss.farland.fps()
        gc.collect()
        print("Shell exited with exit code ", end="")
        print(Exit_code,end="\n\n")
except EOFError:
    print("\nAlert: Serial Ctrl + D caught, exiting\n")
ljinux.io.led.value = False
ljinux.farland.clear()
print("[ OK ] Cleared display")
ljinux.history.save(ljinux.based.user_vars["history-file"])
print("[ OK ] History flush")
os.chdir("/")
print("[ OK ] Switched to Picofs")
gc.collect()
print("[ OK ] Cleared garbage")
os.sync()
print("[ OK ] Sync all volumes")
ljinux.io.led.value = True
try:
    ljinux.io.led.value = False
    storage.umount("/ljinux")
    print("[ OK ] Unmount /ljinux")
    ljinux.io.led.value = True
except OSError:
    pass
print("[ OK ] Reached target: Quit")
ljinux.io.led.value = False
if (Exit_code == 245):
    microcontroller.reset()
elif (Exit_code == 244):
    print("[ OK ] Reached target: Halt")
    while True:
        time.sleep(3600)
else:
    sys.exit(Exit_code)
