# -*- coding: utf-8 -*-
#   md_format_converter.TrajInput.py
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
################################### CLASSES ###################################
class TrajInput(object):
    """
    Manages generation of segments from an input trajectory.
    """

    def __init__(self, **kwargs):
        """
        Initializes; currently no function.

        Arugments:
          kwargs (dict): Additional keyword arguments
        """
        pass

    def __iter__(self, **kwargs):
        """
        Allows class to act as a generator.
        """
        return self

    def next(self):
        """
        Prepares and yields next trajectory segment.
        """
        raise NotImplementedError("TrajInput base class cannot be used "
          "directly; must be subclassed")

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
        raise NotImplementedError("TrajInput base class cannot be used "
          "directly; must be subclassed")

    @staticmethod
    def add_shared_args(subparser, **kwargs):
        """
        Adds command line arguments shared by all input formats.

        Arguments:
          subparser (Subparser): Subparser to which to add arguments
          kwargs (dict): Additional keyword arguments
        """
        arg_groups = {ag.title: ag 
                       for ag in subparser._action_groups}
        arg_groups["input"].add_argument("--in_progress",
          action = "store_true",
          help   = "Omit last segment of trajectory")
