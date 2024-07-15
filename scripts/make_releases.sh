#!/bin/bash

mkdir release
for directory in "../Boardfiles"/*; do
    board="${directory##*/}"
    make clean
    make BOARD=$board install
    zip -r "release/${board}.zip" "./build_${board}/"
done
make clean
