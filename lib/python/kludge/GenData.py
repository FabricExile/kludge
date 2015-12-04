class GenData:

  def __init__(self, value):
    self.name = value.name
    self.type = value.type_info.spec
    self.children = map(
      lambda child: child._gen_data,
      value.type_info.spec.child_values
      )

    self._codec = value.type_info.codec

  @property
  def element(self):
    return self.children[0]

  @property
  def edk_to_cpp(self):
    return self._codec.gen_edk_to_cpp(self)

  @property
  def cpp_arg(self):
    return self._codec.gen_cpp_arg(self)

  @property
  def cpp_to_edk(self):
    return self._codec.gen_cpp_to_edk(self)
