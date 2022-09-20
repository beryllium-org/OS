# Ljinux 
A "linux" written in python, for CircuitPython powered microcontrollers.<br />
[![build](https://github.com/bill88t/ljinux/actions/workflows/Compiletest.yml/badge.svg)](https://github.com/bill88t/ljinux/actions/workflows/Compiletest.yml)
[![Black Formatting](https://github.com/bill88t/ljinux/actions/workflows/black.yml/badge.svg)](https://github.com/bill88t/ljinux/actions/workflows/black.yml)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<br />
![neofetch](https://github.com/bill88t/ljinux/blob/main/other/screenshots/bneofetch.png)
<br />
Important notes:<br />
Do not take this project seriously.<br />
This is not a real os / linux distribution, but here we are.<br />
Also, it's still in an alpha state.<br /><br />

<b><i>We also now have a [discord](https://discord.gg/V8AejwGpCv) server!<br />
If you need support or want to hang out, feel free to join in!</i></b><br /><br />

Anyways, since you are still reading...<br />

Table of Contents
=================
* [Prerequisites](#prerequisites-and-optional-hardware)<br />
* [Installation / updating](#installation--updating)
* [Configuration](#configuration)
* [Connection](#connection)
* [Directory structure](#directory-structure)
* [Contributors](#contributors)
* [Manual](#a-complete-ljinux-manual-is-available)
* [Useful resources](#useful-resources-that-helped-with-the-development-of-this-project)

<br />

## Prerequisites and optional hardware

Runs on circuitpython 7.3.X or 8.0.X.<br />
At the moment the supported microcontrollers are:<br /><br />

 - Raspberry Pi Pico<br />
 - Raspberry Pi Pico W <br />
   Notice: Wifi still doesn't work correctly.<br />
 - Waveshare RP2040-Zero <br />
 - Adafruit KB2040 <br />
 - Waveshare ESP32-S2-Pico <br />
 - Adafruit Feather ESP32-S2 <br />
 - Pimoroni Pico Lipo (16mb) <br />

But it can probably run on many more.<br />
The only real limiting factor should be ram, as about 120k are needed for the system to even function.<br />
<i>(If you have gotten it running on an unsupported board, feel free to pr a configuration file)</i><br />

<br />Optional hardware compatible with ljinux:<br />
 - SSD1306 displays for display output<br />
 - sdcard breakout boards for more storage<br />
 - w5500 networking breakouts board for networking.<br />

For the missing hardware the functions will be automatically deactivated. (The hardware will also be deactivated in case of missing libraries.)<br />
It expects to find a <code>/LjinuxRoot</code> folder which uses as it's root. It can be on the built in fs, or an sd card.<br />
More info in Configuration.<br />

Ljinux's shell is named <b>based</b> and is equivelant to gnu bash.<br />
Python commands can also be used with the pexec command.<br />
Whole .py files can be run with the use of the fpexec command.<br />
They all run in the same scope as ljinux for ease of use. Security is not a priority on a microcontroller. Especially at the cost of ram.<br />
You can connect to it over usb serial, or by providing startup commands via a <code>Init.lja</code> file.<br />
The <code>Init.lja</code> has to be at <code>/LjinuxRoot/boot/</code> of the board's internal storage or on the <code>/boot/</code> of the attached sd card.<br />
It has it's own curses library, jcurses.<br />
And it's own display "compositor", farland.<br /><br />

## Installation / Updating

1) Install a supported CircuitPython version onto the board<br />
    Detailed instructions regarding CircuitPython can be found [here](https://learn.adafruit.com/welcome-to-circuitpython).<br />
2) Clone (or download this repository) and from within the "source" folder, run <code>make install</code>.<br />
    If you are on windows (why are you such a masochist), run the <code>windows-install.bat</code>.<br />
    To update on windows, run the <code>windows-update.bat</code>.<br />
    This command will automatically update the system files if they already exist.<br />
    To only update the wanna-be kernel run <code>make</code> instead.<br />
    (For this to work you need to have python3 installed, even on windows, and the board attached & mounted.)<br />
3) *(Optional)* To include drivers to the installation run <code>make *device name*</code>.<br />
    The currently available drivers are: <code>wifi</code>, <code>w5500</code><br />
    For windows, you can run instead the respective bat file.<br />
4) Eject & power off the board. (This is an important step.)<br />
    When it's plugged back in, it should run automatically and you can connect to it via serial. (You can use putty on windows, or gnu/screen on gnu/linux)<br />
    An automated connection script exists in the form of <code>make connection</code><br />
<b>IMPORTANT NOTE: To make the pi appear as a usb device on the host, run the ljinux command </b><code>devmode</code><br />
<br />

## Configuration

<i>Each board has it's own different pin configuration. You can see the defaults and modify them from the board's respecive config file.</i><br /><br />

<b>Libraries needed for optional hardware:</b><br />
For the SSD1306 display: <code>adafruit_ssd1306 adafruit_framebuf</code><br />
Sdcard: <code>adafruit_sdcard adafruit_bus_device</code><br />
    The sdcard has to be formatted as Fat32 / Fat16 or equivelant.<br />
Ethernet: Handled by <code>make</code><br /><br />

The neccessary libraries can be found [here](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases)<br />
Download the zip (The 7.x-mpy variant), extract it & copy the libraries you want onto <code>/lib</code> of the board.<br /><br />


## Connection
For an automated way on Linux/MacOS, run <code>make connection</code>. Manual way below.<br /><br />

To connect to the board it's recommended to use Putty for Windows and GNU/Screen for Linux/MacOS.<br />
For Putty, select connection type to be Serial, select the port to be COM<b>X</b> where <b>X</b> is the number of the serial port allocated by the board and set the speed/baudrate to 115200. (You can find which com port is allocated from within the Device Manager, it usually is COM3 or COM4)<br /><br />

For GNU/Screen, if you are on linux, you need to be in the <code>dialout</code> user group and to connect, run: <code>screen /dev/ttyACM0 115200</code><br />If you are on a Mac instead, run: <code>ls /dev/tty.usb*</code> to find the device name, and connect to it by running: <code>screen /dev/tty.usb\<Device name here\> 115200</code><br />
Example: <code>screen /dev/tty.usbmodem12210 115200</code><br /><br />
To disconnect, press Ctrl + A, K and confirm with y.<br />
To be added to the <code>dialout</code> group, run <code>sudo usermod -a -G dialout \<your username here\></code><br /><br />
 
## Directory structure

<ul>
<li><code>LjinuxRoot</code>, the root filesystem for ljinux. It should be copied as is to the board.</li>
<li><code>rootfilesystem</code>, the files needed in the root of the board. These should also be copied as is.</li>
<li><code>scripts</code>, the files needed for compilation, and installation to a board. They should not be copied over,</li>
<li><code>source</code>, the source files for ljinux and co. They should be compiled into .mpy files and put in /lib of the board.</li>
<li><code>packages</code>, ljinux featured packages and preinstalled software, coming soon.</li>
<li><code>other</code>, miscellaneous files</li>
</ul>
<br />

## Contributors

 -> [bill88t](https://github.com/bill88t) - @bill88t#4044
 <br />-> [Marios](https://github.com/mariospapaz) - @mariospapaz#2188
 <br />-> [mdaadoun](https://github.com/mdaadoun) - @mdaadoun#4475
 <br />-> [markbirss](https://github.com/markbirss)
 <br />-> [RetiredWizard](https://github.com/RetiredWizard)
 <br />

## A complete Ljinux manual is available

 https://github.com/bill88t/ljinux/blob/main/Manual.txt<br />
 <br />

## Additional screenshots
![less](https://github.com/bill88t/ljinux/blob/main/other/screenshots/less.png)
![extra commands](https://github.com/bill88t/ljinux/blob/main/other/screenshots/some.png)

## Useful resources that helped with the development of this project
 https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797<br />
 https://en.wikipedia.org/wiki/ANSI_escape_code<br />
 https://github.com/todbot/circuitpython-tricks<br />
<br />

More stuff will be added later as the project spirals into chaos.
