#!/bin/bash
if [ "$(uname)" == "Darwin" ]; then
    echo "We are on macos, skipping linux group checks"
    exit 0
fi

if id -nG "$USER" | grep -qw "dialout"; then
    echo "$USER belongs to dialout"
    exit 0
else
    echo -e "$USER does not belong to dialout\nRunning \"sudo usermod -a -G dialout $USER\""
    sudo usermod -a -G dialout $USER
    echo -e "For the user group changes to take effect, please logout or reboot"
    exit 1
fi
