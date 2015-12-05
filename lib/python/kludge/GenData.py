from kludge import ValueName, TypeCodec

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

    for protocol_name, hook_names in TypeCodec.protocols.iteritems():
      for hook_name in hook_names:
        def impl(type_codec = type_info.codec, gen_hook_name = 'gen_' + hook_name):
          return getattr(
            type_codec,
            gen_hook_name
            )(self)
        setattr(self, hook_name, impl)
