from libkludge.type_codecs.abstract import IndRet

class CStringBase(IndRet):

  def __init__(self, type_name):
    IndRet.__init__(self, type_name)

  def gen_get_cstring(self, edk_name):
    return edk_name + ".getCString()"

class CStringValue(CStringBase):

  def __init__(self, type_name):
    CStringBase.__init__(self, type_name)

  def gen_edk_ind_ret_param(self):
    return self.gen_edk_result_param()

  def gen_edk_store_result_pre(self):
    return self.gen_edk_result_name() + " = ";

  def gen_edk_store_result_post(self):
    return "";

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

CStringConstRef = CStringValue
