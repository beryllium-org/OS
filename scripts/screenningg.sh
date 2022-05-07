if [ -c /dev/ttyACM0 ]; then
    declare picc="/dev/ttyACM0"
else
    declare picc=$(ls /dev/tty.usb*)
    if ! [ -c $picc ]; then
        echo "Could find the board."
        exit 1
    fi
fi
screen $picc 115200
if [[ $0 =~ .*"screenningg.sh" ]]; then
    echo -e "\nTo permenantly have this script available in your path,\nConsider running \"make ccon\" to install it in your path"
fi
exit 0
