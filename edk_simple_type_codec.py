from edk_type_codec import *

class EDKSimpleBaseTypeCodec(EDKTypeCodec):

  def __init__(self, kl_type_name, cpp_type_name):
    EDKTypeCodec.__init__(self, kl_type_name, cpp_type_name)

  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    return ""

  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
    return ""
  
class EDKSimpleValueTypeCodec(EDKSimpleBaseTypeCodec):

  def __init__(self, kl_type_name, cpp_type_name):
    EDKSimpleBaseTypeCodec.__init__(self, kl_type_name, cpp_type_name)

  def gen_edk_dir_result_type(self):
    return self.kl_type_name

  def gen_edk_ind_ret_param(self):
    return ""

  def gen_edk_store_result_pre(self):
    return self.kl_type_name + " " + self.gen_cpp_result_name() + " = ";

  def gen_edk_store_result_post(self):
    return "";

  def gen_edk_return_dir_result(self):
    return "return " + self.gen_cpp_result_name() + ";"

  def gen_kl_param(self, kl_name):
    return self.gen_kl_in_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_in_param(edk_name)

  def gen_cpp_arg(self, edk_name, cpp_name):
    return edk_name
  
class EDKSimpleConstRefTypeCodec(EDKSimpleBaseTypeCodec):

  def __init__(self, kl_type_name, cpp_type_name):
    EDKSimpleBaseTypeCodec.__init__(self, kl_type_name, cpp_type_name)

  def gen_edk_dir_result_type(self):
    return self.kl_type_name

  def gen_edk_ind_ret_param(self):
    return ""

  def gen_edk_store_result_pre(self):
    return self.kl_type_name + " " + self.gen_cpp_result_name() + " = ";

  def gen_edk_store_result_post(self):
    return "";

  def gen_edk_return_dir_result(self):
    return "return " + self.gen_cpp_result_name() + ";"

  def gen_kl_param(self, kl_name):
    return self.gen_kl_in_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_in_param(edk_name)

  def gen_cpp_arg(self, edk_name, cpp_name):
    return edk_name
  
class EDKSimpleConstPtrTypeCodec(EDKSimpleBaseTypeCodec):

  def __init__(self, kl_type_name, cpp_type_name):
    EDKSimpleBaseTypeCodec.__init__(self, kl_type_name, cpp_type_name)

  def gen_kl_param(self, kl_name):
    return self.gen_kl_in_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_in_param(edk_name)

  def gen_cpp_arg(self, edk_name, cpp_name):
    return self.gen_edk_ptr_to(edk_name)
  
class EDKSimpleMutableRefTypeCodec(EDKSimpleBaseTypeCodec):

  def __init__(self, kl_type_name, cpp_type_name):
    EDKSimpleBaseTypeCodec.__init__(self, kl_type_name, cpp_type_name)

  def gen_edk_dir_result_type(self):
    return self.kl_type_name

  def gen_edk_ind_ret_param(self):
    return ""

  def gen_edk_store_result_pre(self):
    return self.kl_type_name + " " + self.gen_cpp_result_name() + " = ";

  def gen_edk_store_result_post(self):
    return "";

  def gen_edk_return_dir_result(self):
    return "return " + self.gen_cpp_result_name() + ";"

  def gen_kl_param(self, kl_name):
    return self.gen_kl_io_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_io_param(edk_name)

  def gen_cpp_arg(self, edk_name, cpp_name):
    return edk_name
  
class EDKSimpleMutablePtrTypeCodec(EDKSimpleBaseTypeCodec):

  def __init__(self, kl_type_name, cpp_type_name):
    EDKSimpleBaseTypeCodec.__init__(self, kl_type_name, cpp_type_name)

  def gen_kl_param(self, kl_name):
    return self.gen_kl_io_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_io_param(edk_name)

  def gen_cpp_arg(self, edk_name, cpp_name):
    return self.gen_edk_ptr_to(edk_name)
