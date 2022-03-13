# Ljinux
A "linux" written in python, for the Raspberry Pi Pico.<br />

Important note:<br />
Do not take this project seriously.<br />
This is not a real os / linux distrubution, but here we are.<br />

<h3>Anyways, since you are still reading let's start with the basics.</h3>
It runs on the rpi pico, circuitpython 7.<br />
You can optionally attach a SSD1306 display for output, a ds1302 RTC (make sure to set <code>fixrtc</code> to false from <code>config.json</code>) for persistent time or a w5500 networking breakout board for networking.<br />
For the missing hardware the functions will be automatically deactivated. (The hardware will also be deactivated in case of missing libraries.)<br />
More info in Configuration.<br />
It expects to find a <code>/LjinuxRoot</code> folder which uses as it's root. It can be on the built in fs, or an sd card, more details at Configuration.<br />

It's structure:<br />

It's shell which is named <b>based</b>, is equivelant to gnu bash.<br />Python can also be used with the pexec command.<br />
You can execute commands over serial to it, or by feeding them from a <code>Init.lja</code> file.<br />
The <code>Init.lja</code> has to be at <code>/LjinuxRoot/boot/</code> of the pico's internal storage or on the <code>/boot/</code> of the attached sd card.<br />

<h2>Installation to a fresh pi pico:</h2><br />

Install Circuitpython 7.X.X onto the pico, and unzip this entire repo (or a release), except for the "source" folder onto the CIRCUITPY drive.<br />
Then eject it and fully disconnect it from the pc. (It is important to power cycle the pi.)<br />
When it's plugged back in, it should run automatically and you can connect to it via serial. (You can use putty on windows, or gnu/screen on gnu/linux)

<h3>Configuration</h3>

<b>GPIO PINS:</b><br />
For the SSD1306 display: GP17(scl), GP16(sda) - libraries needed: <code>adafruit_ssd1306 adafruit_framebuf</code><br />
For the ds1302 RTC: GP6(clk), GP7(data), GP8(ce) - libraries needed: <code>ds1302</code><br />
Left button GP19 - Right Button GP18 - Enter Button GP20<br />
Piezo buzzer: GP15<br />
Sdcard: GP2(clk),GP3(mosi),GP4(miso), GP5(cs) - libraries needed: <code>adafruit_sdcard adafruit_bus_device</code><br />
Ethernet: GP10(clk), GP13(cs), GP11(mosi), GP12(miso) - libraries needed: <code>adafruit_wiznet5k adafruit_wsgi adafruit_requests adafruit_bus_device</code><br /><br />
The neccessary libraries can be found [here](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases)<br />
Preferably use .mpy's to reduce storage & ram usage.<br /><br />

<b>IMPORTANT NOTE: To make the pi appear as a usb device, run the command <code>devmode</code>.</b><br />

<h3>Build instructions for linux:</h3>

In order to build & upload a binary different than the one provided to the pico, enable developer mode on the pico and from within the "source" folder, run make.<br />
The binary will be automatically uploaded to the pico and be used upon the next reload/reboot of the device.<br />
In order for it to complete successfully you need to have the pico mounted to <code>/media/$(shell whoami)/LJINUX/</code>.

<h2>A complete Ljinux manual can also be found at:</h2>
[Manual.txt](https://github.com/bill88t/ljinux/blob/main/Manual.txt)

More stuff will be added later as the project spirals into chaos.<br />
