#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import sys

def log(opts, level, string):
  if opts.verbosity >= level:
    print string

def error(opts, string):
  log(opts, 0, "Error: %s" % string)

def warning(opts, string):
  log(opts, 1, "Warning: %s" % string)

def info(opts, string):
  log(opts, 2, string)

def debug(opts, string):
  log(opts, 3, "Debug: %s" % string)
