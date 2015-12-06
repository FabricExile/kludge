class TypeInfo:

  def __init__(
    self,
    type_codec_cls,
    type_spec,
    ):
    self._codec_cls = type_codec_cls
    self._spec = type_spec

  @property
  def kl(self):
    return self._spec.kl

  @property
  def edk(self):
    return self._spec.edk

  @property
  def cpp(self):
    return self._spec.cpp

  def make_codec(self, value_name):
    return self._codec_cls(value_name, self._spec)
