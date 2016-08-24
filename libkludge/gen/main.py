#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import optparse
from ext import Ext

usage = "gen [OPTIONS] <name> <gen_script.kludge.py> [<gen_script.kludge.py>...]"
description = "Generate KL extension from a Kludge script"

def main(args):
  opt_parser = optparse.OptionParser(
      usage="%prog " + usage,
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
  if len(args) < 1:
    raise Exception("missing extension name")
  ext = Ext(
    name = args[0],
    opts = opts,
    )
  script_filenames = args[1:]
  if len(script_filenames) == 0:
    ext.warning("No script filename provided, empty extension will be generated")
  else:
    for script_filename in script_filenames:
      ext.process(script_filename)
  ext.write()
