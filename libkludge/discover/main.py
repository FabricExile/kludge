#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

import sys, optparse
from libkludge import util
from libkludge.discover import name, usage, description

def quit_with_usage(prog):
  print "Run '%s %s --help' for usage" % (prog, name)
  sys.exit(1)

def main(prog, args):
  opt_parser = optparse.OptionParser(
    usage="%%prog %s %s" % (prog, usage),
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
    '-s', '--skip-master',
    action='store_true',
    default=False,
    dest='skip_master',
    help="Skip generation of master .kludge.py script",
    )
  opt_parser.add_option(
    '', '--ignore-dir',
    action='append',
    dest='dirs_to_ignore',
    metavar='DIR',
    help="Ignore DIR when finding header files to parse",
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
    '-L', None,
    action='append',
    dest='libpath',
    metavar='DIR',
    help="Add directory to library path",
    )
  opt_parser.add_option(
    '-l', None,
    action='append',
    dest='libs',
    metavar='LIB',
    help="Add library for link",
    )
  opt_parser.add_option(
    '-C', '--clang-opt',
    action='append',
    dest='clang_opts',
    metavar='OPT',
    help="Pass option to Clang++",
    )
  (opts, args) = opt_parser.parse_args(args=args)
  ext_name = args[0]
  dirs_and_files = args[1:]
  if not opts.dirs_to_ignore:
    opts.dirs_to_ignore = []
  if len(dirs_and_files) == 0:
    util.error(opts, "Missing directories and/or headers to process")
    quit_with_usage(prog)
  from libkludge.discover.parser import Parser
  parser = Parser(
    name = args[0],
    opts = opts,
    )
  parser.process(ext_name, dirs_and_files)
  return 0
