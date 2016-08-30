#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from decl import Decl
from libkludge.cpp_type_expr_parser import Void
from libkludge.result_codec import ResultCodec
from libkludge.param_codec import ParamCodec
from libkludge import cpp_type_expr_parser
import hashlib
import util

class Func(Decl):
  def __init__(
    self,
    ext,
    name,
    ):
    Decl.__init__(
      self,
      ext,
      "Global function '%s'" % name
      )

    self._nested_function_name = name.split('::')

    self.result_codec = ResultCodec(self.ext.type_mgr.get_dqti(Void()))
    self.params = []

  @property
  def edk_symbol_name(self):
    h = hashlib.md5()
    for name in self._nested_function_name:
      h.update(name)
    for param in self.params:
      h.update(param.type_info.edk.name.toplevel)
    return "_".join([self.ext.name] + self._nested_function_name + [h.hexdigest()])

  def returns(self, cpp_type_name):
    self.result_codec = ResultCodec(
      self.ext.type_mgr.get_dqti(
        self.ext.cpp_type_expr_parser.parse(cpp_type_name)
        )
      )
    return self

  def add_param(self, cpp_type_name, name = None):
    if not isinstance(name, basestring):
      name = "arg%d" % len(self.params)
    self.params.append(
      ParamCodec(
        self.ext.type_mgr.get_dqti(
          self.ext.cpp_type_expr_parser.parse(cpp_type_name)
          ),
        name
        )
      )
    return self

  def get_test_name(self):
    return self.name_kl

  @property
  def name_kl(self):
    return "_".join(self._nested_function_name)

  @property
  def name_cpp(self):
    return "::" + "::".join(self._nested_function_name)

  def get_template_basename(self):
    return 'func'
  
