#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from decl import Decl
from libkludge.cpp_type_expr_parser import Void
from libkludge.result_codec import ResultCodec
from libkludge import cpp_type_expr_parser
import hashlib

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

    self._update_edk_symbol_name()

  def _update_edk_symbol_name(self):
    h = hashlib.md5()
    for name in self._nested_function_name:
      h.update(name)
    for param in self.params:
      h.update(param.type_info.edk.name.toplevel)
    self.edk_symbol_name = "_".join([self.ext.name] + self._nested_function_name + [h.hexdigest()])

  def returns(self, cpp_type_name):
    self.result_codec = ResultCodec(
      self.ext.type_mgr.get_dqti(
        self.ext.cpp_type_expr_parser.parse(cpp_type_name)
        )
      )
    return self
    
  def name_kl(self):
    return "_".join(self._nested_function_name)

  def name_cpp(self):
    return "::" + "::".join(self._nested_function_name)

  def jinja_stream_funcs(self, jinjenv, lang):
    return jinjenv.get_template('gen/func/func.template.' + lang).stream(decl=self, func=self)
