#!/bin/bash

mkdir release
for directory in "../Boardfiles"/*; do
    board="${directory##*/}"
    make clean
    make BOARD=$board install
    (cd "./build_${board}" && zip -r "../release/${board}.zip" .)
done
make clean
