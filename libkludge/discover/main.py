#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import sys, optparse
from parser import Parser
from libkludge import util

name = "discover"
usage = "[OPTIONS] <header.h> [<header.h> ...]"
description = "Generate Kludge script stubs from C++ headers"

def quit_with_usage(prog):
  print "Run '%s %s --help' for usage" % (prog, name)
  sys.exit(1)

def main(prog, args):
  opt_parser = optparse.OptionParser(
    usage="%%prog %s %s" % (name, usage),
    description=description,
    )
  opt_parser.add_option(
    '-o', '--output-dir',
    action='store',
    default='.',
    dest='outdir',
    metavar='OUTDIR',
    help="output directory (defaults to .)",
    )
  opt_parser.add_option(
    '-v', '--verbosity',
    type='int',
    action='store',
    default=2,
    dest='verbosity',
    metavar='VERBOSITY',
    help="Verbosity of output (defaults to 2)",
    )
  opt_parser.add_option(
    '-I', None,
    action='append',
    dest='cpppath',
    metavar='DIR',
    help="Add directory to C++ include path",
    )
  opt_parser.add_option(
    '-D', None,
    action='append',
    dest='cppdefines',
    metavar='DEFINE',
    help="Define a preprocessor value",
    )
  opt_parser.add_option(
    '-C', '--clang-opt',
    action='append',
    dest='clang_opts',
    metavar='OPT',
    help="Pass option to Clang++",
    )
  (opts, args) = opt_parser.parse_args(args=args)
  headers = args
  if len(headers) == 0:
    util.error(opts, "Missing header to process")
    quit_with_usage(prog)
  parser = Parser(
    name = args[0],
    opts = opts,
    )
  for script_filename in headers:
    parser.process(script_filename)
  return 0
