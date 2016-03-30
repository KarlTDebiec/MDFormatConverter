Introduction
============

md_format_converter is a python script used to convert Molecular Dynamics (MD)
simulation trajectories that are split into multiple segments between different
formats. Currently, the package exclusively supports conversion from `Anton
<https://www.psc.edu/index.php/computing-resources/anton>`_ format trajectories
to `PDB <http://deposit.rcsb.org/adit/docs/pdb_atom_format.html>`_, `mol2
<http://www.tripos.com/data/support/mol2.pdf>`_, `AMBER text mdcrd
<http://ambermd.org/formats.html#trajectory>`_, and `GROMACS trr
<http://www.gromacs.org/Documentation/File_Formats/.trr_File>`_ formats, using
the program `Visual Molecular Dynamics (VMD)
<http://www.ks.uiuc.edu/Research/vmd>`_. It supports manual writing of bonds to
mol2 format (as guessed by VMD based on geometry), which may be helpful for
recovering trajectories whose atoms are not in standard order. Conversion to a
single format is supported from the command line, while conversion to multiple
formats is supported via a `YAML <http://www.yaml.org/spec/1.2/spec.html>`_
configuration file.

The script is much more complex than strictly necessary for the above, as an
exercise in applying coroutines and writing a multilevel argument parser.

Dependencies
------------

md_format_converter supports Python 2.7, and requires the program Visual
Molecular Dynamics (VMD).

Installation
------------

No intstallation is necessary, just run ``convert.py``:

    python /path/to/convert.py -h

Authorship
----------

md_format_converter is developed by Karl T. Debiec, a graduate student at the
University of Pittsburgh advised by Professors Lillian T. Chong and Angela M.
Gronenborn.

License
-------

Released under a 3-clause BSD license.
