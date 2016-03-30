# -*- coding: utf-8 -*-
#   md_format_converter.Mol2TrajOutput.py
#
#   Copyright (C) 2012-2016 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Manages addition of mol2 output information to segments.
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
from .TrajOutput import TrajOutput
################################### CLASSES ###################################
class Mol2TrajOutput(TrajOutput):
    """
    Manages addition of mol2 output information to segments.
    """

    def __init__(self, manual_bonds=False, **kwargs):
        """
        Initializes.

        Arguments:
          manual_bonds (bool): Write bonds to mol2 manually
          kwargs (dict): additional keyword arguments
        """
        import os

        self.manual_bonds = manual_bonds

        super(self.__class__, self).__init__(**kwargs)

    def receive_segment(self, **kwargs):
        """
        Receives a trajectory segment and sends to each target.

        Arugments:
          kwargs (dict): Additional keyword arguments
        """
        import os

        while True:
            segment = yield
            segment_mol2 = "{0}/{1:04d}/{1:04d}{2}.mol2".format(self.outpath,
              int(segment.number), self.suffix)
            if not os.path.isfile(segment_mol2) or self.force:
                segment.outputs.append(
                  dict(
                    format    = "mol2",
                    filename  = segment_mol2,
                    selection = self.selection,
                    first     = 0,
                    last      = 0))
                if self.manual_bonds:
                    segment.outputs[-1]["format"] = "mol2_manual_bonds"

            for target in self.targets:
                target.send(segment)

    @staticmethod
    def add_subparser(level1_subparser, level2_subparsers, level3_classes):
        """
        Adds subparser for this input format to nascent parser.

        Arguments:
          level1_subparser (Subparser): Level 1 subparser to which level
            2 subparser will be added
          level2_subparsers (Subparsers): Nascent collection of level 2
            subparsers to which level 2 subparser will be added
          level3_classes (list): Classes for which level 3 subparsers
            will be added

        Returns:
          (*Subparser*, *Subparsers*): New level 2 subparser and
            associated collection of level 3 subparsers
        """
        level2_subparser = level2_subparsers.add_parser(
          name  = "mol2",
          usage = "convert.py {0} mol2".format(level1_subparser.name),
          help  = "mol2 output")
        setattr(level2_subparser, "name", "mol2")

        level3_subparsers = level2_subparser.add_subparsers(
          title = "Converter")
        for level3_class in level3_classes:
            level3_subparser = level3_class.add_subparser(level1_subparser,
              level2_subparser, level3_subparsers)

            arg_groups = {ag.title: ag 
                           for ag in level3_subparser._action_groups}
            if level3_subparser.name == "vmd":
                arg_groups["action"].add_argument("--manual-bonds",
                  action   = "store_true",
                  dest     = "manual_bonds",
                  help     = "Write bonds to mol2 manually; useful for "
                             "topologies in which atoms are not well-ordered")
            Mol2TrajOutput.add_shared_args(level3_subparser)

            level3_subparser.set_defaults(output_coroutine=Mol2TrajOutput)

        return level2_subparser, level3_subparsers
