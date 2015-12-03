class TypeCodec:

  def __init__(
    self,
    type_name,
    ):
    self.type_name = type_name

  # Protocol: return

  def raise_unsupported_as_result(self):
    raise Exception(self.type_name.cpp + ": unsupported as result type")

  def gen_kl_result_type(self):
    return self.type_name.kl.base

  def gen_direct_result_edk_type(self):
    self.raise_unsupported_as_result()

  def gen_indirect_result_edk_param(self):
    self.raise_unsupported_as_result()

  def gen_edk_store_result_pre(self):
    self.raise_unsupported_as_result()

  def gen_edk_store_result_post(self):
    self.raise_unsupported_as_result()

  def gen_edk_return_dir_result(self):
    self.raise_unsupported_as_result()

  # Protocol: parameters

  def raise_unsupported_as_param(self):
    raise Exception(self.type_name.cpp + ": unsupported as parameter type")

  def gen_kl_param(self, kl_name):
    self.raise_unsupported_as_param()

  def gen_edk_param(self, edk_name):
    self.raise_unsupported_as_param()

  def gen_edk_param_to_cpp_arg(self, param_name):
    self.raise_unsupported_as_param()

  def gen_cpp_arg(self, param_name):
    self.raise_unsupported_as_param()

  def gen_cpp_arg_to_edk_param(self, param_name):
    self.raise_unsupported_as_param()

  # Helpers

  def gen_kl_in_param(self, kl_name):
    return self.type_name.kl.base + " " + kl_name + self.type_name.kl.suffix

  def gen_kl_io_param(self, kl_name):
    return "io " + self.type_name.kl.base + " " + kl_name + self.type_name.kl.suffix

  def gen_edk_result_name(self):
    return "_KLUDGE_EDK_RESERVED_result";

  def gen_edk_traits(self):
    return "Traits< " + self.type_name.edk + " >"

  def gen_edk_result_param(self):
    return self.gen_edk_traits() + "::Result " + self.gen_edk_result_name()

  def gen_edk_in_param(self, edk_name):
    return self.gen_edk_traits() + "::INParam " + edk_name

  def gen_edk_io_param(self, edk_name):
    return self.gen_edk_traits() + "::IOParam " + edk_name

  def gen_edk_ptr_to(self, edk_name):
    return "&" + edk_name

  def gen_cpp_result_name(self):
    return "_KLUDGE_CPP_RESERVED_result";

  def gen_cpp_ptr_to(self, cpp_name):
    return "&" + cpp_name
