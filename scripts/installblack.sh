if $(command -v pip >/dev/null); then
    echo -e "Detected pip\npip install black"
    pip install black
elif $(command -v pip3 >/dev/null); then
    echo -e "Detected pip3\npip3 install black"
    pip3 install black
else
    echo -e "Could not detect pip.\nblack installation failed"
    exit 1
fi
exit 0
