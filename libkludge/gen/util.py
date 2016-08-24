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

def is_kl_keyword(name):
  return name in [
    "alias",
    "async",
    "ArrayProducer",
    "break",
    "case",
    "_CN",
    "const",
    "continue",
    "createArrayCache",
    "createArrayGenerator",
    "createArrayMap",
    "createArrayTransform",
    "createConstArray",
    "createConstValue",
    "createReduce",
    "createValueCache",
    "createValueGenerator",
    "createValueMap",
    "createValueTransform",
    "default",
    "do",
    "else",
    "__export",
    "EXT_VER_ENDIF",
    "EXT_VER_IF",
    "false",
    "FILE",
    "for",
    "function",
    "idle",
    "if",
    "in",
    "inline",
    "interface",
    "io",
    "LINE",
    "lock",
    "null",
    "object",
    "on",
    "operator",
    "out",
    "permits",
    "public",
    "protected",
    "private",
    "Ref",
    "require",
    "return",
    "StackChain",
    "struct",
    "switch",
    "throw",
    "true",
    "ValueProducer",
    "var",
    "while",
    ]
