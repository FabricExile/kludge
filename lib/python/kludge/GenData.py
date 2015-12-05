from kludge import ValueName

class GenData:

  def __init__(self, value_name, type_info):
    self.name = value_name
    self.type = type_info.spec
    self.children = []
    child_index = 1
    for child_type_info in type_info.spec.child_type_infos:
      self.children.append(
        GenData(
          ValueName(value_name.kl + "_RESERVED_child_%u" % child_index),
          child_type_info
          )
        )
      child_index += 1
    if self.children:
      setattr(
        self,
        'element',
        self.children[0]
        )

    self._codec = type_info.codec

  def conv_edk_to_cpp(self):
    return self._codec.gen_conv_edk_to_cpp(self)

  def conv_edk_to_cpp_decl(self):
    return self._codec.gen_conv_edk_to_cpp_decl(self)

  def conv_cpp_to_edk(self):
    return self._codec.gen_conv_cpp_to_edk(self)

  def conv_cpp_to_edk_decl(self):
    return self._codec.gen_conv_cpp_to_edk_decl(self)
