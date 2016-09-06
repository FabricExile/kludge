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
    cpp_name,
    kl_name = None,
    ):
    Decl.__init__(
      self,
      parent_namespace,
      "Global function '%s'" % cpp_name
      )

    self.cpp_name = cpp_name
    if not kl_name:
      kl_name = cpp_name
    self.kl_name = kl_name

    self.result_codec = ResultCodec(self.type_mgr.get_dqti(Void()))
    self.params = []
  
  def get_edk_symbol_name(self):
    base_edk_symbol_name = self.name_kl
    h = hashlib.md5()
    h.update(base_edk_symbol_name)
    for param in self.params:
      h.update(param.type_info.edk.name)
    return "_".join([self.ext.name, base_edk_symbol_name, h.hexdigest()])

  def returns(self, cpp_type_name):
    self.result_codec = ResultCodec(
      self.type_mgr.get_dqti(
        self.cpp_type_expr_parser.parse(cpp_type_name)
        )
      )
    return self

  def add_param(self, cpp_type_name, name = None):
    if not isinstance(name, basestring):
      name = "arg%d" % len(self.params)
    self.params.append(
      ParamCodec(
        self.type_mgr.get_dqti(
          self.cpp_type_expr_parser.parse(cpp_type_name)
          ),
        name
        )
      )
    return self

  def get_test_name(self):
    return self.name_kl

  @property
  def name_kl(self):
    return "_".join(self.parent_namespace.nested_kl_names + [self.kl_name])

  @property
  def name_cpp(self):
    return "::".join(self.parent_namespace.nested_cpp_names + [self.cpp_name])

  def get_template_basename(self):
    return 'func'
  
