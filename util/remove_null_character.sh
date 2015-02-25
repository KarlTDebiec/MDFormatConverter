#!/bin/bash

set -x

for folder in $(ls); do
    cd $folder
    for pdb in $(ls *.pdb); do
        perl -pe "s/\000//g" $pdb > temp.pdb
        mv   temp.pdb $pdb
    done
    cd ..
done
