from libkludge.type_codecs.abstract import IndRet

class StdVectorBase(IndRet):

  def __init__(self, type_name, element_type_codec):
    IndRet.__init__(self, type_name)
    self._element_type_codec = element_type_codec

  def gen_decl_std_vector(self, edk_name, cpp_name):
    element_edk_name = edk_name + "[i]"
    element_cpp_name = "element"
    return """std::vector< %s > %s;
for ( uint32_t i = 0; i < %s.size(); ++i )
{
  %s
  %s.push_back(%s);
}""" % (
  self._element_type_codec.type_name.cpp,
  cpp_name,
  edk_name,
  self._element_type_codec.gen_edk_param_to_cpp_arg(element_edk_name, element_cpp_name),
  cpp_name,
  self._element_type_codec.gen_cpp_arg(element_edk_name, element_cpp_name),
  )

  def gen_upd_std_string(self, edk_name, cpp_name):
    raise Exception("Unimplemented")

class StdVectorValue(StdVectorBase):

  def __init__(self, type_name, element_type_codec):
    StdVectorBase.__init__(self, type_name, element_type_codec)

  def gen_edk_ind_ret_param(self):
    return self.gen_edk_result_param()

  def gen_edk_store_result_pre(self):
    raise Exception("Unimplemented")

  def gen_edk_store_result_post(self):
    raise Exception("Unimplemented")

  def gen_kl_param(self, kl_name):
    return self.gen_kl_in_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_in_param(edk_name)

  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    return self.gen_decl_std_vector(edk_name, cpp_name)

  def gen_cpp_arg(self, edk_name, cpp_name):
    return cpp_name

  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
    return ""

StdVectorConstRef = StdVectorValue
