# -*- coding: utf-8 -*-
#   md_format_converter.StandardTrajInput.py
#
#   Copyright (C) 2012-2015 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Manages generation of segments from an input trajectory.
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
from .TrajInput import TrajInput
################################### CLASSES ###################################
class StandardTrajInput(TrajInput):
    """
    Manages generation of segments from an input trajectory.
    """

    def __init__(self, topology, trajectory, **kwargs):
        """
        Initializes.

        Arugments:
          topology (string): Path to input topology
          trajectory (string): Path to root folder containing simulaion
            segments
          kwargs (dict): Additional keyword arguments
        """
        import os

        self.topology = os.path.expandvars(topology)
        self.trajectory = os.path.expandvars(trajectory)
        self.segments = sorted(os.listdir(self.trajectory))

        super(self.__class__, self).__init__(**kwargs)

    def next(self):
        """
        Prepares and yields next trajectory segment.

        Yields:
            (TrajSegment): New trajectory segment
        """
        import os
        from .TrajSegment import TrajSegment

        if len(self.segments) == 0:
            raise StopIteration()
        else:
            number = self.segments.pop(0)
            files = os.listdir("{0}/{1}".format(self.trajectory, number))
            segment = TrajSegment(number=number, files = files)
            segment.inputs = [
                dict(
                  format="pdb",
                  filename=self.topology,
                  first=-1,
                  last=-1),
                dict(
                  format="xtc",
                  filename="{0}/{1}/{2}".format(self.trajectory, number,
                    segment["xtc"]))]
            return segment

    @staticmethod
    def add_subparser(level1_subparsers, level2_classes, level3_classes):
        """
        Adds subparser for this input format to nascent parser.

        Arguments:
          level1_subparsers (Subparsers): Nascent collection of level 1
            subparsers to which level 1 subparser will be added
          level2_classes (list): Classes for which level 2 subparsers
            will be added
          level3_classes (list): Classes for which level 3 subparsers
            will be added

        Returns:
          (*Subparser*, *Subparsers*): New level 1 subparser and
            associated collection of level 2 subparsers
        """
        level1_subparser = level1_subparsers.add_parser(
          name  = "standard",
          usage = "convert.py standard {output format} {converter}",
          help  = "Standard trajectory input")
        setattr(level1_subparser, "name", "standard")

        level2_subparsers = level1_subparser.add_subparsers(
          title = "Output trajectory format")
        for level2_class in level2_classes:
            level_2_subparser, level3_subparsers = level2_class.add_subparser(
              level1_subparser, level2_subparsers, level3_classes)

            for level3_subparser in level3_subparsers.choices.values():
                arg_groups = {ag.title: ag 
                               for ag in level3_subparser._action_groups}
                arg_groups["input"].add_argument("-topology",
                  type     = str,
                  required = True,
                  help     = "Input topology")
                arg_groups["input"].add_argument("-trajectory",
                  type     = str,
                  required = True,
                  help     = "Path to root folder containing simulation "
                             "segments")
                StandardTrajInput.add_shared_args(level3_subparser)

                level3_subparser.set_defaults(input_source=StandardTrajInput)

        return level1_subparser, level2_subparsers
