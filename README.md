# ljinux
A "linux" written in 🅱️ython, for the pi pico.

Disclaimer: 

Do not take this project seriously. Code contains UwU's and Awooo's.
I know it's not a linux, or an os, or anything in that regard, but.. making it look like one, makes it funnier.

<h3>Anyways, since you are still reading let's start with the basics.</h3>
It runs on the rpi pico, circuitpython.
As for the display I use a SSD1306 over I2C, it's optional tho.

It's basics:
there are no basics, it's all a complex mess.

It's shell which is named <b>based</b>, is the only programming language it has.
You can execute commands over serial to it, or by feeding them from a autorun.lja

based commands:
```
help [COMMAND]

OUTPUTS A BASIC LIST OF COMMANDS TO SERIAL OUT


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


load [FILE]

LOADS AN .lja FILE AND EXECUTES IT'S COMMANDS
```

More stuff will be added later as the project progresses into complete mayhem.
