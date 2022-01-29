# I HAAAATE MAKE
SHELL = bash
all: clean program.run

program.run: 
	./mpy-cross-$(shell uname -m) ./ljinux_source.py -s Ljinux -v -O150 -o /media/$(shell whoami)/LJINUX/ljinux.mpy
clean:
	if (test -f /media/$(shell whoami)/LJINUX/ljinux.mpy); then rm /media/$(shell whoami)/LJINUX/ljinux.mpy; fi
