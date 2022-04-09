# I HAAAATE MAKE
SHELL = bash
all: clean program.run manual sync

program.run:
	@echo -en "\nLjinux making:\n[1/4] "
	./mpy-cross-$(shell uname -m) ./ljinux_source.py -s Ljinux -v -O4 -o ../ljinux.mpy
	cp ../ljinux.mpy /media/$(shell whoami)/LJINUX/ljinux.mpy
	@echo -n "[2/4] "
	./mpy-cross-$(shell uname -m) ./jcurses.py -s jCurses -v -O4 -o ../lib/jcurses.mpy
	cp ../lib/jcurses.mpy /media/$(shell whoami)/LJINUX/lib/jcurses.mpy
	@echo -n "[3/4] "
	./mpy-cross-$(shell uname -m) ./lj_colours.py -s lJcolours -v -O4 -o ../lib/lj_colours.mpy
	cp ../lib/lj_colours.mpy /media/$(shell whoami)/LJINUX/lib/lj_colours.mpy
	@echo -n "[4/4] "
	./mpy-cross-$(shell uname -m) ./jcurses_data.py -s jCurses_data -v -O4 -o ../lib/jcurses_data.mpy
	cp ../lib/jcurses_data.mpy /media/$(shell whoami)/LJINUX/lib/jcurses_data.mpy
clean:
	@echo -en "Cleaning:\n[1/6] "
	if (test -f ../ljinux.mpy); then rm ../ljinux.mpy; fi
	@echo -n "[2/6] "
	if (test -f /media/$(shell whoami)/LJINUX/ljinux.mpy); then rm /media/$(shell whoami)/LJINUX/ljinux.mpy; fi
	@echo -n "[3/6] "
	if (test -f /media/$(shell whoami)/LJINUX/jcurses.mpy); then rm /media/$(shell whoami)/LJINUX/lib/jcurses.mpy; fi
	@echo -n "[4/6] "
	if (test -f /media/$(shell whoami)/LJINUX/lj_colours.mpy); then rm /media/$(shell whoami)/LJINUX/lib/lj_colours.mpy; fi
	@echo -n "[5/6] "
	if (test -f /media/$(shell whoami)/LJINUX/jcurses_data.mpy); then rm /media/$(shell whoami)/LJINUX/lib/jcurses_data.mpy; fi
	@echo -n "[6/6] "
	if (test -f /media/$(shell whoami)/LJINUX/LjinuxRoot/home/pi/Manual.txt); then rm /media/$(shell whoami)/LJINUX/LjinuxRoot/home/pi/Manual.txt; fi
manual:
	@echo -e "\nManual file:"
	cp ../Manual.txt /media/$(shell whoami)/LJINUX/LjinuxRoot/home/pi/Manual.txt
sync:
	@echo -e "\nSyncing changes:"
	sync
