from edk_type_codec import *

class EDKCStringBaseTypeCodec(EDKIndRetTypeCodec):

  def __init__(self, kl_type_name, cpp_type_name):
    EDKIndRetTypeCodec.__init__(self, kl_type_name, cpp_type_name)

  def gen_get_cstring(self, edk_name):
    return edk_name + ".getCString()"

class EDKCStringValueTypeCodec(EDKCStringBaseTypeCodec):

  def __init__(self, kl_type_name, cpp_type_name):
    EDKCStringBaseTypeCodec.__init__(self, kl_type_name, cpp_type_name)

  def gen_kl_param(self, kl_name):
    return self.gen_kl_in_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_in_param(edk_name)

  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    return ""

  def gen_cpp_arg(self, edk_name, cpp_name):
    return self.gen_get_cstring(edk_name)

  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
    return ""

class EDKCStringConstRefTypeCodec(EDKCStringBaseTypeCodec):

  def __init__(self, kl_type_name, cpp_type_name):
    EDKCStringBaseTypeCodec.__init__(self, kl_type_name, cpp_type_name)

  def gen_kl_param(self, kl_name):
    return self.gen_kl_in_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_in_param(edk_name)

  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    return ""

  def gen_cpp_arg(self, edk_name, cpp_name):
    return self.gen_get_cstring(edk_name)

  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
    return ""
