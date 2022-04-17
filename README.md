# Ljinux 
A "linux" written in python, for CircuitPython powered microcontrollers.<br />
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a><br />

Important note:<br />
Do not take this project seriously.<br />
This is not a real os / linux distribution, but here we are.<br /><br />

We also now have a [discord](https://discord.gg/V8AejwGpCv) server! If you need help, feel free to hop on for some support.<br /><br />

<h3>Anyways, since you are still reading let's start with the basics.</h3>
Depends on circuitpython 7.<br />
At the moment the supported microcontrollers are:<br />
 - Raspberry Pi Pico <br />
 - Waveshare RP2040-Zero <br />
But it can probably run on many more.<br />
The only real limiting factor should be ram, as about 150k are needed for the system to even function.<br />
If you have gotten it running on an unsupported board, feel free to pr a configuration file.<br /><br />

<br />You can optionally attach a SSD1306 display for output, a ds1302 RTC <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(make sure to set <code>fixrtc</code> to false from <code>config</code> file)<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;for persistent time or a w5500 networking breakout board for networking.<br />

For the missing hardware the functions will be automatically deactivated. (The hardware will also be deactivated in case of missing libraries.)<br />
It expects to find a <code>/LjinuxRoot</code> folder which uses as it's root. It can be on the built in fs, or an sd card.<br />
More info in Configuration.<br />

It's structure:<br />

It's shell which is named <b>based</b>, is equivelant to gnu bash.<br />Python can also be used with the pexec command.<br />
You can execute commands over serial to it, or by feeding them from a <code>Init.lja</code> file.<br />
The <code>Init.lja</code> has to be at <code>/LjinuxRoot/boot/</code> of the board's internal storage or on the <code>/boot/</code> of the attached sd card.<br />

<h2>Installation to a fresh board:</h2><br />

<i>Note: Windows not supported. Linux & MacOS only.</i><br /><br />

1) Install CircuitPython 7.X.X onto the board (pi pico uf2 file can be found [here](https://circuitpython.org/board/raspberry_pi_board) & detailed instructions regarding CircuitPython can be found [here](https://learn.adafruit.com/welcome-to-circuitpython)).<br />
2) Clone (or download this project) and from within it run <code>make install</code>.<br />
3) Install the optional libraries for the hardware you want to connect to it. Details in Configuration.<br />
<b>If you plan on using the board standalone, you don't need put any extra libraries in.</b><br /><br />
4) After these steps, eject the board and fully disconnect it from the pc. (It is important to power cycle it.)<br />
   When it's plugged back in, it should run automatically and you can connect to it via serial. (You can use putty on windows, or gnu/screen on gnu/linux)<br />
   An automated connection script exists in the form of <code>make connection</code>
<b>IMPORTANT NOTE: To make the pi appear as a usb device, run the command <code>devmode</code></b><br />

<h3>Configuration</h3>

<i>Each board has it's own different pin configuration. You can see the defaults and modify them from the board's respecive config file.</i><br /><br />

<b>Libraries needed for hardware:</b><br />
For the SSD1306 display: <code>adafruit_ssd1306 adafruit_framebuf</code><br />
For the ds1302 RTC: <code>ds1302</code> (It's included in /lib) <br />
Sdcard: <code>adafruit_sdcard adafruit_bus_device</code><br />
    The sdcard has to be formatted as Fat32 / Fat16 or equivelant.<br />
Ethernet: <code>adafruit_wiznet5k adafruit_wsgi adafruit_requests adafruit_bus_device</code><br /><br />

The neccessary libraries can be found [here](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases)<br />
Download the zip (The 7.x-mpy variant), extract it & copy the libraries you want onto <code>/lib</code> of the board.

<h3>Connection</h3>

To connect to the board it's recommended to use Putty for Windows and GNU/Screen for Linux/Mac.<br />
For Putty, select connection type to be Serial, select the port to be COM<b>X</b> where <b>X</b> is the number of the serial port allocated by the board and set the speed/baudrate to 115200. (You can find which com port is allocated from within the Device Manager, it usually is COM3 or COM4)<br /><br />

For GNU/Screen, if you are on linux, you need to be in the <code>dialout</code> user group and to connect, run: <code>screen /dev/ttyACM0 115200</code><br />If you are on a Mac instead, run: <code>ls /dev/tty.usb*</code> to find the device name, and connect to it by running: <code>screen /dev/tty.usb\<Device name here\> 115200</code><br />
Example: <code>screen /dev/tty.usbmodem12210 115200</code><br /><br />
To disconnect, press Ctrl + A, K and confirm with y.<br />
To be added to the <code>dialout</code> group, run <code>sudo usermod -a -G dialout \<your username here\></code><br /><br />

<h3>Contributors:</h3>

-> [bill88t](https://github.com/bill88t) - @bill88t#4044
<br />-> [Marios](https://github.com/mariospapaz) - @mariospapaz#2188
<br />-> [mdaadoun](https://github.com/mdaadoun) - @mdaadoun#4475

<h3>Build instructions for Linux / Macos:</h3>

In order to build & upload a kernel binary different than the one provided to the board, enable developer mode from within ljinux and then from within the "source" folder of the project, run <code>make</code>. To update all the board files (commands, kernel, etc.) run <code>make install</code><br />
The binary will be automatically uploaded to the board and be used upon the next reload/reboot of the device.<br />

<h2>A complete Ljinux manual can also be found at:</h2>
https://github.com/bill88t/ljinux/blob/main/Manual.txt<br /><br />

More stuff will be added later as the project spirals into chaos.
