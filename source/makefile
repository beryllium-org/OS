all: clean program.run

program.run: 
	/home/pi/Desktop/mpy-cross /media/pi/LJINUX/source/ljinux_source.py -s Ljinux -v -O150 -o /media/pi/LJINUX/ljinux.mpy
clean:
	if (test -f /media/pi/LJINUX/ljinux.mpy); then rm /media/pi/LJINUX/ljinux.mpy; fi 
