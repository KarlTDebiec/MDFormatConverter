# -*- coding: utf-8 -*-
#   md_format_converter.PdbTrajOutput.py
#
#   Copyright (C) 2012-2015 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Manages addition of PDB output information to segments.
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
from .TrajOutput import TrajOutput
################################### CLASSES ###################################
class PdbTrajOutput(TrajOutput):
    """
    Manages addition of PDB output information to segments.
    """

    def __init__(self, outpath=None, selection=None, suffix=None, force=False,
        **kwargs):
        """
        Initializes.

        Arugments:
          outpath (str): Outfile path
          selection (str): Atom selection string
          suffix (str): Suffix to add to outfiles between name and
            extension
          force(bool): Overwrite output if already present
          targets (list): Targets to which this coroutine will send
            segments after processing
          kwargs (dict): Additional keyword arguments
        """
        import os

        self.outpath = os.path.expandvars(outpath)
        if suffix is None:
            self.suffix = suffix
        elif suffix.startswith("_"):
            self.suffix = suffix
        else:
            self.suffix = "_" + suffix
        self.selection = selection
        self.force = force

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
            segment_pdb = "{0}/{1:04d}/{1:04d}{2}.pdb".format(self.outpath,
              int(segment.number), self.suffix)
            if not os.path.isfile(segment_pdb) or self.force:
                segment.outputs.append(
                  dict(
                    format="pdb",
                    filename=segment_pdb,
                    selection=self.selection,
                    first=0,
                    last=0))

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
          name  = "pdb",
          usage = "convert.py {0} pdb".format(level1_subparser.name),
          help  = "PDB output")
        setattr(level2_subparser, "name", "pdb")

        level3_subparsers = level2_subparser.add_subparsers(
          title = "Converter")
        for level3_class in level3_classes:
            level3_subparser = level3_class.add_subparser(level1_subparser,
              level2_subparser, level3_subparsers)

            arg_groups = {ag.title: ag 
                           for ag in level3_subparser._action_groups}
            PdbTrajOutput.add_shared_args(level3_subparser)

            level3_subparser.set_defaults(output_coroutine=PdbTrajOutput)

        return level2_subparser, level3_subparsers
