# ljinux [![](https://tokei.rs/b1/github/bill88t/ljinux)](https://github.com/bill88t/ljinux)
A "linux" written in python, for the Raspberry Pi Pico.<br />

Important note:<br />

Do not take this project seriously.<br />
I know it's not a linux, or an os, or anything in that regard, but here we are.<br />

<h3>Anyways, since you are still reading let's start with the basics.</h3>
It runs on the rpi pico, circuitpython.<br />
As for the display I use a SSD1306 over I2C, it's optional tho.<br />
If the display is not available, all graphics functions will be disabled.<br />
You can attach an rtc, I used a ds1302.<br />
If you don't attach one, expect borked timestamps, nothing else.
The timings will work correctly though.<br />
Networking can be achieved by attaching a w5500 breakout board.<br />
It expects to find a /ljinux folder which uses as it's root. It can be on the built in fs, or an sd card, more details at Configuration.<br />

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

<b>GPIO PINS:</b><br />For display GP17(scl), GP16(sda)<br />For rtc GP6(clk), GP7(data), GP8(ce)<br />button left GP19 - button right GP18 - button enter GP20<br />For buzzer GP15<br />For sdcard GP2(clk),GP3(mosi),GP4(miso)<br />For ethernet GP10(clk), GP13(cs), GP11(mosi), GP12(miso),<br />

<b>IMPORTANT NOTE: To make the pi appear as a usb device, run the command "devmode".</b><br />

Built-in commands moved to Wiki<br />

More stuff will be added later as the project spirals into chaos.<br />

<h3>Build instructions for linux:</h3>

In order to build & upload a binary different than the one provided to the pico, enable developer mode on the pico and from within the "source" folder, run make.<br />
The binary will be automatically uploaded to the pico and be used upon the next reload/reboot of the device.
