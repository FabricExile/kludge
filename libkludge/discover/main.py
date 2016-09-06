#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import sys, optparse
# from parser import Parser
import libkludge.util

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
      action='store',
      default='2',
      dest='verbosity',
      metavar='VERBOSITY',
      help="Verbosity of output (defaults to 2)",
      )
  (opts, args) = opt_parser.parse_args(args=args)
  opts.verbosity = int(opts.verbosity)
  headers = args
  if len(headers) == 0:
    util.error(opts, "Missing header to process")
    quit_with_usage(prog)
  parser = Parser(
    name = args[0],
    opts = opts,
    )
  for script_filename in headers:
    ext.process(script_filename)
  ext.write()
  return 0
