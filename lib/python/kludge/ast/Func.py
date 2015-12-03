from kludge.ast import Decl

class Func(Decl):
  def __init__(
    self,
    extname,
    include_filename,
    location,
    desc,
    nested_function_name,
    ret_type_codec,
    params,
    ):
    Decl.__init__(self, extname, include_filename, location, desc)

    self._nested_function_name = nested_function_name
    self._ret_type_codec = ret_type_codec
    self.params = params

  def gen_kl_result_type(self):
    if self._ret_type_codec:
      return self._ret_type_codec.gen_kl_result_type()
    else:
      return ""

  def gen_edk_dir_result_type(self):
    if self._ret_type_codec:
      return self._ret_type_codec.gen_edk_dir_result_type()
    else:
      return "void"

  def gen_edk_store_result_pre(self):
    if self._ret_type_codec:
      return self._ret_type_codec.gen_edk_store_result_pre()
    else:
      return ""

  def gen_edk_store_result_post(self):
    if self._ret_type_codec:
      return self._ret_type_codec.gen_edk_store_result_post()
    else:
      return ""

  def gen_edk_return_dir_result(self):
    if self._ret_type_codec:
      return self._ret_type_codec.gen_edk_return_dir_result()
    else:
      return ""

  def gen_kl_name(self):
    return "_".join(self._nested_function_name)

  def gen_edk_name(self):
    return self._extname + "_" + "_".join(self._nested_function_name)

  def gen_cpp_name(self):
    return "::" + "::".join(self._nested_function_name)

  def gen_kl_params(self):
    snippets = []
    for param in self.params:
      snippets.append(param.gen_kl_param())
    return ",\n    ".join(snippets)

  def gen_edk_params(self):
    snippets = []
    if self._ret_type_codec:
      edk_ind_ret_param = self._ret_type_codec.gen_edk_ind_ret_param()
      if edk_ind_ret_param:
        snippets.append(edk_ind_ret_param)
    for param in self.params:
      snippets.append(param.gen_edk_param())
    return ",\n    ".join(snippets)

  def gen_cpp_args(self):
    snippets = []
    for param in self.params:
      snippets.append(param.gen_cpp_arg())
    return ",\n        ".join(snippets)

  def jinjify(self, target, jinjenv):
    return lambda: jinjenv.get_template('edk_func.template.'+target).render(func = self)
