all: clean program.run

program.run: 
	./mpy-cross-$$(uname -m) ./ljinux_source.py -s Ljinux -v -O150 -o /media/$$USER/LJINUX/ljinux.mpy
clean:
	if (test -f /media/$$USER/LJINUX/ljinux.mpy); then rm /media/$$USER/LJINUX/ljinux.mpy; fi 
