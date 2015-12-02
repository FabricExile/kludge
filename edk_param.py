class EDKParam:
  def __init__(self, name, type_codec):
    self._kl_name = name
    self._edk_name = name + "__EDK"
    self._cpp_name = name + "__CPP"
    self._type_codec = type_codec

  def gen_kl_param(self, is_last):
    result = self._type_codec.gen_kl_param(self._kl_name)
    if not is_last:
      result += ","
    return result

  def gen_edk_param(self, is_last):
    result = self._type_codec.gen_edk_param(self._edk_name)
    if not is_last:
      result += ","
    return result

  def gen_edk_param_to_cpp_arg(self):
    return self._type_codec.gen_edk_param_to_cpp_arg(self._edk_name, self._cpp_name)

  def gen_cpp_arg(self, is_last):
    result = self._type_codec.gen_cpp_arg(self._edk_name, self._cpp_name)
    if not is_last:
      result += ","
    return result

  def gen_cpp_arg_to_edk_param(self):
    return self._type_codec.gen_cpp_arg_to_edk_param(self._edk_name, self._cpp_name)
