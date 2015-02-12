# -*- coding: utf-8 -*-
#   md_format_converter.AntonTrajInput.py
#
#   Copyright (C) 2012-2015 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Manages generation of segments from an Anton input trajectory.
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
from .TrajInput import TrajInput
################################### CLASSES ###################################
class AntonTrajInput(TrajInput):
    """
    Manages generation of segments from an Anton input trajectory.
    """

    def __init__(self, topology, trajectory, sub_path=None, **kwargs):
        """
        Initializes.

        Arguments:
            topology (string): Path to input topology (cms)
            trajectory (string): Path to text file containing paths to
              each input segment (stk)
            sub_path (tuple): Substitution to perform on paths in
              trajectory file (Anton path, local path)
            kwargs (dict): additional keyword arguments
        """
        self.topology = topology
        self.trajectory = trajectory
        self.sub_path = sub_path
        self.infile = open(self.trajectory, "r")

        super(self.__class__, self).__init__(**kwargs)

    def next(self):
        """
        Prepares and yields next trajectory segment.

        Segment is numbered using Anton's segment number, and is
        associated with two files: the atr format trajectory, and, if
        present, the energy log. Segment is associated with two inputs,
        the cms format topology file applicable to all segments, from
        which no frames are instructed to be used, and the atr format
        trajectory, from which all frames are instructed to be used.

        Yields:
            (TrajSegment): New trajectory segment
        """
        import os
        from .TrajSegment import TrajSegment

        segment_atr = self.infile.readline().strip()
        if segment_atr == "":
            self.infile.close()
            raise StopIteration()
        else:
            if self.sub_path is not None:
                segment_atr = segment_atr.replace(*self.sub_path)
            number = segment_atr.split("/")[-2].split("-")[0]
            files = [segment_atr]
            ene = os.path.dirname(segment_atr) + "/energy/eneseq.txt"
            if os.path.isfile(ene):
                files.append(ene)

            return TrajSegment(number=number, files = files,
              inputs = [
                dict(
                  format="mae",
                  filename=self.topology,
                  first=-1,
                  last=-1),
                dict(
                  format="dtr",
                  filename=segment_atr)])

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
          name  = "anton",
          usage = "Converter.py anton {output format} {converter}",
          help  = "Anton atr input")
        setattr(level1_subparser, "name", "anton")

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
                  help     = "Input topology (cms)")
                arg_groups["input"].add_argument("-trajectory",
                  type     = str,
                  required = True,
                  help     = "Input trajectory (stk)")
                arg_groups["input"].add_argument("-sub_path",
                  type     = str,
                  nargs    = 2,
                  metavar  = ("ANTON_PATH", "LOCAL_PATH"),
                  help     = "Substitute path in input trajectory "
                             "e.g. '-sub_path /antonfs/raw /home'")
                AntonTrajInput.add_shared_args(level3_subparser)

                level3_subparser.set_defaults(input_source=AntonTrajInput)

        return level1_subparser, level2_subparsers
