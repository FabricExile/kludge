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
    extname,
    include_filename,
    location,
    desc,
    nested_function_name,
    result_dqti,
    params,
    ):
    Decl.__init__(
      self,
      extname,
      include_filename,
      location,
      "Global function '%s'" % desc
      )

    self._nested_function_name = nested_function_name
    if result_dqti:
      self.result_codec = ResultCodec(result_dqti)
    else:
      self.result_codec = None
    self.params = params

    h = hashlib.md5()
    for name in nested_function_name:
      h.update(name)
    for param in params:
      h.update(param.type_info.edk.name.toplevel)
    self.edk_symbol_name = "_".join([self._extname] + self._nested_function_name + [h.hexdigest()])

  def name_kl(self):
    return "_".join(self._nested_function_name)

  def name_cpp(self):
    return "::" + "::".join(self._nested_function_name)

  def jinja_stream_funcs(self, jinjenv, lang):
    return jinjenv.get_template('ast/builtin/func.template.' + lang).stream(decl = self)
