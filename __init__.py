# -*- coding: utf-8 -*-
#   md_format_converter.__init__.py
#
#   Copyright (C) 2012-2015 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
.. todo:
    - TrajOutput
    - Pass debug and verbose to VMD
"""
################################### MODULES ###################################
from os.path import dirname
################################## VARIABLES ##################################
MODULE_PATH = dirname(__file__)
################################## FUNCTIONS ##################################
def run_command(command, leader="", verbose=False, **kwargs):
    """
    """
    from subprocess import Popen, PIPE, STDOUT

    if verbose:
        print leader + command
    pipe = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT, **kwargs)
    for line in iter(pipe.stdout.readline, ""):
        out_line = leader + line.rstrip().replace("\n", " ")
        if verbose:
            print(out_line)
