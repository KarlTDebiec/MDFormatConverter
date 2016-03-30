# -*- coding: utf-8 -*-
#   md_format_converter.TrajSegment.py
#
#   Copyright (C) 2012-2016 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
################################### CLASSES ###################################
class TrajSegment(object):
    """
    """

    def __init__(self, number=None, inputs=None, outputs=None, files=None,
        **kwargs):
        """
        """
        self.number = number
        if inputs is not None:
            self.inputs = inputs
        else:
            self.inputs = []
        if outputs is not None:
            self.outputs = outputs
        else:
            self.outputs = []
        self.files = files

    def __str__(self):
        return str(self.number)

    def __repr__(self):

        return str(self.number)

    def __getitem__(self, extension):
        """
        """
        matches = [f for f in self.files if f.endswith(extension)]
        if   len(matches) == 1:
            return matches[0]
        elif len(matches) == 0:
            raise IndexError("No files with extension "
              "{0} present\n".format(extension) +
              "Files present: {0}".format(self.files))
        else:
            raise IndexError("Multiple files with extension "
              "{0} prenet\n".format(extension) +
               "Files present: {0}".format(self.files))
