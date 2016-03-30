#!/bin/env bash
#   md_format_converter/util/remove_null_character.sh
#
#   Copyright (C) 2012-2016 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
#
#   VMD ocassionaly writes PDB files containing a null character, which it
#   cannot subsequently read. This script removes this null character from
#   every pdb in every subfolder of the folder from which it is run

set -x

for folder in $(ls); do
    cd $folder
    for pdb in $(ls *.pdb); do
        perl -pe "s/\000//g" $pdb > temp.pdb
        mv   temp.pdb $pdb
    done
    cd ..
done
