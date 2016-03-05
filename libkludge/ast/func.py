from decl import Decl
from libkludge.value_name import ValueName
from libkludge import cpp_type_expr_parser

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
    Decl.__init__(
      self,
      extname,
      include_filename,
      location,
      "Global function '%s'" % desc
      )

    self._nested_function_name = nested_function_name
    if not isinstance(result_type_info.cpp.expr, cpp_type_expr_parser.Void):
      self.result_codec = result_type_info.make_codec(
        ValueName("RESERVED_result"),
        )
    else:
      self.result_codec = None
    self.params = params

  def result_type_kl(self):
    if self.result_codec:
      return self.result_codec.type.kl.compound
    else:
      return ""

  def result_direct_type_edk(self):
    if self.result_codec:
      return self.result_codec.result_direct_type_edk()
    else:
      return "void"

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

  def jinja_stream(self, jinjenv, lang):
    return jinjenv.get_template('func.template.' + lang).stream(decl = self)
