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

class Func(Decl):
  def __init__(
    self,
    parent_namespace,
    cpp_global_name,
    kl_global_name,
    returns_cpp_type_expr,
    params,
    ):
    Decl.__init__(
      self,
      parent_namespace,
      )

    self.cpp_global_name = cpp_global_name
    self.kl_global_name = kl_global_name

    self.result = ResultCodec(
      self.type_mgr.get_dqti(
        self.cpp_type_expr_parser.parse(returns_cpp_type_expr)
        )
      )
    self.params = []
    for param_index in range(0, len(params)):
      param = params[param_index]
      self.params.append(
        param.gen_codec(param_index, self.type_mgr, self.cpp_type_expr_parser)
        )
    self.comments = []
  
  def get_edk_symbol_name(self):
    base_edk_symbol_name = self.kl_global_name
    h = hashlib.md5()
    h.update(base_edk_symbol_name)
    for param in self.params:
      h.update(param.type_info.edk.name)
    return "_".join([self.ext.name, base_edk_symbol_name, h.hexdigest()])

  def add_comment(self, comment):
    self.comments.append(util.clean_comment(comment))
    return self

  def get_desc(self):
    return "Function KL[%s] C++[%s]" % (self.kl_global_name, self.cpp_global_name)
  
  def get_test_name(self):
    return self.kl_global_name

  def get_template_path(self):
    return 'generate/func/func'
  
