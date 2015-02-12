Introduction
============

md_format_converter is a python package used to convert Molecular Dynamics (MD)
simulation trajectories that are split into multiple files (segments) between
different formats. Currently, the package exclusively supports converstion from
Anton format trajectories to PDB and Amber NetCDF formats, using the program
Visual Molecular Dynamics (VMD). The package is currently much more complex
than necessary for this purpose, in order to facilitate future integration in
complex conversion and analysis pipelines.

Dependencies
------------

md_format_converter supports Python 2.7, and requires the program Visual
Molecular Dynamics (VMD).

Installation
------------

Put in your ``$PYTHONPATH``::

    export PYTHONPATH=/path/to/my/python/modules:$PYTHONPATH

where ``/path/to/my/python/modules`` contains ``md_format_converter``.

Authorship
----------

md_format_converter is developed by Karl T. Debiec, a graduate student at the
University of Pittsburgh advised by Professors Lillian T. Chong and Angela M.
Gronenborn.

License
-------

Released under a 3-clause BSD license.
