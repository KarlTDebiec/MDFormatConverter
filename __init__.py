# -*- coding: utf-8 -*-
#   md_format_converter.__init__.py
#
#   Copyright (C) 2012-2016 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
.. todo:
    - Pass debug and verbose to VMD
    - Figure out reasonable way to copy Anton ene log
"""
################################### MODULES ###################################
from os.path import dirname
################################## VARIABLES ##################################
MODULE_PATH = dirname(__file__)
################################## FUNCTIONS ##################################
def get_yaml(input):
    """
    Generates a data structure from YAML input.

    If ``input`` is a string, tests whether or not it is a path to a YAML file.
    If it is, the file is loaded using yaml; if it is not, the string itself is
    loaded using YAML. If ``input`` is a dict, it is returned without
    modification.

    Arguments:
      input (str, dict): YAML input

    Returns:
      (*dict*): Data structure specified by input

    Raises:
      TypeError: Input file type not understood.
    """
    import six

    if six.PY2:
        open_yaml = file
    else:
        open_yaml = open

    if isinstance(input, dict):
        return input
    elif isinstance(input, six.string_types):
        from os.path import isfile
        import yaml

        if isfile(input):
            with open_yaml(input, "r") as infile:
                return yaml.load(infile)
        else:
            return yaml.load(input)
    else:
        raise TypeError("get_yaml does not understand input of type " +
          "{0}".format(type(input)))

def merge_dicts(dict_1, dict_2):
    """
    Recursively merges two dictionaries.

    Arguments:
      dict_1 (dict): First dictionary
      dict_2 (dict): Second dictionary; values for keys shared by both
        dictionaries are drawn from dict_2

    Returns:
      (*dict*): Merged dictionary
    """
    def merge(dict_1, dict_2):
        """
        Generator used to recursively merge two dictionaries

        Arguments:
          dict_1 (dict): First dictionary
          dict_2 (dict): Second dictionary; values for keys shared by
            both dictionaries are drawn from dict_2

        Yields:
          (*tuple*): Merged (key, value) pair
        """
        for key in set(dict_1.keys()).union(dict_2.keys()):
            if key in dict_1 and key in dict_2:
                if (isinstance(dict_1[key], dict)
                and isinstance(dict_2[key], dict)):
                    yield (key, dict(merge(dict_1[key], dict_2[key])))
                else:
                    yield (key, dict_2[key])
            elif key in dict_1:
                yield (key, dict_1[key])
            else:
                yield (key, dict_2[key])

    return dict(merge(dict_1, dict_2))

def run_command(command, leader="", verbose=False, **kwargs):
    """
    Runs a shell command, optionally printing live output.

    Arguments:
      command (string): Shell command to run
      leader (string): String with which to prepend output
      verbose (bool): Enable verbose output
      kwargs (dict): Additional keyword arguments
    """
    from subprocess import Popen, PIPE, STDOUT

    if verbose:
        print leader + command
    pipe = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT, **kwargs)
    for line in iter(pipe.stdout.readline, ""):
        out_line = leader + line.rstrip().replace("\n", " ")
        if verbose:
            print(out_line)
