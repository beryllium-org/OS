if [ -d /media/$(whoami)/LJINUX ]; then
    declare picop="/media/$(whoami)/LJINUX"
elif [ -d /media/$(whoami)/CIRCUITPY ]; then
    declare picop="/media/$(whoami)/CIRCUITPY"
elif [ -d /Volumes/LJINUX ]; then
    declare picop="/Volumes/LJINUX"
elif [ -d /Volumes/CIRCUITPY ]; then
    declare picop="/Volumes/CIRCUITPY"
else
    exit 1
fi
echo "[1/4] old ljinux.mpy"
rm $picop/ljinux.mpy
rm ../ljinux.mpy
echo "[2/4] lib/jcurses.mpy"
rm $picop/lib/jcurses.mpy
rm ../lib/jcurses.mpy
echo "[3/4] lib/lj_colours.mpy"
rm $picop/lib/lj_colours.mpy
rm ../lib/lj_colours.mpy
echo "[4/4] jcurses_data.py -> lib/jcurses_data.mpy"
rm $picop/lib/jcurses_data.mpy
rm ../lib/jcurses_data.mpy
exit 0
