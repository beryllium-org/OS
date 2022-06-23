if $(command -v apt >/dev/null); then
    echo -e "Detected apt\nsudo apt install -y screen"
    sudo apt install -y screen
elif $(command -v yum >/dev/null); then
    echo -e "Detected yum\nsudo yum install screen"
    sudo yum install screen
elif $(command -v dnf >/dev/null); then
    echo -e "Detected dnf\nsudo dnf install -y screen"
    sudo dnf install -y screen

elif $(command -v pamac >/dev/null); then
    echo -e "Detected Pamac\nsudo pamac install screen"
    sudo pamac install screen

elif $(command -v yay >/dev/null); then
    echo -e "Detected yay\n yay -S screen"
    yay -S screen

elif $(command -v pacman >/dev/null); then
    echo -e "Detected Pacman\nsudo pacman -S screen"
    sudo pacman -S screen

else
    echo "No suitable package manager found"
    exit 1
fi

exit 0
