from kludge import GenData, TypeCodec

class Value:
  
  def __init__(
    self,
    value_name,
    type_info,
    ):
    self.name = value_name
    self.type_info = type_info

    self._gen_data = GenData(self)

for protocol_name, hook_names in TypeCodec.protocols.iteritems():
  for hook_name in hook_names:
    setattr(
      Value,
      hook_name,
      property(
        # Python lambdas bind variables by name, so we need
        # this default param trick
        lambda self, gen_hook_name='gen_'+hook_name: getattr(
          self.type_info.codec,
          gen_hook_name
          )(self._gen_data)
        )
      )
