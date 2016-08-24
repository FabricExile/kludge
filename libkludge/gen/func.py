#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from decl import Decl
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

    self.result_codec = None
    self.params = []

  @property
  def edk_symbol_name(self):
    h = hashlib.md5()
    for name in nested_function_name:
      h.update(name)
    for param in params:
      h.update(param.type_info.edk.name.toplevel)
    return "_".join([self._ext.name] + self._nested_function_name + [h.hexdigest()])

  def name_kl(self):
    return "_".join(self._nested_function_name)

  def name_cpp(self):
    return "::" + "::".join(self._nested_function_name)

  def jinja_stream_funcs(self, jinjenv, lang):
    return jinjenv.get_template('func/func.template.' + lang).stream(decl=self, func=self)
