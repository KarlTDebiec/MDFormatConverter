# -*- coding: utf-8 -*-
#   md_format_converter.TrajOutput.py
#
#   Copyright (C) 2012-2015 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Manages addition of output information to segments.
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
################################### CLASSES ###################################
class TrajOutput(object):
    """
    Manages addition of output information to segments.
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

        self.targets = kwargs.get("targets", [])

        self.func = self.receive_segment()
        self.next()

    def next(self, **kwargs):
        """
        Moves wrapped function to first yield statement.

        Arugments:
          kwargs (dict): Additional keyword arguments
        """
        self.func.next()

    def send(self, *args, **kwargs):
        """
        Transfers arguments to wrapped function.

        Arugments:
          args (tuple): Additional arguments
          kwargs (dict): Additional keyword arguments
        """
        self.func.send(*args, **kwargs)

    def close(self, *args, **kwargs):
        """
        Terminates wrapped function.

        Arugments:
          args (tuple): Additional arguments
          kwargs (dict): Additional keyword arguments
        """
        self.func.close(*args, **kwargs)

    def add_target(self, target, **kwargs):
        """
        Adds a target to this coroutine

        Arugments:
          target (object): Target to which this coroutine will send
            segments after processing
        """
        self.targets.append(target)

    def receive_segment(self, **kwargs):
        """
        Receives a trajectory segment and sends to each target.

        Arugments:
          kwargs (dict): Additional keyword arguments
        """
        raise NotImplementedError("TrajOutput base class cannot be used "
          "directly; must be subclassed")

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
          (*Subparser*, *Subparsers*): Output format subparser and
            associated collection of converter subparsers
        """
        raise NotImplementedError("TrajOutput base class cannot be used "
          "directly; must be subclassed")

    @staticmethod
    def add_shared_args(subparser, **kwargs):
        """
        Adds command line arguments shared by all output formats.

        Arguments:
          subparser (Subparser): Subparser to which to add arguments
          kwargs (dict): Additional keyword arguments
        """
        arg_groups = {ag.title: ag 
                       for ag in subparser._action_groups}
        arg_groups["output"].add_argument("-outpath",
          type     = str,
          required = True,
          help     = "Output path")
        arg_groups["output"].add_argument("-f", "--force",
          action   = "store_true",
          help     = "Overwrite even if already present")
