#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from decl import Decl
from libkludge.cpp_type_expr_parser import Void
from libkludge.result_codec import ResultCodec
from libkludge.param_codec import ParamCodec
from libkludge import cpp_type_expr_parser
import hashlib
from libkludge import util

class BinOp(Decl):
  op_to_edk_op = {
    "+": 'ADD',
    "-": 'SUB',
    "*": 'MUL',
    "/": 'DIV',
    "%": 'MOD',
    "==": 'EQ',
    "!=": 'NE',
    "<": 'LT',
    "<=": 'LE',
    ">": 'GT',
    ">=": 'GE',
    "===": 'EX_EQ',
    "!==": 'EX_NE',
    "|": 'BIT_OR',
    "&": 'BIT_AND',
    "^": 'BIT_XOR',
    "<<": 'SHL',
    ">>": 'SHR',
  }

  def __init__(
    self,
    parent_namespace,
    op,
    returns_cpp_type_expr,
    params,
    ):
    Decl.__init__(
      self,
      parent_namespace,
      )

    self.op = op

    self.result = ResultCodec(
      self.type_mgr.get_dqti(
        self.cpp_type_expr_parser.parse(returns_cpp_type_expr)
        )
      )
    self.params = []
    for param_index in range(0, len(params)):
      param = params[param_index]
      param_codec = param.gen_codec(param_index, parent_namespace.resolve_dqti)
      if not param_codec:
        raise Exception("cannot parse type for parameter %d" % (param_index + 1))
      self.params.append(param_codec)
    self.comments = []
  
  def get_edk_symbol_name(self):
    base_edk_symbol_name = 'bin_op_' + self.op_to_edk_op[self.op]
    h = hashlib.md5()
    h.update(base_edk_symbol_name)
    for param in self.params:
      h.update(param.type_info.edk.name)
    return "_".join([self.ext.name, base_edk_symbol_name, h.hexdigest()])

  def add_comment(self, comment):
    self.comments.append(util.clean_comment(comment))
    return self

  def get_desc(self):
    return "BinOp KL[%s] C++[%s]" % (self.op, self.op)
  
  def get_test_name(self):
    return 'bin_op_' + self.op_to_edk_op[self.op]

  def get_template_path(self):
    return 'generate/bin_op/bin_op'
  
  def get_template_aliases(self):
    return ['bin_op']
