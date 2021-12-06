# ljinux
A "linux" written in 🅱️ython, for the pi pico.

Disclaimer: 

Do not take this project seriously. Code contains UwU's and Awooo's.
I know it's not a linux, or an os, or anything in that regard, but.. making it look like one, makes it funnier.

Also, it's wip.

<h3>Anyways, since you are still reading let's start with the basics.</h3>
It runs on the rpi pico, circuitpython.
As for the display I use a SSD1306 over I2C, it's optional tho.

It's basics:
there are no basics, this project is a dumpster fire.

It's shell which is named <b>based</b>, is the only programming language it has.
You can execute commands over serial to it, or by feeding them from a Init.lja

<h2>Installation to a fresh pi pico:</h2>

Install Circuitpython version 7.x,  
copy over the display library to /lib along with the framebuf library,  
and unzip this repo onto the CIRCUITPY drive

<b>IMPORTANT NOTE: unless the GP0 and GP1 pins are connected the drive will no longer appear after a powercycle.</b>

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
```

More stuff will be added later as the project progresses into complete mayhem.
