if [ -d /media/$(whoami)/LJINUX ]; then
    declare picop="/media/$(whoami)/LJINUX"
elif [ -d /media/$(whoami)/CIRCUITPY ]; then
    declare picop="/media/$(whoami)/CIRCUITPY"
elif [ -d /Volumes/LJINUX ]; then
    declare picop="/Volumes/LJINUX"
elif [ -d /Volumes/CIRCUITPY ]; then
    declare picop="/Volumes/CIRCUITPY"
else
    echo "Error: Pico not found, make sure it is connected and mounted."
    exit 1
fi
echo "[1/4] Deleting old ljinux.mpy"
if [ -f $picop/ljinux.mpy ]; then rm $picop/ljinux.mpy; fi
echo "[2/4] Deleting old jcurses.mpy"
if [ -f $picop/lib/jcurses.mpy ]; then rm $picop/lib/jcurses.mpy; fi
echo "[3/4] Deleting old lj_colours.mpy"
if [ -f $picop/lib/lj_colours.mpy ]; then rm $picop/lib/lj_colours.mpy; fi
echo "[4/4] Deleting old jcurses_data.py"
if [ -f $picop/lib/jcurses_data.mpy ]; then rm $picop/lib/jcurses_data.mpy; fi
exit 0
