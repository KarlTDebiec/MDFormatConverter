# -*- coding: utf-8 -*-
#   md_format_converter.Converter.py
#
#   Copyright (C) 2012-2015 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Manages conversion of segments between output formats.
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
################################### CLASSES ###################################
class Converter(object):
    """
    Manages conversion of segments between formats.
    """

    def __init__(self, **kwargs):
        """
        Initializes.

        Arugments:
          kwargs (dict): Additional keyword arguments
        """
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

    def receive_segment(self, **kwargs):
        """
        Receives a trajectory segment.

        Arugments:
          kwargs (dict): Additional keyword arguments
        """
        raise NotImplementedError("Converter base class cannot be used "
          "directly; must be subclassed")

    @staticmethod
    def add_subparser(level1_subparser, level2_subparser, level3_subparsers):
        """
        Adds subparser for this converter to nascent parser.

        Arguments:
          level3_subparsers (Subparsers): Nascent collection of
            converter subparsers

        Returns:
          (*Subparser*): Converter subparser
        """
        raise NotImplementedError("Converter base class cannot be used "
          "directly; must be subclassed")

    @staticmethod
    def add_shared_args(subparser, **kwargs):
        """
        Adds command line arguments shared by all converters.

        Arguments:
          subparser (Subparser): Subparser to which to add arguments
          kwargs (dict): Additional keyword arguments
        """
        arg_groups = {ag.title: ag 
                       for ag in subparser._action_groups}
        arg_groups["output"].add_argument("-suffix",
          type = str,
          help = "Suffix to add to output files; between segment number "
                 "and extenstion e.g 0000_solute.pdb")
