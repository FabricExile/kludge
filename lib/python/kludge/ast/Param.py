from kludge import ParamName

class Param:
  
  def __init__(self, name, type_codec):
    self._param_name = ParamName(name)
    self._type_codec = type_codec

  def gen_kl_param(self):
    return self._type_codec.gen_kl_param(self._param_name.kl)

  def gen_edk_param(self):
    return self._type_codec.gen_edk_param(self._param_name.edk)

  def gen_edk_param_to_cpp_arg(self):
    return self._type_codec.gen_edk_param_to_cpp_arg(self._param_name)

  def gen_cpp_arg(self):
    return self._type_codec.gen_cpp_arg(self._param_name)

  def gen_cpp_arg_to_edk_param(self):
    return self._type_codec.gen_cpp_arg_to_edk_param(self._param_name)
