#!/usr/bin/python
# -*- coding: utf-8 -*-
#   md_format_converter.convert.py
#
#   Copyright (C) 2012-2015 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Converts Molecular Dynamics (MD) simulation trajectories that are split
into multiple segments between different formats.
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
if __name__ == "__main__":
    __package__ = str("md_format_converter")
    import md_format_converter
#################################### MAIN #####################################
if __name__ == "__main__":
    import argparse

    parser             = argparse.ArgumentParser(
      usage            = "convert.py {input format} {output format} "
                         "{converter}",
      description      = __doc__,
      formatter_class  = argparse.RawTextHelpFormatter)
    level1_subparsers = parser.add_subparsers(
      title            = "Input trajectory format")

    from .AntonTrajInput import AntonTrajInput
    level1_classes  = [AntonTrajInput]
    from .AmberTrajOutput import AmberTrajOutput
    from .PdbTrajOutput import PdbTrajOutput
    level2_classes = [AmberTrajOutput, PdbTrajOutput]
    from .VmdConverter import VmdConverter
    level3_classes = [VmdConverter]

    for level1_class in level1_classes:
        level1_class.add_subparser(level1_subparsers, level2_classes,
          level3_classes)

    kwargs = vars(parser.parse_args())

    input_source = kwargs.pop("input_source")(**kwargs)
    output_coroutine = kwargs.pop("output_coroutine")(**kwargs)
    converter_sink = kwargs.pop("converter_sink")(**kwargs)
    output_coroutine.add_target(converter_sink)

    for segment in input_source:
        output_coroutine.send(segment)
