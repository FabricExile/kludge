#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
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

class EmptyCommentContainer(object):
  def add_comment(self, comment):
    pass
  def add_test(kl, out, test_name='', skip_epilog=False):
    pass

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
    "entry",
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

def is_builtin_type_name(type_name):
  return type_name in [
    'Boolean',
    'SInt8',
    'UInt8',
    'SInt16',
    'UInt16',
    'SInt32',
    'UInt32',
    'SInt64',
    'UInt64',
    'Float32',
    'Float64',
    'Byte',
    'Index',
    'Size',
    'String',
    'Data',
    'Type',

    'Vec2',
    'Vec3',
    'Vec4',
    'Quat',
    'RotationOrder',
    'Euler',
    'Color',
    'Xfo',
    'Mat22',
    'Mat33',
    'Mat44',
    'Box2',
    'Box3',
    'Box4',
    ]

def is_builtin_method_name(method_name):
    return method_name in [
        'data',
        'dataSize',
        'clone',
        'cloneMembersTo',
        ]

def clean_method_name(method_name):
    if is_kl_keyword(method_name) \
        or is_builtin_method_name(method_name) \
        or is_builtin_type_name(method_name):
            return method_name + '_'
    return method_name


builtin_cxx_suffixes = [
    'get',
    'set',
    'getAtIndex',
    'setAtIndex',
    'deref',
    ]

def clean_cxx_method_name(method_name):
    if method_name in builtin_cxx_suffixes:
        return method_name + '_'
    return method_name

def clean_param_name(param_name):
    if is_kl_keyword(param_name) \
        or is_builtin_type_name(param_name):
          return param_name + '_'
    return param_name

def clean_comment(comment):
    comment = comment.strip()
    if comment.startswith('/*'):
        return comment
    safe_lines = []
    for line in comment.splitlines():
        line = line.strip()
        if line.startswith('//'):
            safe_lines.append(line)
        else:
            safe_lines.append('// ' + line)
    return '\n'.join(safe_lines)
