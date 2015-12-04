from kludge import TypeSpec

class GenData:
  def __init__(
    self,
    value_name,
    type_spec,
    ):
    self.name = value_name
    # if not isinstance(type_spec, TypeSpec):
    #   raise "internal error"
    self.type = type_spec
