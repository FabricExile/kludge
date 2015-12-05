class TypeInfo:

  def __init__(
    self,
    type_codec_cls,
    type_spec,
    ):
    self._codec_cls = type_codec_cls
    self.spec = type_spec

  def make_codec(self, value_name):
    return self._codec_cls(value_name, self.spec)
