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
    echo "Error: Board not found.\nMake sure it is attached and mounted before you run make"
    exit 1
fi
echo "[1/10] ljinux_source.py -> ljinux.mpy"
$mpyn ./ljinux_source.py -s Ljinux -v -o $picop/ljinux.mpy
if ! [ -d $picop/lib ]; then
    echo "Created lib directory."
    mkdir $picop/lib
fi
if [ $?==0 ];then
    echo "[2/10] jcurses.py -> lib/jcurses.mpy"
    $mpyn ./jcurses.py -s jCurses -v -o $picop/lib/jcurses.mpy
else
    echo -e "NOT OK\n"
    exit 1
fi
if [ $?==0 ];then
    echo "[3/10] lj_colours.py -> lib/lj_colours.mpy"
    $mpyn ./lj_colours.py -s lJcolours -v -o $picop/lib/lj_colours.mpy
else
    echo -e "NOT OK\n"
    exit 1
fi
if [ $?==0 ];then
    echo "[4/10] jcurses_data.py -> lib/jcurses_data.mpy"
    $mpyn ./jcurses_data.py -s jCurses_data -v -o $picop/lib/jcurses_data.mpy
else
    echo -e "NOT OK\n"
    exit 1
fi
if [ $?==0 ];then
    echo "[5/10] neopixel_colors.py -> lib/neopixel_colors.mpy"
    $mpyn ./neopixel_colors.py -s Neopixel_colors -v -o $picop/lib/neopixel_colors.mpy
else
    echo -e "NOT OK\n"
    exit 1
fi
if [ $?==0 ];then
    echo "[6/10] ds1302.py -> lib/ds1302.mpy"
    $mpyn ./ds1302.py -s DS1302 -v -o $picop/lib/ds1302.mpy
else
    echo -e "NOT OK\n"
    exit 1
fi
if [ $?==0 ];then
    echo "[7/10] code.py"
    \cp ./rootfilesystem/code.py $picop/code.py
else
    echo -e "NOT OK\n"
    exit 1
fi
if [ $?==0 ];then
    echo "[8/10] boot.py"
    \cp ./rootfilesystem/boot.py $picop/boot.py
else
    echo -e "NOT OK\n"
    exit 1
fi
if [ $?==0 ];then
    echo "[9/10] config-raspberry_pi_pico.json"
    \cp ./rootfilesystem/config-raspberry_pi_pico.json $picop/config-raspberry_pi_pico.json
else
    echo -e "NOT OK\n"
    exit 1
fi
if [ $?==0 ];then
    echo "[10/10] config-waveshare_rp2040_zero.json"
    \cp ./rootfilesystem/config-waveshare_rp2040_zero.json $picop/config-waveshare_rp2040_zero.json
else
    echo -e "NOT OK\n"
    exit 1
fi
exit 0
