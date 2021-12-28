# ljinux [![CI](https://github.com/bill88t/ljinux/actions/workflows/main.yml/output/badge.svg)](https://github.com/bill88t/ljinux/actions/workflows/main.yml)
A "linux" written in python, for the Raspberry Pi Pico.

Important note:

Do not take this project seriously.
I know it's not a linux, or an os, or anything in that regard, but here we are.

Also, it's quality is alpha-stage at best.

<h3>Anyways, since you are still reading let's start with the basics.</h3>
It runs on the rpi pico, circuitpython.
As for the display I use a SSD1306 over I2C, it's optional tho.
You can attach an rtc, I used a ds1302. If you don't attach one, expect borked timestamps, nothing else.
It expects to find a /ljinux folder which uses as it's root. It can be on the built in fs, or an sd card, more details at Configuration.

It's basics:

It's shell which is named <b>based</b>, is the only programming language it has.
You can execute commands over serial to it, or by feeding them from a Init.lja
The Init.lja has to be at /ljinux/boot/ of the pi pico, or on /boot/ of the attached sd card.

<h2>Installation to a fresh pi pico:</h2>

Install Circuitpython version 7.x,  
and unzip this repo onto the CIRCUITPY drive

<h3>Configuration</h3>

<b>GPIO PINS:</b> GP0,GP1 for usb drive access - rtc GP6(clk),GP7(data),GP8(ce) - button left GP12 - button right GP12 - button enter GP11 - buzzer GP15 - sdcard GP2(clk),GP3(mosi),GP4(miso)

<b>IMPORTANT NOTE: unless the GP0 and GP1 pins are connected the drive will no longer appear after a powercycle.</b>
That needs to be done for the os to have rw access to the built in fs.

based commands:
```
help [COMMAND]

OUTPUTS A BASIC LIST OF COMMANDS TO SERIAL OUT

cd [DIR]...

CHANGES TO SPECIFIED DIRECTORY


read [left_key / right_key / enter_key / serial_input]...

READ DATA FROM SPECIFIED SOURCE AND RETURN THEM


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
```

More stuff will be added later as the project spirals into chaos.
