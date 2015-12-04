from kludge import GenData

class Param:
  
  def __init__(self, value_name, type_info):
    self._type_codec = type_info.codec
    self._gen_data = GenData(value_name, type_info.spec)

  def gen_kl_param(self):
    return self._type_codec.gen_kl_param(self._gen_data)

  def gen_edk_param(self):
    return self._type_codec.gen_edk_param(self._gen_data)

  def gen_edk_to_cpp(self):
    return self._type_codec.gen_edk_to_cpp(self._gen_data)

  def gen_cpp_arg(self):
    return self._type_codec.gen_cpp_arg(self._gen_data)

  def gen_cpp_to_edk(self):
    return self._type_codec.gen_cpp_to_edk(self._gen_data)
