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
\cp -rv ./LjinuxRoot/ $picop/
\cp -v ./Manual.txt $picop/LjinuxRoot/home/pi/Manual.txt
exit 0
