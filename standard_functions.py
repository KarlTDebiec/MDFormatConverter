#!/usr/bin/python

desc = """standard_functions.py
    Standard functions
    Written by Karl Debiec on 13-02-03
    Last updated 13-04-14"""
########################################### MODULES, SETTINGS, AND DEFAULTS ############################################
import os, subprocess, sys
import numpy as np
################################################ SEGMENT LIST FUNCTIONS ################################################
class Segment:
    def __init__(self, number, path, topology = None, trajectory = None, files = None):
        self.number     = number
        self.path       = path
        if topology   != None:  self.topology   = topology
        if trajectory != None:  self.trajectory = trajectory
        self.files      = files
    def __float__(self):        return float(self.number)
    def __str__(self):          return self.number
    def __repr__(self):         return self.number
    def __add__(self, other):   return str(self.number) + other
    def __radd__(self, other):  return other + str(self.number)
    def file_of_type(self, end):
        temp    = [f for f in self.files if f.endswith(end)]
        if len(temp) == 1:  return temp[0]
        else:               raise  Exception("Multiple files with extension {0} present".format(end))
def segments_standard(path):
    """ Lists segment folders, topologies, and trajectories  at <path>, assuming the format ####/####.* """
    segments = []
    for directory in sorted([f for f in os.listdir(path) if is_num(f)]):
        files       = ["{0}/{1}/{2}".format(path, directory, f) for f in os.listdir("{0}/{1}/".format(path, directory))]
        segments   += [Segment(number       = directory,
                               path         = "{0}/{1}/".format(path, directory),
                               files        = files)]
    return segments
################################################## GENERAL FUNCTIONS ###################################################
def is_num(test):
    try:    float(test)
    except: return False
    return  True
def execute_shell_command(command, leader = "", output = "stdout"):
    pipe    = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    if   output == "stdout":
        for line in iter(pipe.stdout.readline, ""):     print "{0}{1}".format(leader, line.rstrip().replace("\n", " "))
    elif output == "stderr":
        for line in iter(pipe.stderr.readline, ""):     print "{0}{1}".format(leader, line.rstrip().replace("\n", " "))
    pipe.wait()
