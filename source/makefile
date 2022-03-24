# I HAAAATE MAKE
SHELL = bash
all: clean program.run

program.run: 
	./mpy-cross-$(shell uname -m) ./ljinux_source.py -s Ljinux -v -O150 -o ../ljinux.mpy
	cp ../ljinux.mpy /media/$(shell whoami)/LJINUX/ljinux.mpy
	./mpy-cross-$(shell uname -m) ./jcurses.py -s Jcurses -v -O150 -o ../lib/jcurses.mpy
	cp ../lib/jcurses.mpy /media/$(shell whoami)/LJINUX/lib/jcurses.mpy
	./mpy-cross-$(shell uname -m) ./lj_colours.py -s Jcurses -v -O150 -o ../lib/lj_colours.mpy
	cp ../lib/lj_colours.mpy /media/$(shell whoami)/LJINUX/lib/lj_colours.mpy
	sync
clean:
	if (test -f ../ljinux.mpy); then rm ../ljinux.mpy; fi
	if (test -f /media/$(shell whoami)/LJINUX/ljinux.mpy); then rm /media/$(shell whoami)/LJINUX/ljinux.mpy; fi
	if (test -f /media/$(shell whoami)/LJINUX/jcurses.mpy); then rm /media/$(shell whoami)/LJINUX/lib/jcurses.mpy; fi
	if (test -f /media/$(shell whoami)/LJINUX/lj_colours.mpy); then rm /media/$(shell whoami)/LJINUX/lib/lj_colours.mpy; fi
