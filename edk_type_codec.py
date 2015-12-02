class EDKTypeCodec:

  def __init__(
    self,
    kl_type_name,
    cpp_type_name,
    ):
    self.kl_type_name = kl_type_name
    self.cpp_type_name = cpp_type_name

  # Protocol: return

  def raise_unsupported_as_ret(self):
    raise self.cpp_type_name + ": unsupported as return"

  def gen_dir_ret_type(self):
    self.raise_unsupported_as_ret()

  def gen_ind_ret_param(self, edk_name):
    self.raise_unsupported_as_ret()

  # Protocol: parameters

  def raise_unsupported_as_param(self):
    raise self.cpp_type_name + ": unsupported as parameter"

  def gen_kl_param(self, kl_name):
    self.raise_unsupported_as_param()

  def gen_edk_param(self, edk_name):
    self.raise_unsupported_as_param()

  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    self.raise_unsupported_as_param()

  def gen_cpp_arg(self, edk_name, cpp_name):
    self.raise_unsupported_as_param()

  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
    self.raise_unsupported_as_param()

  # Helpers

  def gen_kl_in_param(self, kl_name):
    return self.kl_type_name + " " + kl_name

  def gen_kl_io_param(self, kl_name):
    return "io " + self.kl_type_name + " " + kl_name

  def gen_edk_result(self, edk_name):
    return "Traits<" + self.kl_type_name + ">::Result " + edk_name

  def gen_edk_in_param(self, edk_name):
    return "Traits<" + self.kl_type_name + ">::INParam " + edk_name

  def gen_edk_io_param(self, edk_name):
    return "Traits<" + self.kl_type_name + ">::IOParam " + edk_name

  def gen_edk_ptr_to(self, edk_name):
    return "&" + edk_name

  def gen_cpp_ptr_to(self, cpp_name):
    return "&" + cpp_name

class EDKIndRetTypeCodec(EDKTypeCodec):

  def __init__(self, kl_type_name, cpp_type_name):
    EDKTypeCodec.__init__(self, kl_type_name, cpp_type_name)
  
  def gen_dir_ret_type(self):
    return "void"

  def gen_ind_ret_param(self, edk_name):
    return gen_edk_result(edk_name)
