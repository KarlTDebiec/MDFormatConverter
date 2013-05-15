#!/usr/bin/python
desc = """xtc_converter.py
    Converts trajectories to pdb and xtc format
    Written by Karl Debiec on 13-04-12
    Last updated 13-05-15"""
########################################### MODULES, SETTINGS, AND DEFAULTS ############################################
import argparse, os, subprocess, sys
from   standard_functions import Segment, execute_shell_command, segments_standard
vmd_script  = os.path.dirname(os.path.realpath(__file__)) + "/trr_converter.tcl"
###################################################### FUNCTIONS #######################################################
def segments_stk(path, stk):
    segments    = []
    with open(stk, "r") as stk:
        for segment, atr in enumerate(stk.readlines()):
            files       = [atr.strip()]
            ene         = atr[:-9] + "/energy/eneseq.txt"
            if os.path.isfile(ene):
                files  += [ene]
            segments   += [Segment(number   = "{0:04d}".format(segment),
                                   path     = "{0}{1:04d}/".format(path, segment),
                                   files    = files)]
    return segments

def convert(vmd_eval, path, output, force = False, in_progress = False, **kwargs):
    segments        = segments_standard(path)
    if in_progress:   segments = segments[:-1]
    for segment in segments:
        print segment, segment.path
        new_output      = False
        vmd_command     = eval(vmd_eval)
        trjconv_command = ""
        rm_command      = ""
        for sel, suffix in output:
            prefix  = segment.path + segment + suffix
            if force or not os.path.isfile(prefix  + ".pdb") or not os.path.isfile(prefix  + ".xtc"):
                new_output          = True
                vmd_command        += " \"{0}\" {1}.pdb {1}.trr ".format(sel, prefix)
                trjconv_command    += " trjconv -f {0}.trr -o {0}.xtc -ndec 5; ".format(prefix)
                rm_command         += " rm -v {0}.trr; ".format(prefix)
        if new_output:
            execute_shell_command(vmd_command)
            execute_shell_command(trjconv_command, output = "stderr")
            execute_shell_command(rm_command)

def convert_desmond(infile = None, **kwargs):
    if not (infile == None):
        raise Exception("Desmond converter does not accept infile(s)")
    vmd_eval        = "\"vmd -dispdev text -e " + vmd_script + " -args desmond {0} {1}/clickme.dtr\"" + \
                      ".format(segment.file_of_type('cms'), segment.file_of_type('_trj'))"
    convert(vmd_eval, **kwargs)

def convert_amber(infile = None,**kwargs):
    if not (isinstance(infile, list) and len(infile) == 1):
        raise Exception("Amber converter requires prmtop infile")
    top             = infile[0]
    vmd_eval        = "\"vmd -dispdev text -e " + vmd_script + " -args amber " + top + " {0}\"" + \
                      ".format(segment.file_of_type('crd'))"
    convert(vmd_eval, **kwargs)

def convert_anton(path, output, infile = None, force = False, in_progress = False, **kwargs):
    if not (isinstance(infile, list) and len(infile) == 2):
        raise Exception("Anton converter requires cms and stk infiles")
    cms, stk        = infile
    segments        = segments_stk(path, stk)
    if in_progress:   segments = segments[:-1]
    vmd_eval        = "\"vmd -dispdev text -e " + vmd_script + " -args anton " + cms + " {0}\"" + \
                      ".format(segment.file_of_type('atr'))"
    for segment in segments:
        print segment, segment.path
        execute_shell_command("mkdir -pv {0}".format(segment.path))
        new_output      = False
        vmd_command     = eval(vmd_eval)
        trjconv_command = ""
        rm_command      = ""
        for sel, suffix in output:
            prefix      = segment.path + segment + suffix
            ene         = segment.path + segment + ".ene"
            if force or not os.path.isfile(prefix  + ".pdb") or not os.path.isfile(prefix  + ".xtc"):
                new_output          = True
                vmd_command        += " \"{0}\" {1}.pdb {1}.trr ".format(sel, prefix)
                trjconv_command    += " trjconv -f {0}.trr -o {0}.xtc -ndec 5; ".format(prefix)
                rm_command         += " rm -v {0}.trr; ".format(prefix)
        if new_output:
            execute_shell_command(vmd_command)
            execute_shell_command(trjconv_command, output = "stderr")
            execute_shell_command(rm_command)
            try:      execute_shell_command("cp -v {0} {1}".format(segment.file_of_type("eneseq.txt"), ene))
            except:   continue

def convert_gromacs(path, output, infile = None, force = False, in_progress = False, **kwargs):
    if infile != None:
        raise Exception("Gromacs converter does not accept infile(s)")
    segments        = segments_standard(path) 
    if in_progress:   segments = segments[:-1]
    for sel, suffix in output:
        if suffix  == "":
            raise Exception("Gromacs conversion without suffix may overwrite original xtc file")
    vmd_eval        = "\"vmd -dispdev text -e " + vmd_script + " -args gromacs {0} {1}\"" + \
                      ".format(segment.file_of_type('gro'), segment.file_of_type(segment + '.xtc'))"
    for segment in segments:
        print segment, segment.path
        new_output      = False
        vmd_command     = eval(vmd_eval)
        trjconv_command = ""
        rm_command      = ""
        for sel, suffix in output:
            prefix      = segment.path + segment + suffix
            if force or not os.path.isfile(prefix  + ".pdb") or not os.path.isfile(prefix  + ".xtc"):
                new_output          = True
                vmd_command        += " \"{0}\" {1}.pdb {1}.trr ".format(sel, prefix)
                trjconv_command    += " echo -e \"1 \n\" | trjconv -f {0}.trr -o {0}.xtc".format(prefix) + \
                                      " -s {0}/{1}.tpr -ndec 5 -pbc whole; ".format(segment.path, segment)
                rm_command         += " rm -v {0}.trr; ".format(prefix)
        if new_output:
            execute_shell_command(vmd_command)
            execute_shell_command(trjconv_command, output = "stderr")
            execute_shell_command(rm_command)

######################################################### MAIN #########################################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = desc, formatter_class = argparse.RawTextHelpFormatter)
    parser.add_argument("-package",
      required  = True,
      type      = str,
      choices   = ["amber", "anton", "desmond", "gromacs"],
      help      = "Molecular dynamics package")
    parser.add_argument("-path",
      required  = True,
      type      = str,
      help      = "Trajectory path")
    parser.add_argument("-infile",
      type      = str,
      nargs     = "*",
      help      = "Infile(s) including topology; number of arguments required depends on package")
    parser.add_argument("-output",
      required  = True,
      action    = "append",
      type      = str,
      nargs     = "*",
      help      = "Output atom selections and suffixes for outfiles. Must be multiple of two. " +
                  "E.g. \"-output 'not water' '_solute'\"")
    parser.add_argument("--force",
      action    = "store_true",
      help      = "Force output; do not skip segments for which expected output is already present")
    parser.add_argument("--in_progress",
      action    = "store_true",
      help      = "Omit last segment of trajectory")

    kwargs      = dict(((k,v) for k,v in dict(parser.parse_args()._get_kwargs()).iteritems() if v is not None))
    raw_output  = kwargs.pop("output")[0]
    if len(raw_output) % 2 != 0:
        raise Exception("Output arguments must be in pairs of atom selection and suffix")
    kwargs["output"]    = []
    while len(raw_output) >= 2:
        kwargs["output"] += [(raw_output.pop(0).replace(" ", "_"), raw_output.pop(0))]

    locals()["convert_" + kwargs.pop("package")](**kwargs)
