from kludge.ast import Decl
from kludge import ValueName, Value, CPPTypeExpr

class Func(Decl):
  def __init__(
    self,
    extname,
    include_filename,
    location,
    desc,
    nested_function_name,
    result_type_info,
    params,
    ):
    Decl.__init__(self, extname, include_filename, location, desc)

    self._nested_function_name = nested_function_name
    if not isinstance(result_type_info.cpp.expr, CPPTypeExpr.Void):
      self._result_codec = result_type_info.make_codec(
        ValueName("RESERVED_result"),
        )
    else:
      self._result_codec = None
    self.params = params

  def result_type_kl(self):
    if self._result_codec:
      return self._result_codec.type.kl.compound
    else:
      return ""

  def result_direct_type_edk(self):
    if self._result_codec:
      return self._result_codec.result_direct_type_edk()
    else:
      return "void"

  def result_indirect_param_edk(self):
    if self._result_codec:
      return self._result_codec.result_indirect_param_edk()
    else:
      return ""

  def result_indirect_init_edk(self):
    if self._result_codec:
      return self._result_codec.result_indirect_init_edk()
    else:
      return ""

  def result_decl_and_assign_cpp(self):
    if self._result_codec:
      return self._result_codec.result_decl_and_assign_cpp()
    else:
      return ""

  def result_indirect_assign_to_edk(self):
    if self._result_codec:
      return self._result_codec.result_indirect_assign_to_edk()
    else:
      return ""

  def result_direct_return_edk(self):
    if self._result_codec:
      return self._result_codec.result_direct_return_edk()
    else:
      return ""

  def name_kl(self):
    return "_".join(self._nested_function_name)

  def name_edk(self):
    return self._extname + "_" + "_".join(self._nested_function_name)

  def name_cpp(self):
    return "::" + "::".join(self._nested_function_name)

  def params_kl(self):
    snippets = []
    for param in self.params:
      snippets.append(param.param_kl())
    return ",\n".join(snippets)

  def params_edk(self):
    snippets = []
    if self._result_codec:
      result_indirect_param_edk = self._result_codec.result_indirect_param_edk()
      if result_indirect_param_edk:
        snippets.append(result_indirect_param_edk)
    for param in self.params:
      snippets.append(param.param_edk())
    return ",\n".join(snippets)

  def params_cpp(self):
    snippets = []
    for param in self.params:
      snippets.append(param.param_cpp())
    return ",\n".join(snippets)

  def jinja_stream(self, jinjenv, lang):
    return jinjenv.get_template('func.template.' + lang).stream(func = self)
