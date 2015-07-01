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

    parser            = argparse.ArgumentParser(
      usage           = "convert.py {input format} {output format} "
                        "{converter}",
      description     = __doc__,
      formatter_class = argparse.RawTextHelpFormatter)
    level1_subparsers = parser.add_subparsers(
      title           = "Input trajectory format")

    from .AntonTrajInput import AntonTrajInput
    from .StandardTrajInput import StandardTrajInput
    level1_classes = [AntonTrajInput, StandardTrajInput]

    from .AmberTrajOutput import AmberTrajOutput
    from .GromacsTrajOutput import GromacsTrajOutput
    from .Mol2TrajOutput import Mol2TrajOutput
    from .PdbTrajOutput import PdbTrajOutput
    level2_classes = [AmberTrajOutput, GromacsTrajOutput,
                      Mol2TrajOutput,  PdbTrajOutput]

    from .VmdConverter import VmdConverter
    level3_classes = [VmdConverter]

    level1_subparser = level1_subparsers.add_parser(
      name  = "yaml",
      usage = "convert.py yaml YAML_FILE",
      help  = "Read input, output, and converter configuration from YAML file")
    level1_subparser.add_argument("yaml_filename")
    level1_subparser.set_defaults(input_source="yaml")

    for level1_class in level1_classes:
        level1_class.add_subparser(level1_subparsers, level2_classes,
          level3_classes)

    kwargs = vars(parser.parse_args())

    input_source = kwargs.pop("input_source")
    if input_source == "yaml":
        from . import get_yaml

        yaml_dict = get_yaml(kwargs.pop("yaml_filename"))

        input_source_kwargs = yaml_dict.pop("input")
        input_source = {
          "anton":    AntonTrajInput,
          "standard": StandardTrajInput}.get(
          input_source_kwargs.pop("format"))(**input_source_kwargs)

        converter_sink_kwargs = yaml_dict.pop("converter")
        converter_sink = {
          "vmd": VmdConverter}.get(
          converter_sink_kwargs.pop("format"))(**converter_sink_kwargs)
        next_target = converter_sink

        output_coroutine_list = yaml_dict.pop("output")
        for output_coroutine_kwargs in output_coroutine_list:
            output_coroutine = {
              "amber":   AmberTrajOutput,
              "gromacs": GromacsTrajOutput,
              "mol2":    Mol2TrajOutput,
              "pdb":     PdbTrajOutput}.get(
              output_coroutine_kwargs.pop("format"))(**output_coroutine_kwargs)
            output_coroutine.add_target(next_target)
            next_target = output_coroutine
        for segment in input_source:
            next_target.send(segment)

    else:
        input_source = input_source(**kwargs)
        output_coroutine = kwargs.pop("output_coroutine")(**kwargs)
        converter_sink = kwargs.pop("converter_sink")(**kwargs)
        output_coroutine.add_target(converter_sink)

        for segment in input_source:
            output_coroutine.send(segment)
