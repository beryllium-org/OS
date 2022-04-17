if [ -c /dev/ttyACM0 ]; then
    declare picc="/dev/ttyACM0"
else
    declare picc=$(ls /dev/tty.usb*)
    if ! [ -c picc ]; then
        echo "Could find the board."
        exit 1
    fi
fi
screen $picc 115200
exit 0
