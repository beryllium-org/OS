# I HAAAATE MAKE
SHELL = bash
all: clean presync program.run sync
install: clean presync program.run rootfs manual sync
debug: clean presync program.run.debug rootfs manual sync

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
program.run.debug:
	@echo -en "\nLjinux debug making:\n[1/4] "
	./mpy-cross-$(shell uname -m) ./ljinux_source.py -s Ljinux -v -o ../ljinux.mpy
	cp ../ljinux.mpy /media/$(shell whoami)/LJINUX/ljinux.mpy
	@echo -n "[2/4] "
	./mpy-cross-$(shell uname -m) ./jcurses.py -s jCurses -v -o ../lib/jcurses.mpy
	cp ../lib/jcurses.mpy /media/$(shell whoami)/LJINUX/lib/jcurses.mpy
	@echo -n "[3/4] "
	./mpy-cross-$(shell uname -m) ./lj_colours.py -s lJcolours -v -o ../lib/lj_colours.mpy
	cp ../lib/lj_colours.mpy /media/$(shell whoami)/LJINUX/lib/lj_colours.mpy
	@echo -n "[4/4] "
	./mpy-cross-$(shell uname -m) ./jcurses_data.py -s jCurses_data -v -o ../lib/jcurses_data.mpy
	cp ../lib/jcurses_data.mpy /media/$(shell whoami)/LJINUX/lib/jcurses_data.mpy
clean:
	@echo -en "Cleaning:\n[1/6] "
	[ -f ../ljinux.mpy ] && rm ../ljinux.mpy || true
	@echo -n "[2/6] "
	[ -f /media/$(shell whoami)/LJINUX/ljinux.mpy ] && rm /media/$(shell whoami)/LJINUX/ljinux.mpy || true
	@echo -n "[3/6] "
	[ -f /media/$(shell whoami)/LJINUX/jcurses.mpy ] && rm /media/$(shell whoami)/LJINUX/lib/jcurses.mpy || true
	@echo -n "[4/6] "
	[ -f /media/$(shell whoami)/LJINUX/lj_colours.mpy ] && rm /media/$(shell whoami)/LJINUX/lib/lj_colours.mpy || true
	@echo -n "[5/6] "
	[ -f /media/$(shell whoami)/LJINUX/jcurses_data.mpy ] && rm /media/$(shell whoami)/LJINUX/lib/jcurses_data.mpy || true
	@echo -n "[6/6] "
	[ -f /media/$(shell whoami)/LJINUX/LjinuxRoot/home/pi/Manual.txt ] && rm /media/$(shell whoami)/LJINUX/LjinuxRoot/home/pi/Manual.txt || true
manual:
	@echo -e "\nManual file:"
	cp ../Manual.txt /media/$(shell whoami)/LJINUX/LjinuxRoot/home/pi/Manual.txt
sync:
	@echo -e "\nSyncing changes:"
	sync
presync:
	@echo -e "\nSyncing source:"
	sync
rootfs:
	@echo -e "\nUpdating the pico's rootfs:"
	[ -d /media/$(shell whoami)/LJINUX ] && cp -rv ../LjinuxRoot/ /media/$(shell whoami)/LJINUX/ || true
	[ -d /media/$(shell whoami)/CIRCUITPY ] && cp -rv ../LjinuxRoot/ /media/$(shell whoami)/CIRCUITPY/ || true
