# -*- coding: utf-8 -*-
#   md_format_converter.VmdConverter.py
#
#   Copyright (C) 2012-2016 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Manages conversion of segments between output formats using VMD.
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
from .Converter import Converter
################################### CLASSES ###################################
class VmdConverter(Converter):
    """
    Manages conversion of segments between formats using VMD.
    """

    def __init__(self, **kwargs):
        """
        Initializes and checks if vmd excutable is available.

        Arugments:
          kwargs (dict): Additional keyword arguments
        """
        from commands import getstatusoutput
        if getstatusoutput("hash vmd")[0] != 0:
            raise OSError("'vmd' command is not available; check $PATH and "
                          "modules")
        super(self.__class__, self).__init__(**kwargs)

    def receive_segment(self, **kwargs):
        """
        Receives a trajectory segment.

        Arugments:
          kwargs (dict): Additional keyword arguments
        """
        from . import MODULE_PATH, run_command
        vmd_script = "{0}/convert.tcl".format(MODULE_PATH)

        while True:
            segment = yield
            print(segment)
            command = "vmd -dispdev text -e {0} -args ".format(vmd_script)

            for input in segment.inputs:
                command += " -input "
                for key, value in input.items():
                    command += "{0}\={1}:".format(key, value)
                command = command[:-1]

            for output in segment.outputs:
                command +=  " -output "
                for key, value in output.items():
                    if key == "selection":
                        if value is not None:
                            command += "{0}\={1}:".format(key,
                                         value.replace(" ", "_"))
                    else:
                        command += "{0}\={1}:".format(key, value)
                command = command[:-1]

            if len(segment.outputs) == 0:
                continue
            run_command(command, verbose=True)

    @staticmethod
    def add_subparser(level1_subparser, level2_subparser, level3_subparsers):
        """
        Adds subparser for this converter to nascent parser.

        Arguments:
          level1_subparser (Subparser): Level 1 subparser to which level
            2 subparser will be added
          level2_subparser (Subparser): Level 2 subparser to which level
            3 subparser will be added
          level3_subparsers (Subparsers): Nascent collection of level 3
            subparsers to which level 3 subparser will be added

        Returns:
          (*Subparser*): New level 3 subparser
        """
        level3_subparser = level3_subparsers.add_parser(
          name  = "vmd",
          usage = "convert.py {0} {1} vmd".format(level1_subparser.name,
            level2_subparser.name),
          help  = "Conversion using Visual Molecular Dynamics")
        setattr(level3_subparser, "name", "vmd")

        level3_subparser.add_argument_group("input")
        level3_subparser.add_argument_group("action")
        level3_subparser.add_argument_group("output")

        arg_groups = {ag.title: ag 
                       for ag in level3_subparser._action_groups}
        arg_groups["action"].add_argument("-selection",
          type = str,
          help = "Atom selection to output, uses VMD syntax "
                 "e.g. -selection 'not resname T4PE'")
        VmdConverter.add_shared_args(level3_subparser)

        level3_subparser.set_defaults(converter_sink=VmdConverter)

        return level3_subparser
