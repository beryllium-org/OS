declare mpyn="./mpy-crosses/mpy-cross-$(uname -m)"
echo "[1/6] ljinux.mpy"
$mpyn ./ljinux_source.py -s Ljinux -v -O4 -o /dev/null
if [ $?==0 ];then
    echo -e "OK\n[2/6] jcurses.mpy"
    $mpyn ./jcurses.py -s jCurses -v -O4 -o /dev/null
else
    echo -e "NOT OK\n"
    exit 1
fi
if [ $?==0 ];then
    echo -e "OK\n[3/6] lj_colours.mpy"
    $mpyn ./lj_colours.py -s lJcolours -v -O4 -o /dev/null
else
    echo -e "NOT OK\n"
    exit 1
fi
if [ $?==0 ];then
    echo -e "OK\n[4/6] jcurses_data.mpy"
    $mpyn ./jcurses_data.py -s jCurses_data -v -O4 -o /dev/null
else
    echo -e "NOT OK\n"
    exit 1
fi
if [ $?==0 ];then
    echo -e "OK\n[5/6] neopixel_colors.py -> lib/neopixel_colors.mpy"
    $mpyn ./neopixel_colors.py -s Neopixel_colors -v -O4 -o /dev/null
else
    echo -e "NOT OK\n"
    exit 1
fi
if [ $?==0 ];then
    echo -e "OK\n[6/6] ds1302.py -> lib/ds1302.mpy"
    $mpyn ./ds1302.py -s DS1302 -v -O4 -o $picop/lib/ds1302.mpy
else
    echo -e "NOT OK\n"
    exit 1
fi
echo -e "OK\nCompile Test successful.\n"
exit 0
