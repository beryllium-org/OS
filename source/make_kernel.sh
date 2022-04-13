declare mpyn="./mpy-cross-$(uname -m)"
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
echo "[1/4] ljinux_source.py -> ljinux.mpy"
$mpyn ./ljinux_source.py -s Ljinux -v -O4 -o ../ljinux.mpy
cp ../ljinux.mpy $picop/ljinux.mpy
if ! [ -d $picop/lib ]; then
    echo "Created lib directory."
    mkdir $picop/lib
fi
echo "[2/4] jcurses.py -> lib/jcurses.mpy"
$mpyn ./jcurses.py -s jCurses -v -O4 -o ../lib/jcurses.mpy
cp ../lib/jcurses.mpy $picop/lib/jcurses.mpy
echo "[3/4] lj_colours.py -> lib/lj_colours.mpy"
$mpyn ./lj_colours.py -s lJcolours -v -O4 -o ../lib/lj_colours.mpy
cp ../lib/lj_colours.mpy $picop/lib/lj_colours.mpy
echo "[4/4] jcurses_data.py -> lib/jcurses_data.mpy"
$mpyn ./jcurses_data.py -s jCurses_data -v -O4 -o ../lib/jcurses_data.mpy
cp ../lib/jcurses_data.mpy $picop/lib/jcurses_data.mpy
exit 0
