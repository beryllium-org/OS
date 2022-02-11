# Ljinux
A "linux" written in python, for the Raspberry Pi Pico.<br />

Important note:<br />

Do not take this project seriously.<br />
I know it's not a linux, or an os, or anything in that regard, but here we are.<br />

<h3>Anyways, since you are still reading let's start with the basics.</h3>
It runs on the rpi pico, circuitpython.<br />
As for the display I use a SSD1306 over I2C, it's optional tho.<br />
If the display is not available, all graphics functions will be disabled.<br />
You can attach an ds1302 rtc.<br />
If you attach one, remove "fixrtc" from the config.json during deployment, or from the development mode.<br />
The timings will work correctly though.<br />
Networking can be achieved by attaching a w5500 breakout board.<br />
It expects to find a /LjinuxRoot folder which uses as it's root. It can be on the built in fs, or an sd card, more details at Configuration.<br />

It's structure:<br />

It's shell which is named <b>based</b>, is the only thing available to use with it. You will be able to use python too with it in the future.<br />
You can execute commands over serial to it, or by feeding them from a Init.lja<br />
The Init.lja has to be at /ljinux/boot/ of the pi pico or on the /boot/ of the attached sd card.<br />

<h2>Installation to a fresh pi pico:</h2><br />

Install Circuitpython version 7.1.1,<br />
And unzip this entire repo, except for the "source" folder onto the CIRCUITPY drive.<br />
Then eject it and fully disconnect it from the pc. (It is important to power cycle the pi.)<br />
When it's plugged back in, it should run automatically and you can connect to it via serial. (You can use putty on windows, or gnu/screen on gnu/linux)

<h3>Configuration</h3>

<b>GPIO PINS:</b><br />For display GP17(scl), GP16(sda)<br />For rtc GP6(clk), GP7(data), GP8(ce)<br />button left GP19 - button right GP18 - button enter GP20<br />For buzzer GP15<br />For sdcard GP2(clk),GP3(mosi),GP4(miso), GP5(cs)<br />For ethernet GP10(clk), GP13(cs), GP11(mosi), GP12(miso),<br />

<b>IMPORTANT NOTE: To make the pi appear as a usb device, run the command "devmode".</b><br />

More stuff will be added later as the project spirals into chaos.<br />

<h3>Build instructions for linux:</h3>

In order to build & upload a binary different than the one provided to the pico, enable developer mode on the pico and from within the "source" folder, run make.<br />
The binary will be automatically uploaded to the pico and be used upon the next reload/reboot of the device.

<h3>Ljinux Manual:</h3>


based built-in commands:<br />

```
help [COMMAND]

OUTPUTS A BASIC LIST OF COMMANDS TO SERIAL OUT

cd [DIR]...

CHANGES TO SPECIFIED DIRECTORY


echo [DATA]...

PRINT SOME VARIABLES OR TEXT ONTO SERIAL OUT


var [DATA]...

CREATE A NEW VARIABLE. SYNTAX: var a = "ok"
NUMBERS DO NOT NEED BRACKETS.
THE COMMAND ITSELF IS OPTIONAL (a = "is also valid")


uname [-a]

OUTPUTS THE INFO ABOUT THE DEVICE TO SERIAL OUT


mkdir [DIR]...

MAKE A NEW DIRECTORY


rmdir [DIR]...

DELETE A DIRECTORY


rm [FILE]...

DELETE A FILE


ls [OPTIONS]... [DIR]...

OUTPUTS THE DIRECTORY LISTING TO SERIAL OUT


pwd

OUTPUTS THE CURRENT DIRECTORY TO SERIAL OUT


display [OPERATION] [OPERATION DATA]

DISPLAYS SOMETHING ON THE I2C DISPLAY
RETURNS OBJECT ID, DO NOT LOSE IT
BUDGET DIDNT ALLOW PORTING WAYLAND, SO I MADE FARLAND
OPERATIONS:

dot

line

rectangle

square

circle

rhombus

move

delete


exec [FILE]

LOADS AN .lja FILE AND EXECUTES IT'S COMMANDS


wait [TIME]

IN SECONDS


goto [LINE]

GOTO INTERPRETED LINE AND RERUN FROM THERE


exit [CODE]

EXIT THE CURRENT PROCESS WITH AN EXIT CODE, DEFAULT = 0


time [set]...

VIEW THE TIME, OR SET IT
VALID FORMAT "time set dd mm yyyy hr mm ss"


su

DISABLE SECURITY, ASKS FOR PASSWORD
DEFAULT PASSWORD == Ljinux


picofetch

NEOFETCH FOR THE PICO OFC


history [save/load/clear]

DISPLAYS THE HISTORY


webserver [args]

A INTEGRATED WEBSERVER
UNLESS A PATH IS GIVEN AS AN ARGUMENT, IT WILL TRY TO SERVE /ljinux/var/www/default/
SEND "webserver -k" TO KILL


devmode

ENABLES USB ACCESS AND OTHER DEVELOPMENT FEATURES
THIS PROHIBITS WRITE ACCESS TO THE BUILT IN FILESYSTEM


pexec [python commands]

RUNS PYTHON COMMANDS -- EXPERIMENTAL

reboot [mode]

REBOOTS THE MICROCONTROLLER
OPTIONALLY YOU CAN PASS A REBOOT MODE (safemode, uf2, bootloader)

dmesg

PRINTS OUT THE DMESG LOG

```

<h3>Config.json</h3>
It is equivelant to the config.txt of a raspi, however much more janky.<br /><br />

example config:<br />
```
{
"fixrtc": true
"displaySCL": 17
"displaySDA": 16
}
```
