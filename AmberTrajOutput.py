# -*- coding: utf-8 -*-
#   md_format_converter.AmberTrajOutput.py
#
#   Copyright (C) 2012-2016 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Manages addition of Amber output information to segments.
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
from .TrajOutput import TrajOutput
################################### CLASSES ###################################
class AmberTrajOutput(TrajOutput):
    """
    Manages addition of Amber output information to segments.
    """

    def receive_segment(self, **kwargs):
        """
        Receives a trajectory segment and sends to each target.

        Arugments:
          kwargs (dict): Additional keyword arguments
        """
        import os

        while True:
            segment = yield
            segment_crd = "{0}/{1:04d}/{1:04d}{2}.crd".format(self.outpath,
              int(segment.number), self.suffix)
            if not os.path.isfile(segment_crd) or self.force:
                segment.outputs.append(
                  dict(
                    filename  = segment_crd,
                    format    = "crdbox",
                    selection = self.selection))
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
          name  = "amber",
          usage = "convert.py {0} amber".format(level1_subparser.name),
          help  = "Amber crd text output")
        setattr(level2_subparser, "name", "amber")

        level3_subparsers = level2_subparser.add_subparsers(
          title = "Converter")
        for level3_class in level3_classes:
            level3_subparser = level3_class.add_subparser(level1_subparser,
              level2_subparser, level3_subparsers)

            arg_groups = {ag.title: ag
                           for ag in level3_subparser._action_groups}
            AmberTrajOutput.add_shared_args(level3_subparser)

            level3_subparser.set_defaults(output_coroutine=AmberTrajOutput)

        return level2_subparser, level3_subparsers
