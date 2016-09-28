#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

name = "discover"
usage = "[OPTIONS] <extension name> <directory OR header.h> [<directory OR header.h> ...]"
description = "Generate Kludge script stubs from C++ headers"

def main(prog, args):
  from libkludge.discover.main import main
  return main(prog, args)
