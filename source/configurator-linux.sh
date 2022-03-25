#!/bin/bash
declare verrr="0.3.0 dev"
echo -e "Ljinux" $verrr "configuration & management tool.\n\nSelect the option you need.\n\nFull-Install replaces all present pico system files with the updated ones.\nCore-Install, copies over only the basic files needed, for a ljinux installation.\nConnect, opens a GNU/Screen connection to the pico\n\n"
PS3="-> "

select opt in Full-Install Core-Install Connect; do
    if [ $REPLY == 1 ]; then
        echo "Full (Re)Install of lJinux" $verrr
        while true; do
            read -p "Are you sure you want to reinstall Ljinux? -> " yn
            case $yn in
                [Yy]* ) ls;
                        pwd;
                        break;;
                [Nn]* ) exit;;
                * ) echo "Please answer yes or no.";;
            esac
        done

    elif [ $REPLY == 2 ]; then
        echo "Core (Re)Install of lJinux" $verrr
    elif [ $REPLY == 3 ]; then
        echo "Opening GNU/Screen connection.."
        if ! command -v screen &> /dev/null
            then
                echo -e "GNU/Screen could not be found\n\n$ sudo apt install screen"
                sudo apt install screen
                exit
        fi
        screen /dev/ttyACM0 115200
    fi
    break
done
sync
exit 0
