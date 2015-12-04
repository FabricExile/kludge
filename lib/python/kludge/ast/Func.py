from kludge.ast import Decl
from kludge import ValueName, Value

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
    if result_type_info:
      self._result_value = Value(
        ValueName("RESERVED_result"),
        result_type_info,
        )
    else:
      self._result_value = None
    self.params = params

  @property
  def kl_result_type(self):
    if self._result_value:
      return self._result_value.kl_result_type
    else:
      return ""

  @property
  def direct_result_edk_type(self):
    if self._result_value:
      return self._result_value.direct_result_edk_type
    else:
      return "void"

  @property
  def edk_store_result_pre(self):
    if self._result_value:
      return self._result_value.edk_store_result_pre
    else:
      return ""

  @property
  def edk_store_result_post(self):
    if self._result_value:
      return self._result_value.edk_store_result_post
    else:
      return ""

  @property
  def edk_return_direct_result(self):
    if self._result_value:
      return self._result_value.edk_return_direct_result
    else:
      return ""

  @property
  def kl_name(self):
    return "_".join(self._nested_function_name)

  @property
  def edk_name(self):
    return self._extname + "_" + "_".join(self._nested_function_name)

  @property
  def cpp_name(self):
    return "::" + "::".join(self._nested_function_name)

  @property
  def kl_params(self):
    snippets = []
    for param in self.params:
      snippets.append(param.kl_param)
    return ",\n    ".join(snippets)

  @property
  def edk_params(self):
    snippets = []
    if self._result_value:
      indirect_result_edk_param = self._result_value.indirect_result_edk_param
      if indirect_result_edk_param:
        snippets.append(indirect_result_edk_param)
    for param in self.params:
      snippets.append(param.edk_param)
    return ",\n    ".join(snippets)

  @property
  def cpp_args(self):
    snippets = []
    for param in self.params:
      snippets.append(param.cpp_arg)
    return ",\n        ".join(snippets)

  def jinjify(self, target, jinjenv):
    return lambda: jinjenv.get_template('edk_func.template.'+target).render(func = self)
