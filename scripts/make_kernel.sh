declare mpyn="./mpy-crosses/mpy-cross-$(uname -m)"
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
echo "[1/8] ljinux_source.py -> ljinux.mpy"
$mpyn ./ljinux_source.py -s Ljinux -v -O4 -o $picop/ljinux.mpy
if ! [ -d $picop/lib ]; then
    echo "Created lib directory."
    mkdir $picop/lib
fi
echo "[2/8] jcurses.py -> lib/jcurses.mpy"
$mpyn ./jcurses.py -s jCurses -v -O4 -o $picop/lib/jcurses.mpy
echo "[3/8] lj_colours.py -> lib/lj_colours.mpy"
$mpyn ./lj_colours.py -s lJcolours -v -O4 -o $picop/lib/lj_colours.mpy
echo "[4/8] jcurses_data.py -> lib/jcurses_data.mpy"
$mpyn ./jcurses_data.py -s jCurses_data -v -O4 -o $picop/lib/jcurses_data.mpy
echo "[5/9] neopixel_colors.py -> lib/neopixel_colors.mpy"
$mpyn ./neopixel_colors.py -s Neopixel_colors -v -O4 -o $picop/lib/neopixel_colors.mpy
echo "[6/9] code.py"
cp ./rootfilesystem/code.py $picop/code.py
echo "[7/9] boot.py"
cp ./rootfilesystem/boot.py $picop/boot.py
echo "[8/9] config-raspberry_pi_pico.json"
cp ./rootfilesystem/config-raspberry_pi_pico.json $picop/config-raspberry_pi_pico.json
echo "[9/9] config-waveshare_rp2040_zero.json"
cp ./rootfilesystem/config-waveshare_rp2040_zero.json $picop/config-waveshare_rp2040_zero.json
exit 0
