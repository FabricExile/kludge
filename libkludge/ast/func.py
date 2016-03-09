from decl import Decl
from libkludge.result_codec import ResultCodec
from libkludge import cpp_type_expr_parser

class Func(Decl):
  def __init__(
    self,
    extname,
    include_filename,
    location,
    desc,
    nested_function_name,
    result_dqti,
    param_codecs,
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
    self.params = param_codecs

  def name_kl(self):
    return "_".join(self._nested_function_name)

  def name_edk(self):
    return self._extname + "_" + "_".join(self._nested_function_name)

  def name_cpp(self):
    return "::" + "::".join(self._nested_function_name)

  def jinja_stream(self, jinjenv, lang):
    return jinjenv.get_template('ast/builtin/func.template.' + lang).stream(decl = self)
