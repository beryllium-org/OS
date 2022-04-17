declare mpyn="./mpy-crosses/mpy-cross-$(uname -m)"
echo "[1/4] ljinux.mpy"
$mpyn ./ljinux_source.py -s Ljinux -v -O4 -o /dev/null
echo -e "OK\n[2/4] jcurses.mpy"
$mpyn ./jcurses.py -s jCurses -v -O4 -o /dev/null
echo -e "OK\n[3/4] lj_colours.mpy"
$mpyn ./lj_colours.py -s lJcolours -v -O4 -o /dev/null
echo -e "OK\n[4/4] jcurses_data.mpy"
$mpyn ./jcurses_data.py -s jCurses_data -v -O4 -o /dev/null
echo -e "OK\nCompile Test successful."
exit 0
